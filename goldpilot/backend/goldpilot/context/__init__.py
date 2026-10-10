"""Informations de contexte (autres marchés) : jamais utilisées pour générer un signal.

Cahier des charges § 2 : « Les autres marchés peuvent uniquement servir de sources d'information contextuelles pour
analyser le gold. » Les modules de ce paquet ne sont importés ni par la stratégie, ni par le moteur de risque :
le moteur se contente de rafraîchir les valeurs et de les ranger dans la base pour l'affichage.
"""
