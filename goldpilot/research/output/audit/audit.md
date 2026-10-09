# Audit des données historiques

## xau_15m

- 480717 barres, du 2004-06-11 07:15:00 au 2025-09-30 19:30:00
- ordre croissant : True, doublons : 0, OHLC incohérents : 0, prix ≤ 0 : 0
- intervalles réguliers : 98.26 % ; volume : entier (nombre de ticks du broker, pas un volume d'échange)
- trous de plus de 4 jours : 6
  - après 2005-11-23 19:15:00 → reprise 2005-11-28 08:30:00 (4.6 jours)
  - après 2006-11-22 19:00:00 → reprise 2006-11-27 01:00:00 (4.2 jours)
  - après 2025-03-21 22:45:00 → reprise 2025-04-01 01:00:00 (10.1 jours)
  - après 2025-04-04 23:45:00 → reprise 2025-05-01 01:00:00 (26.1 jours)
  - après 2025-06-13 23:45:00 → reprise 2025-07-01 01:00:00 (17.1 jours)
  - après 2025-07-11 23:45:00 → reprise 2025-09-30 19:15:00 (80.8 jours)

## xau_5m

- 50000 barres, du 2025-02-13 22:30:00 au 2025-10-28 17:20:00
- ordre croissant : True, doublons : 0, OHLC incohérents : 0, prix ≤ 0 : 0
- intervalles réguliers : 99.63 % ; volume : entier (nombre de ticks du broker, pas un volume d'échange)
- trous de plus de 4 jours : 0

## Fuseau horaire (heure New York = heure du fichier − décalage)

| Du mois | Au mois | Décalage | Nb mois |
|---|---|---|---|
| 2004-06 | 2011-03 | 6 h | 82 |
| 2011-04 | 2025-07 | 7 h | 171 |

Fichier 5 min : décalage le plus fréquent = 7 h ({7: 6, 8: 3}).
Recoupement 15 min / 5 min : {'barres_communes': 6399, 'ecart_median_cloture': 0.13, 'ecart_p99_cloture': 8.401}