# Prompt — Risk & Money Management Prop Firm

> À copier-coller tel quel dans Claude Code ou tout autre LLM frontier.

---

```
Tu es le meilleur analyste quantitatif de risque au monde, spécialisé dans les mathématiques des comptes prop firm. Chaque chiffre que tu produis doit être dérivé depuis les premiers principes. Zéro approximation. Zéro supposition. Tu montres chaque dérivation, chaque formule, chaque étape de raisonnement.

---

## CONTEXTE DU COMPTE

- Capital initial : 50 000 $
- Drawdown maximum autorisé : calculé en trailing sur l'equity de clôture du jour précédent si elle constitue un nouveau plus-haut.
  - Règle exacte : le high-water mark (HWM) ne se met à jour QUE si l'equity de fin de journée dépasse l'ancien HWM. Le plancher absolu = HWM – 2 000 $. Ce plancher ne descend jamais, même si l'equity baisse.
  - Exemple : J1 clôture à 51 000 $ → HWM = 51 000 $, plancher = 49 000 $. J2 clôture à 50 000 $ → HWM reste 51 000 $, plancher reste 49 000 $.
- Soft breach journalier (sort breach) : perte de 1 000 $ sur l'equity intra-journalière → compte bloqué jusqu'au lendemain.
- Hard breach journalier : perte de 2 000 $ sur l'equity du dernier jour → compte violé, challenge perdu ou compte financé perdu.
- Ratio risque/rendement visé : 3R en moyenne (pour 1 $ risqué, on cible 3 $ de gain).

---

## PHASE 1 — CHALLENGE (EXAMEN)

- Objectif de profit : +3 000 $ (amener le compte de 50 000 $ à 53 000 $).
- Règle de consistance : aucun jour de profit ne peut représenter plus de 40 % du profit total réalisé à date. Si à un moment donné un seul jour représente ≥ 40 % du total cumulé, la règle est violée.
- Objectif principal : maximiser la probabilité de passer le challenge, tout en respectant toutes les règles ci-dessus.

## PHASE 2 — COMPTE FINANCÉ

- Mêmes règles de drawdown trailing (HWM – 2 000 $) et soft breach 1 000 $.
- Même règle de consistance 40 %.
- Pas d'objectif de profit minimum.
- Objectif principal : maximiser les payouts sur le long terme, les rendre les plus élevés et les plus fréquents possibles, sans jamais brûler le compte, en restant actif aussi longtemps que possible.

---

## CE QUE JE TE DEMANDE — MÉTHODOLOGIE OBLIGATOIRE

### ÉTAPE 1 — INVENTAIRE EXHAUSTIF DES SCÉNARIOS

Avant toute chose, imagine dans ton espace de travail interne TOUS les scénarios possibles. Quand je dis tous, je veux dire tous : pas seulement les principaux, pas seulement les cas classiques. Je veux les cas extrêmes, les cas improbables, les cas aberrants, les cascades d'événements, les corrélations inattendues. Aucun scénario ne doit être écarté sous prétexte d'improbabilité. Pour chaque scénario :

1. Décris-le précisément (suite d'événements, état du compte, règles affectées).
2. Calcule sa probabilité d'occurrence (en te basant sur des modèles mathématiques rigoureux — distribution des returns de trading, loi des grands nombres, simulations Monte Carlo si nécessaire).
3. Identifie l'impact sur le compte (equity, HWM, plancher, consistance, soft breach, hard breach).
4. Classe-le : favorable / neutre / destructeur.

Exemples de catégories de scénarios à couvrir (liste non exhaustive — tu dois en générer bien davantage) :
- Série de gains consécutifs déclenchant la règle de consistance.
- Série de pertes consécutives approchant le hard breach.
- Alternance gains/pertes autour du soft breach.
- Un trade exceptionnel qui vaut à lui seul > 40 % du profit cumulé.
- Volatilité soudaine du marché (gap, news macro, flash crash).
- Jours sans trade (gestion du temps vs objectif).
- Profit cumulé proche de 3 000 $ mais consistance en danger.
- Récupération après soft breach (stratégie du lendemain).
- Dégradation progressive du HWM par micro-pertes quotidiennes.
- Compound effect du trailing drawdown lors d'une croissance rapide du compte.
- Sur-trading émotionnel après une série de pertes.
- Timing du challenge (nombre de jours restants vs profit restant à faire).
- Phase financée : payout trop précoce réduisant la base de capital.
- Phase financée : accumulation sans payout et risque de tout perdre.
- Tout autre scénario que ton analyse rigoureuse identifie.

### ÉTAPE 2 — MODÉLISATION MATHÉMATIQUE

Pour les deux phases, en utilisant les scénarios identifiés :

1. **Modélise la distribution des trades** : à partir d'un winrate W (que tu vas optimiser), d'un RR moyen de 3, dérive la distribution des P&L par trade et par journée.
2. **Simule Monte Carlo** : au minimum 10 000 chemins pour chaque plan. Calcule pour chaque plan :
   - Probabilité de passer le challenge (Phase 1).
   - Probabilité de survie à 1 mois / 3 mois / 6 mois / 1 an (Phase 2).
   - Espérance de payout total sur 12 mois (Phase 2).
   - Distribution des durées avant breach.
3. **Optimise les paramètres** : risque par trade (en $ et en % du capital), nombre de trades par jour, seuils d'arrêt journalier, seuil de prise de profit partielle.
4. **Dérive analytiquement** (pas seulement empiriquement) les formules closes ou semi-closes lorsque c'est possible. Montre chaque étape.

### ÉTAPE 3 — PLAN PHASE 1 (CHALLENGE)

Produis un plan opérationnel complet, optimisé mathématiquement, incluant :

- **Risque par trade** : montant exact en $, pourcentage du capital, justification par la formule de Kelly ou équivalent.
- **Nombre de trades maximum par jour**.
- **Seuil d'arrêt journalier** (différent du hard breach — ton propre seuil de protection).
- **Gestion de la règle de consistance 40 %** : règle de décision jour par jour (quand ralentir, quand s'arrêter, comment lisser les profits sur plusieurs jours si nécessaire).
- **Stratégie de progression vers les 3 000 $** : découpage en étapes, ajustement du risque selon la distance à l'objectif et la distance au plancher.
- **Règle de gestion après soft breach** : comportement le lendemain.
- **Règle de gestion en cas de profit important** : comment éviter de violer le 40 % le lendemain.
- **Probabilité finale de succès du plan** avec les paramètres retenus (issue des simulations).

### ÉTAPE 4 — PLAN PHASE 2 (COMPTE FINANCÉ)

Produis un plan opérationnel complet, optimisé mathématiquement, incluant :

- **Risque par trade** : montant exact, justifié.
- **Stratégie de payout** : à quel seuil de profit demander un payout, quelle fréquence, quel montant, pour maximiser les gains extraits sans fragiliser le compte.
- **Gestion du trailing drawdown en phase de croissance** : comment se comporter quand le HWM monte (le plancher monte aussi, donc la marge se compresse relativement).
- **Gestion de la règle de consistance 40 %** en phase infinie (pas d'objectif, donc risque de jours exceptionnels qui contraignent tous les jours suivants).
- **Stratégie de survie longue durée** : règles pour rester opérationnel des années.
- **Stratégie d'optimisation des payouts** : maximiser la somme extraite sur 12 mois en fonction du niveau de risque.
- **Probabilité de survie à 3 mois / 6 mois / 12 mois** avec les paramètres retenus.
- **Espérance mathématique de gain total extrait sur 12 mois**.

### ÉTAPE 5 — TABLEAU DE BORD ET RÈGLES DÉCISIONNELLES

Fournis un tableau de décision clair, utilisable au quotidien, sous forme de règles SI/ALORS :

- Si mon equity actuelle est X, mon HWM est Y, mon profit cumulé est Z, alors je risque exactement [montant] par trade ce jour-là.
- Si mon meilleur jour représente P % de mon profit total, alors [action].
- Si j'approche du soft breach, alors [action].
- Etc.

Ce tableau doit couvrir tous les états du compte significatifs identifiés à l'Étape 1.

---

## FORMAT DE RÉPONSE

- Réponds entièrement en français.
- Structure ta réponse avec des titres clairs.
- Présente toutes les formules en notation mathématique explicite.
- Pour chaque paramètre retenu, justifie pourquoi c'est la valeur optimale et pas une autre.
- Sois exhaustif mais sans remplissage inutile : chaque phrase doit apporter de l'information.
- Les deux plans (Challenge et Financé) doivent être distincts, complets, et directement applicables.
- Conclus par une synthèse en une page : les 10 règles absolues à ne jamais violer, une pour le challenge et l'autre pour la phase financée, dérivées de l'ensemble de l'analyse.
```
