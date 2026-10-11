import { Link } from "react-router-dom";
import { useTitre } from "../lib/hooks";
import { Badge, Card } from "../components/ui";

export function Help() {
  useTitre("Aide");
  return (
    <>
      <div className="page-head">
        <h1>Aide</h1>
      </div>
      <nav className="toc" aria-label="Sections de l'aide">
        <a href="#etats">Les états</a>
        <a href="#alerte">Quand une alerte arrive</a>
        <a href="#simulation">Simulation</a>
        <a href="#statuts">Statuts d'un signal</a>
        <a href="#glossaire">Glossaire</a>
        <a href="#documents">Documents</a>
      </nav>

      <Card titre="Lire les états de la page d'accueil" id="etats" testid="aide-etats">
        <p>
          <Badge ton="ok">Vert</Badge> uniquement quand le serveur confirme que l'élément fonctionne <strong>et</strong> qu'aucun composant
          critique (connexion, données, moteur) n'est en panne.
        </p>
        <p>
          <Badge ton="warn">Orange</Badge> l'élément demande ton attention (pause, préchauffage, notifications non configurées…), ou il
          fonctionne mais un autre composant critique est en panne.
        </p>
        <p>
          <Badge ton="bad">Rouge</Badge> panne : aucun signal fiable ne peut être produit. Si le serveur ne répond plus, tout passe en rouge et
          un bandeau « Serveur injoignable » apparaît.
        </p>
        <ul className="steps">
          <li>
            <strong>Connexion</strong> : le serveur et le moteur donnent signe de vie (moins d'une minute).
          </li>
          <li>
            <strong>Données de marché</strong> : les prix arrivent, sont récents et cohérents. Sinon le moteur passe en « mode sécurisé » et
            annule les signaux en attente.
          </li>
          <li>
            <strong>Moteur</strong> : <em>actif</em> (surveille le marché), <em>préchauffage</em> (pas encore assez d'historique),{" "}
            <em>pause</em> (suspendu par toi), <em>mode sécurisé</em> (données douteuses), <em>arrêt de sécurité</em> (performances
            dégradées au-delà des seuils fixés à l'avance : reprise manuelle), <em>arrêté</em> (le moteur ne répond plus).
          </li>
          <li>
            <strong>Notifications</strong> : opérationnelles, en erreur (échecs d'envoi), non configurées (Telegram absent) ou désactivées par
            toi.
          </li>
        </ul>
      </Card>

      <Card titre="Quand une alerte arrive sur ton téléphone" id="alerte" testid="aide-alerte">
        <ol className="steps">
          <li>
            Regarde d'abord la première ligne : si elle indique <strong>SIMULATION — NE PAS EXÉCUTER</strong>, n'ouvre aucune position : le
            signal sert uniquement au suivi.
          </li>
          <li>Vérifie le contrat (par exemple MGCZ6 sur Tradovate), le sens (LONG = achat, SHORT = vente) et la plage d'entrée.</li>
          <li>Si le prix est déjà sorti de la plage, ou si la validité est dépassée, laisse passer : un signal ancien n'est plus exploitable.</li>
          <li data-testid="aide-rappel-minute">
            Si l'entrée est exploitable, entre <strong>dans la minute</strong> : dans la recherche, un retard de 5 minutes fait passer
            l'espérance simulée de +0,126 R à +0,045 R par trade (l'essentiel de l'avantage disparaît). Ne poursuis jamais le prix.
          </li>
          <li>Place le stop-loss exactement au prix indiqué, avec la taille indiquée (jamais plus).</li>
          <li>Suis les messages suivants : stop déplacé (stop suiveur), sortie, annulation. Ferme toujours avant l'heure de sortie maximale.</li>
          <li>Ensuite, ouvre le signal sur le site et utilise « Déclarer mon exécution » pour garder une trace (déclaré par toi, non confirmé).</li>
        </ol>
      </Card>

      <Card titre="Ce que signifie « simulation »" id="simulation" testid="aide-simulation">
        <p>
          La stratégie actuelle n'a pas satisfait les critères de validation fixés avant les tests (voir <Link to="/statistiques">Statistiques</Link>
          ). Le système fonctionne donc en <strong>simulation</strong> : il analyse le marché, émet des signaux et suit des positions fictives
          avec des coûts estimés, pour mesurer en conditions réelles si la stratégie tient. Aucun argent n'est engagé et tu ne dois pas exécuter
          ces signaux sur ton compte FundedNext.
        </p>
        <p>
          Le mode réel reste verrouillé par le serveur tant que la stratégie n'est pas validée, que FundedNext n'a pas confirmé par écrit que cet
          outil est autorisé, et que tu n'as pas saisi la phrase de confirmation. Même en réel, GoldPilot ne passe jamais d'ordre : tu exécutes
          toi-même.
        </p>
        <p>
          Le <strong>rejeu historique</strong> (bandeau bleu) est un autre cas : le système rejoue des prix passés pour être testé. Rien n'y est
          réel, pas même la date.
        </p>
      </Card>

      <Card titre="Statuts d'un signal" id="statuts" testid="aide-statuts">
        <dl className="glossary">
          <dt>En attente de déclenchement</dt>
          <dd>Le signal attend que le prix atteigne la zone d'entrée prévue.</dd>
          <dt>Actif</dt>
          <dd>
            Le signal est ouvert (entrée déclenchée ou position simulée suivie). Regarde l'étiquette d'entrée juste à côté :
            seule « Entrée exploitable maintenant » permet d'entrer (prix dans la plage et validité non écoulée).
          </dd>
          <dt>Entrée fermée — ne plus entrer</dt>
          <dd>
            Le prix est sorti de la plage d'entrée, la validité est écoulée ou le mode sécurisé interdit l'entrée : n'entre pas. Si tu es
            déjà en position, garde ton stop ; la position simulée reste suivie jusqu'à sa sortie.
          </dd>
          <dt>Annulé</dt>
          <dd>Annulé par le système (mode sécurisé, données douteuses…) ou par toi avant toute entrée simulée : ne pas entrer.</dd>
          <dt>Expiré</dt>
          <dd>La durée de validité est dépassée sans entrée : ne pas entrer.</dd>
          <dt>Clôturé</dt>
          <dd>
            La position simulée est sortie (stop, stop suiveur ou heure de sortie). Si les prix manquaient à l'heure de sortie, le résultat
            s'affiche « Résultat inconnu (données manquantes) » : aucun résultat n'est inventé et ce trade n'entre pas dans les statistiques.
          </dd>
          <dt>Position simulée</dt>
          <dd>Position fictive suivie par le système aux prix du marché, avec glissement et commission estimés.</dd>
          <dt>Exécution déclarée par toi (non confirmée)</dt>
          <dd>
            Ce que tu déclares toi-même avoir exécuté. GoldPilot n'est pas relié à Tradovate : il ne peut jamais confirmer qu'un ordre a été
            exécuté. Aucune position n'est donc affichée comme « réellement exécutée ».
          </dd>
        </dl>
      </Card>

      <Card titre="Glossaire" id="glossaire" testid="aide-glossaire">
        <dl className="glossary">
          <dt>MGC (Micro Gold)</dt>
          <dd>Contrat à terme sur l'or du COMEX représentant 10 onces. 1 $ de variation du prix = 10 $ par contrat.</dd>
          <dt>GC</dt>
          <dd>Contrat à terme « standard » sur l'or (100 onces), 10 fois plus gros que le MGC.</dd>
          <dt>XAU/USD</dt>
          <dd>Or au comptant (ou CFD). Son prix diffère légèrement de celui des contrats à terme ; il n'est utilisé que pour les tests.</dd>
          <dt>Roll (changement de contrat)</dt>
          <dd>Les contrats à terme expirent : avant l'échéance, on passe au contrat suivant. La date est indiquée sur la page d'accueil.</dd>
          <dt>R</dt>
          <dd>L'unité de risque d'un trade : 1 R = la perte si le stop initial est touché. Un gain de +2 R = deux fois le risque pris.</dd>
          <dt>Espérance</dt>
          <dd>Gain moyen par trade, en R, après les coûts. Positive ne veut pas dire garantie : il faut regarder l'incertitude (IC95).</dd>
          <dt>IC95</dt>
          <dd>Intervalle de confiance à 95 % : la plage dans laquelle se trouve probablement la vraie valeur. S'il contient 0, rien n'est prouvé.</dd>
          <dt>ATR</dt>
          <dd>« Average True Range » : l'amplitude moyenne des mouvements récents. Sert à placer les stops selon la volatilité.</dd>
          <dt>Stop suiveur</dt>
          <dd>Stop qui suit le prix à distance fixe (ici en ATR) quand le trade avance en ta faveur, pour protéger les gains.</dd>
          <dt>Drawdown</dt>
          <dd>La plus forte baisse depuis un plus haut. Le drawdown maximal mesure la pire période traversée.</dd>
          <dt>Profit factor</dt>
          <dd>Gains totaux divisés par pertes totales. Au-dessus de 1 : plus de gains que de pertes.</dd>
          <dt>Walk-forward</dt>
          <dd>Test où les paramètres sont choisis sur le passé puis appliqués à la période suivante jamais vue, année après année.</dd>
          <dt>Monte-Carlo</dt>
          <dd>Milliers de tirages au hasard des trades passés pour estimer les chances de réussir ou d'échouer un challenge.</dd>
          <dt>Plancher (perte maximale)</dt>
          <dd>Le solde sous lequel le compte FundedNext est perdu. Il monte avec ton plus haut solde de fin de journée, puis se fige.</dd>
          <dt>Consistance</dt>
          <dd>Règle du challenge : aucun jour ne doit dépasser 40 % de l'objectif de profit, sinon l'objectif augmente.</dd>
          <dt>Webhook</dt>
          <dd>Message automatique envoyé par TradingView au serveur à chaque alerte.</dd>
        </dl>
      </Card>

      <Card titre="Documents de référence" id="documents" testid="aide-documents">
        <p className="small">Dans le dossier du projet (sur le serveur ou dans le dépôt Git) :</p>
        <ul className="steps">
          <li>
            <code>docs/01_environnement_sources_et_acces.md</code> — sources officielles, accès nécessaires, coûts.
          </li>
          <li>
            <code>docs/02_architecture.md</code> — fonctionnement technique du système.
          </li>
          <li>
            <code>docs/03_protocole_de_recherche.md</code> — protocole de validation fixé avant les tests.
          </li>
          <li>
            <code>research/output/selection/selection.md</code> et <code>research/output/final/final.md</code> — résultats complets.
          </li>
          <li>
            <code>pine/goldpilot_bridge.pine</code> — le script TradingView (aussi disponible dans <Link to="/reglages#tradingview">Réglages</Link>).
          </li>
        </ul>
      </Card>
    </>
  );
}
