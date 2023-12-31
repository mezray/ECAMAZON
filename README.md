# ECAMAZON Dispatching

## Routes API

### POST /add_colis

Cette route permet d'ajouter un nouveau colis à une livraison. Si une livraison a déjà 30 colis, un nouveau camion est sélectionné pour la prochaine livraison.

**Paramètres du corps de la requête :**

- `id` : L'identifiant du colis.
- `adresse_x` : La coordonnée x de l'adresse de livraison du colis.
- `adresse_y` : La coordonnée y de l'adresse de livraison du colis.

### POST /postPosColisFromDevice

Cette route permet de mettre à jour l'état d'un colis.

**Paramètres du corps de la requête :**

- `colis_id` : L'identifiant du colis.
- `etat_colis` : Le nouvel état du colis.

### POST /postPosCamionFromDevice

Cette route permet de mettre à jour la position d'un camion.

**Paramètres du corps de la requête :**

- `camion_id` : L'identifiant du camion.
- `camion_pos_x` : La nouvelle coordonnée x de la position du camion.
- `camion_pos_y` : La nouvelle coordonnée y de la position du camion.

### GET /getLivraison

Cette route retourne les informations sur les livraisons en cours. Elle retourne l'identifiant de la livraison, l'identifiant du colis, les coordonnées de l'adresse de livraison du colis et l'état du colis.
