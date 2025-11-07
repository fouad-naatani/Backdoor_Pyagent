# Backdoor_Pyagent
Backdoor basée sur le concept de connexion inverse afin d'établir le contrôle à distance de la machine cible  &lt;&lt;— le backdoor (client) et le listener (serveur) — >> (hacking éthique)
- **Une connexion inverse** est un mécanisme où la machine ciblée initie la connexion vers une machine de contrôle, au lieu que l’attaquant s’y connecte directe
<img width="743" height="364" alt="image" src="https://github.com/user-attachments/assets/6cb9f4ee-e426-424d-96f8-304bc533f8e7" />

---
# 1. Rôle de chacun

- **Listener (serveur)** : reste en écoute sur une adresse IP et un port. Il attend qu’un client (la machine ciblée) se connecte. C’est l’interface de l’opérateur humain : il envoie des commandes au client, reçoit les réponses et gère les transferts de fichiers.

- **Backdoor (client)** : s’exécute sur la machine distante et initie la connexion vers le listener (reverse connection). Il reçoit les commandes, les exécute localement (ou effectue des opérations sur le système de fichiers), et renvoie les résultats au listener.
---
# 2. Principe de fonctionnement (flux de données)

- **Connexion inverse (reverse shell)** : au lieu que le serveurouvre une connexion vers le client, le client se connecte au serveur. Cela contourne souvent des restrictions côté réseau (NAT/firewall) sur la machine cliente.

- **Échange structuré** : les deux côtés sérialisent les messages (ici JSON) pour envoyer des commandes et recevoir des réponses de façon fiable.

- **Exécution et retour** : le listener envoie une commande (ex. lister un dossier). Le client exécute la commande localement, capture la sortie, la sérialise et la renvoie.

- **Transfert de fichiers** : les fichiers binaires sont encodés en base64 pour être transférés via le canal JSON (texte). Le côté expéditeur encode, le récepteur décode et écrit le fichier.

# 3. Fonctionnalités typiques implémentées

- **Commande à distance** : exécution de commandes shell / système et renvoi de la sortie.

- **Changement de répertoire (cd)** : modifier le contexte du shell distant.

- **Upload / download** : transfert de fichiers bi-directionnel en base64.

 - **Exit / fermeture **: fermeture propre de la session.

# 4. Protocoles et formats utilisés

- **TCP** : transport fiable pour transmettre les octets.

- **JSON** : format de message structuré pour encoder commandes et résultats (lisible, portable).

- **Base64** : pour transformer des données binaires en texte afin de les inclure dans du JSON.

# 6. Sécurité, éthique et légalité

- **Risque élevé** : ces mécanismes donnent un contrôle à distance sur une machine. Utilisés sans autorisation, ils constituent une intrusion illégale dans la plupart des pays.

- **Sécuriser si usage légitime** : authentification mutuelle, chiffrement (TLS), journalisation, permissions limitées, réseau isolé pour tests.

- **Bonnes pratiques** : ne tester que sur des environnements contrôlés (VMs, réseau isolé) et obtenir toujours une autorisation écrite.
