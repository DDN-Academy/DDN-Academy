"""Authentification (un seul utilisateur : toi), sessions et limitation des abus.

* Mot de passe : hachage scrypt (bibliothèque standard), jamais stocké en clair ; seul le hachage est
  placé dans la variable ADMIN_PASSWORD_HASH.
* Session : jeton aléatoire de 256 bits dans un cookie HttpOnly, SameSite=Strict, Secure en production ;
  seul le SHA-256 du jeton est stocké en base (une fuite de la base ne permet pas de se connecter).
* Protection CSRF : cookie SameSite=Strict + en-tête obligatoire X-GoldPilot sur toute requête qui modifie.
* Connexion : 5 essais par 15 minutes et par adresse IP.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from collections import defaultdict, deque
from datetime import timedelta

from fastapi import HTTPException, Request
from sqlalchemy import delete

from .. import db
from ..config import settings

COOKIE = "gp_session"
N, R, P = 2 ** 15, 8, 1


def hash_password(pw: str) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.scrypt(pw.encode(), salt=salt, n=N, r=R, p=P, dklen=32, maxmem=64 * 1024 * 1024)
    return "scrypt$" + base64.b64encode(salt).decode() + "$" + base64.b64encode(dk).decode()


def verify_password(pw: str, stored: str) -> bool:
    try:
        _, s, h = stored.split("$")
        dk = hashlib.scrypt(pw.encode(), salt=base64.b64decode(s), n=N, r=R, p=P, dklen=32, maxmem=64 * 1024 * 1024)
        return hmac.compare_digest(dk, base64.b64decode(h))
    except Exception:
        return False


def client_ip(request: Request) -> str:
    if settings().trust_proxy:
        fwd = request.headers.get("x-forwarded-for", "")
        if fwd:
            return fwd.split(",")[0].strip()
    return request.client.host if request.client else "inconnu"


class RateLimiter:
    def __init__(self, max_hits: int, window_s: float):
        self.max, self.window = max_hits, window_s
        self.hits: dict[str, deque] = defaultdict(deque)

    def allow(self, key: str) -> bool:
        now = time.monotonic()
        q = self.hits[key]
        while q and now - q[0] > self.window:
            q.popleft()
        if len(q) >= self.max:
            return False
        q.append(now)
        return True


login_limiter = RateLimiter(5, 15 * 60)
webhook_limiter = RateLimiter(120, 60)
api_limiter = RateLimiter(300, 60)


def _digest(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_session(ip: str) -> str:
    token = secrets.token_urlsafe(32)
    with db.session() as s:
        s.execute(delete(db.LoginSession).where(db.LoginSession.expires_at < db.now()))
        s.add(db.LoginSession(token_hash=_digest(token), ip=ip, expires_at=db.now() + timedelta(hours=settings().session_hours)))
    return token


def end_session(token: str | None) -> None:
    if token:
        with db.session() as s:
            s.execute(delete(db.LoginSession).where(db.LoginSession.token_hash == _digest(token)))


def require_user(request: Request) -> str:
    token = request.cookies.get(COOKIE)
    if token:
        with db.session() as s:
            row = s.get(db.LoginSession, _digest(token))
            if row is not None and row.expires_at > db.now():
                if request.method not in ("GET", "HEAD", "OPTIONS") and request.headers.get("x-goldpilot") != "1":
                    raise HTTPException(403, "en-tête de sécurité manquant")
                return "utilisateur"
    raise HTTPException(401, "connexion requise")
