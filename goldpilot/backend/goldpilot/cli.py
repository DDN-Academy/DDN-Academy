"""Outils en ligne de commande.

  python -m goldpilot.cli hash-password      → génère ADMIN_PASSWORD_HASH (le mot de passe est demandé, non affiché)
  python -m goldpilot.cli secret             → génère une valeur aléatoire pour SECRET_KEY ou TV_WEBHOOK_TOKEN
  python -m goldpilot.cli migrate            → applique les migrations de la base
  python -m goldpilot.cli check              → vérifie la configuration (sans afficher les secrets)
  python -m goldpilot.cli research-summary   → affiche le statut de validation de la stratégie
"""
from __future__ import annotations

import getpass
import secrets
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "hash-password":
        from .api.security import hash_password

        pw = getpass.getpass("Mot de passe (12 caractères minimum) : ")
        if len(pw) < 12:
            print("Mot de passe trop court.", file=sys.stderr)
            return 1
        if getpass.getpass("Confirmer : ") != pw:
            print("Les deux saisies diffèrent.", file=sys.stderr)
            return 1
        print(hash_password(pw))
        return 0
    if cmd == "secret":
        print(secrets.token_urlsafe(36))
        return 0
    if cmd == "migrate":
        from alembic import command
        from alembic.config import Config

        cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
        cfg.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "migrations"))
        command.upgrade(cfg, "head")
        print("Migrations appliquées.")
        return 0
    if cmd == "check":
        from .config import settings

        st = settings()
        probs = st.startup_problems()
        print(f"Environnement : {st.app_env} ; source de données : {st.data_source}")
        print(f"Telegram configuré : {'oui' if st.telegram_bot_token and st.telegram_chat_id else 'non'}")
        print(f"Jeton webhook TradingView : {'défini' if st.tv_webhook_token else 'absent'}")
        for p in probs:
            print("PROBLÈME :", p)
        return 1 if probs else 0
    if cmd == "research-summary":
        from .engine.strategy_config import validation_status

        print(validation_status())
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
