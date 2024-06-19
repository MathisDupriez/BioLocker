# BioLocker Application

## Description
Classe représentant l'application `BioLocker`.

Cette classe est utilisée pour créer et configurer l'application `BioLocker`.
Elle hérite de la classe `App` du framework Kivy.

## Attributs
- **sambaManager**: Objet `SambaManager` pour gérer le partage de fichiers.
- **model**: Objet `FingerprintModel` pour gérer les données de l'empreinte digitale.
- **view**: Objet `MainView` pour afficher l'interface utilisateur.
- **controller**: Objet `FingerprintController` pour gérer la logique métier.

## Méthodes

### `build()`
Méthode pour construire et configurer l'application.

## Usage

Pour exécuter l'application, instancier la classe `BioLocker` et appeler sa méthode `run()`.


_____________

# MainView

## Description
Classe représentant la vue principale de l'application.

Cette classe hérite de la classe `BoxLayout` et est utilisée pour afficher l'interface utilisateur principale de l'application.

## Attributs
- **controller**: (`ObjectProperty`) Une propriété d'objet utilisée pour référencer le contrôleur de la vue.

## Méthodes

### `__init__(self, **kwargs)`
Méthode spéciale appelée lors de l'initialisation de la classe.

### `setup(self, controller)`
Méthode utilisée pour configurer le contrôleur de la vue.

### `on_size(self, *args)`
Méthode appelée lorsqu'il y a un changement de taille de la vue.

### `add_log(self, log_message, log_type="info")`
Méthode utilisée pour ajouter un message de journalisation à la vue.

### `_add_log(self, log_message, log_type)`
Méthode interne utilisée pour ajouter un message de journalisation à la vue.

### `change_main_button_text(self, text)`
Méthode utilisée pour changer le texte du bouton principal de la vue.

## Configurations Initiales
- Configuration de la fenêtre pour qu'elle se lance en plein écran, avec une largeur de 480 pixels et une hauteur de 320 pixels.
- La fenêtre est rendue non redimensionnable.
- La version de Kivy requise est `2.1.0`.
- Chargement du fichier `.kv` associé à la vue principale.

## Usage

Pour utiliser cette vue, il faut créer une instance de `MainView` et configurer son contrôleur via la méthode `setup`.


_______________


# PasswordReader

## Description
Classe utilisée pour lire les mots de passe à partir d'un fichier JSON.

## Attributs
- **file_path**: Chemin du fichier JSON contenant les données des utilisateurs.

## Méthodes

### `__init__(self, file_path)`
Méthode d'initialisation de la classe.

- **Paramètres** :
  - `file_path` : Chemin du fichier JSON.

### `read_password(self)`
Méthode pour lire le mot de passe du premier utilisateur dans le fichier JSON.

- **Retour** :
  - Le mot de passe du premier utilisateur trouvé ou `None` si aucun mot de passe n'est trouvé.

### `get_password_for_user(self, username)`
Méthode pour obtenir le mot de passe d'un utilisateur spécifique.

- **Paramètres** :
  - `username` : Nom d'utilisateur pour lequel récupérer le mot de passe.

- **Retour** :
  - Le mot de passe de l'utilisateur spécifié ou `None` si l'utilisateur ou le mot de passe n'est pas trouvé.

## Structure JSON Attendue

Le fichier JSON doit avoir la structure suivante :

```json
{
    "users": [
        {
            "username": "user1",
            "password": "password1"
        },
        {
            "username": "user2",
            "password": "password2"
        }
    ]
}
```


_____________________

# FingerprintModel

## Description
Représente un modèle d'empreinte digitale qui interagit avec un capteur d'empreintes digitales.

## Arguments du Constructeur
- **port** (`str`, optionnel): Le port auquel le capteur d'empreintes digitales est connecté. Par défaut, '/dev/ttyAMA10'.
- **baud** (`int`, optionnel): Le débit en bauds pour la communication avec le capteur d'empreintes digitales. Par défaut, 9600.
- **timeout** (`int`, optionnel): La valeur de timeout pour la communication avec le capteur d'empreintes digitales. Par défaut, 3.

## Attributs
- **fp_sensor** (`fplib`): L'objet capteur d'empreintes digitales.

## Méthodes

### `__init__(self, port='/dev/ttyAMA10', baud=9600, timeout=3)`
Initialise une nouvelle instance de la classe `FingerprintModel`.

### `is_finger_pressed(self)`
Vérifie si un doigt est actuellement pressé sur le capteur d'empreintes digitales.

- **Retourne** : `bool` - `True` si un doigt est pressé, `False` sinon.

### `turn_on_led(self)`
Allume la LED du capteur d'empreintes digitales.

### `turn_off_led(self)`
Éteint la LED du capteur d'empreintes digitales.

### `identify_fingerprint(self)`
Identifie l'empreinte digitale actuellement placée sur le capteur.

- **Retourne** : `int` - L'ID de l'empreinte digitale identifiée.

### `get_template_by_check(self, id_to_retrieve)`
Récupère le modèle d'empreinte digitale pour l'ID donné.

- **Arguments** :
  - `id_to_retrieve` (`int`): L'ID du modèle d'empreinte digitale à récupérer.

- **Retourne** : `str` - La représentation hexadécimale du modèle d'empreinte digitale ou un message d'erreur.

- **Exceptions** :
  - `ValueError` : Si l'ID fourni est invalide.


____________________________



# SambaManager

## Description
Gère la gestion des utilisateurs et des partages Samba.

## Arguments du Constructeur
- **smb_conf_path** (`str`) : Chemin du fichier de configuration `smb.conf`. Par défaut, '/etc/samba/smb.conf'.
- **fixed_share_path** (`str`) : Chemin du répertoire de partage fixe. Par défaut, '/srv/samba/fixedshare'.

## Attributs
- **smb_conf_path** (`str`) : Chemin du fichier de configuration `smb.conf`.
- **fixed_share_path** (`str`) : Chemin du répertoire de partage fixe.

## Méthodes

### `generate_random_username(self, length=8)`
Génère un nom d'utilisateur aléatoire.

- **Arguments** :
  - `length` (`int`) : Longueur du nom d'utilisateur généré. Par défaut, 8.
- **Retourne** : `str` - Nom d'utilisateur aléatoire.

### `add_user(self, username, password)`
Ajoute un utilisateur au système et à Samba.

- **Arguments** :
  - `username` (`str`) : Nom d'utilisateur.
  - `password` (`str`) : Mot de passe de l'utilisateur.

### `delete_user(self, username)`
Supprime un utilisateur de Samba et du système.

- **Arguments** :
  - `username` (`str`) : Nom d'utilisateur.

### `create_share(self, share_name, username)`
Crée un partage Samba avec le nom spécifié et l'attribue à l'utilisateur spécifié.

- **Arguments** :
  - `share_name` (`str`) : Nom du partage.
  - `username` (`str`) : Nom d'utilisateur auquel attribuer le partage.

### `remove_share(self, share_name)`
Supprime un partage Samba.

- **Arguments** :
  - `share_name` (`str`) : Nom du partage à supprimer.

### `start_samba(self)`
Démarre les services Samba (`smbd` et `nmbd`).

### `stop_samba(self)`
Arrête les services Samba (`smbd` et `nmbd`).

### `create_random_user_and_share(self, share_name)`
Crée un utilisateur aléatoire et un partage associé.

- **Arguments** :
  - `share_name` (`str`) : Nom du partage.
- **Retourne** : `tuple` - Nom d'utilisateur et mot de passe générés.

### `remove_random_user_and_share(self, share_name, username)`
Supprime un utilisateur et le partage associé.

- **Arguments** :
  - `share_name` (`str`) : Nom du partage.
  - `username` (`str`) : Nom d'utilisateur.

### `open_share(self)`
Démarre les services Samba pour ouvrir le partage.

### `close_share(self)`
Arrête les services Samba pour fermer le partage.


_________________________

# FingerprintController

## Description
Contrôleur pour l'authentification par empreinte digitale.

## Attributs
- **model** (`object`) : L'objet modèle utilisé pour l'authentification par empreinte digitale.
- **view** (`object`) : L'objet vue utilisé pour l'affichage.
- **samba_manager** (`object`) : L'objet gestionnaire Samba utilisé pour le partage de fichiers.
- **fingerprint_done** (`bool`) : Indique si l'authentification par empreinte digitale est terminée.
- **code_entered** (`str`) : Le code saisi par l'utilisateur.
- **Finger_print** (`str`) : L'empreinte digitale de l'utilisateur.
- **checking_Code** (`bool`) : Indique si le code est en cours de vérification.
- **locking** (`bool`) : Indique si le système est verrouillé.
- **unlocking** (`bool`) : Indique si le système est déverrouillé.
- **encryption_state** (`bool`) : Indique l'état du chiffrement des fichiers.
- **sharing_state** (`bool`) : Indique l'état du partage de fichiers.
- **current_username** (`str`) : Le nom d'utilisateur actuel.
- **current_password** (`str`) : Le mot de passe actuel.
- **share_name** (`str`) : Le nom du partage Samba.
- **username_share** (`str`) : Le nom d'utilisateur pour le partage Samba.
- **password_share** (`str`) : Le mot de passe pour le partage Samba.
- **view_ops** (`object`) : L'objet opérations de vue.
- **actions** (`object`) : L'objet actions d'authentification par empreinte digitale.
- **file_ops** (`object`) : L'objet opérations de fichiers.
- **password_reader** (`object`) : L'objet lecteur de mots de passe.

## Méthodes

### `__init__(self, model, view, samba_manager)`
Initialise le contrôleur avec le modèle, la vue et le gestionnaire Samba.

- **Arguments** :
  - `model` (`object`) : L'objet modèle utilisé par le contrôleur.
  - `view` (`object`) : L'objet vue utilisé par le contrôleur.
  - `samba_manager` (`object`) : L'objet gestionnaire Samba utilisé par le contrôleur.

### `unlock(self, instance)`
Déverrouille le système en utilisant l'authentification par empreinte digitale.

- **Arguments** :
  - `instance` (`object`) : L'instance de l'objet qui a déclenché l'événement.

### `lock(self, instance)`
Verrouille le système.

- **Arguments** :
  - `instance` (`object`) : L'instance de l'objet qui a déclenché l'événement.

### `wait_for_fingerprint(self, dt)`
Attend que l'authentification par empreinte digitale soit terminée.

- **Arguments** :
  - `dt` (`float`) : Le temps écoulé depuis la dernière mise à jour de l'horloge.
- **Retourne** : `bool` - `True` si l'attente doit se poursuivre, `False` sinon.

### `identify_fingerprint(self)`
Identifie l'empreinte digitale et effectue les actions nécessaires.

### `check_code(self)`
Vérifie le code saisi par l'utilisateur.

### `verify_code(self)`
Vérifie le code saisi.

### `handle_crypt(self)`
Gère le chiffrement et le déchiffrement des fichiers en fonction de l'état de l'encryption et du verrouillage.

### `start_samba(self)`
Démarre le partage Samba.

### `stop_samba(self)`
Arrête le partage Samba.

### `numpad_button_pressed(self, instance)`
Gère les événements de pression des boutons du pavé numérique.

- **Arguments** :
  - `instance` (`object`) : L'instance de l'objet qui a déclenché l'événement.

### `get_local_ip(self)`
Récupère l'adresse IP locale de l'appareil.

- **Retourne** : `str` - L'adresse IP locale de l'appareil.

### `ip_button_pressed(self)`
Gère l'événement de pression du bouton IP.

### `exit_handler(self)`
Fonction exécutée à la sortie du programme.

### `select_file_encrypt(self)`
Sélectionne un fichier pour le chiffrement.

### `select_file_decrypt(self)`
Sélectionne un fichier pour le déchiffrement.


______________________


# FolderEncryptor

## Description
Une classe qui fournit des méthodes pour crypter et décrypter des fichiers et des dossiers.

## Arguments du Constructeur
- **key** (`bytes`) : L'empreinte utilisée pour le cryptage et le décryptage.

## Attributs
- **key** (`bytes`) : L'empreinte utilisée pour le cryptage et le décryptage.

## Méthodes

### `__init__(self, key)`
Initialise une nouvelle instance de la classe `FolderEncryptor`.

- **Arguments** :
  - `key` (`bytes`) : L'empreinte utilisée pour le cryptage et le décryptage.

### `encrypt_file(self, file_path)`
Crypte un fichier en utilisant la clé de cryptage fournie.

- **Arguments** :
  - `file_path` (`str`) : Le chemin vers le fichier à crypter.

### `decrypt_file(self, file_path)`
Décrypte un fichier en utilisant la clé de cryptage fournie.

- **Arguments** :
  - `file_path` (`str`) : Le chemin vers le fichier à décrypter.

### `encrypt_folder(self, folder_path)`
Crypte tous les fichiers dans un dossier et ses sous-dossiers en utilisant la clé de cryptage fournie.

- **Arguments** :
  - `folder_path` (`str`) : Le chemin vers le dossier à crypter.

### `decrypt_folder(self, folder_path)`
Décrypte tous les fichiers dans un dossier et ses sous-dossiers en utilisant la clé de cryptage fournie.

- **Arguments** :
  - `folder_path` (`str`) : Le chemin vers le dossier à décrypter.

### `_encrypt_data(self, data)`
Crypte les données fournies en utilisant la clé de cryptage.

- **Arguments** :
  - `data` (`bytes`) : Les données à crypter.
- **Retourne** : `bytes` - Les données cryptées.

### `_decrypt_data(self, data)`
Décrypte les données fournies en utilisant la clé de cryptage.

- **Arguments** :
  - `data` (`bytes`) : Les données à décrypter.
- **Retourne** : `bytes` - Les données décryptées.


_______________________


# ViewOperations

## Description
Classe représentant les opérations de vue.

Cette classe gère les opérations de journalisation et d'affichage de messages dans l'interface utilisateur.

## Attributs
- **view** (`object`) : L'objet de la vue.
- **controller** (`object`) : L'objet du contrôleur.

## Méthodes

### `__init__(self, view, controller)`
Initialise une nouvelle instance de la classe `ViewOperations`.

- **Arguments** :
  - `view` (`object`) : L'objet de la vue.
  - `controller` (`object`) : L'objet du contrôleur.

### `log(self, message, log_type="info")`
Ajoute un message de journalisation à l'interface utilisateur.

- **Arguments** :
  - `message` (`str`) : Le message à ajouter.
  - `log_type` (`str`, optionnel) : Le type de journalisation. Par défaut, "info".

### `log_fingerprint_start(self)`
Journalise le début de la procédure de déverrouillage par empreinte digitale.

### `log_finger_time_remaining(self, time_remaining)`
Journalise le temps restant pour placer le doigt sur le capteur.

- **Arguments** :
  - `time_remaining` (`int`) : Le temps restant en secondes.

### `log_fingerprint_not_detected(self)`
Journalise l'absence de détection d'empreinte digitale sur le capteur.

### `log_enter_code_message(self)`
Journalise le message demandant à l'utilisateur d'entrer son code.

### `log_code_entered(self, code)`
Journalise la saisie du code par l'utilisateur.

- **Arguments** :
  - `code` (`str`) : Le code saisi.

### `log_code_correct(self)`
Journalise la confirmation que le code saisi est correct.

### `log_code_incorrect(self)`
Journalise l'erreur de saisie du code.

### `log_ip_address(self, ip_address)`
Journalise l'adresse IP de l'appareil.

- **Arguments** :
  - `ip_address` (`str`) : L'adresse IP de l'appareil.

### `log_folder_action(self, action)`
Journalise l'action en cours sur le dossier.

- **Arguments** :
  - `action` (`str`) : L'action en cours sur le dossier.

### `log_decrypting_done(self)`
Journalise la fin du décryptage du dossier.

### `log_encrypting_done(self)`
Journalise la fin du cryptage du dossier.

### `log_handle_fingerprint_match(self)`
Journalise la correspondance d'empreinte digitale trouvée.

### `log_handle_fingerprint_mismatch(self)`
Journalise l'absence de correspondance d'empreinte digitale.

### `log_samba_start(self)`
Journalise le démarrage du serveur Samba.

### `log_samba_stop(self)`
Journalise l'arrêt du serveur Samba.

### `log_samba_share_created(self, share_name, username, password)`
Journalise la création d'un partage Samba.

- **Arguments** :
  - `share_name` (`str`) : Le nom du partage.
  - `username` (`str`) : Le nom d'utilisateur.
  - `password` (`str`) : Le mot de passe.

### `log_samba_share_already_open(self, share_name, username, password)`
Journalise l'erreur de tentative d'ouverture d'un partage Samba déjà ouvert.

- **Arguments** :
  - `share_name` (`str`) : Le nom du partage.
  - `username` (`str`) : Le nom d'utilisateur.
  - `password` (`str`) : Le mot de passe.

### `log_you_cant_open(self)`
Journalise l'erreur de tentative d'ouverture d'un partage Samba lorsque le dossier est crypté.

### `log_decryption_already_done(self)`
Journalise l'erreur de tentative de décryptage d'un dossier déjà décrypté.

### `log_encryption_already_done(self)`
Journalise l'erreur de tentative de cryptage d'un dossier déjà crypté.

### `log_samba_share_already_closed(self)`
Journalise l'erreur de tentative de fermeture d'un partage Samba déjà fermé.

### `log_closing_sharing_for_encryption(self)`
Journalise la fermeture du partage Samba pour la gestion du cryptage.

### `show_file_chooser(self, action)`
Affiche le sélecteur de fichiers pour l'action donnée.

- **Arguments** :
  - `action` (`str`) : L'action pour laquelle afficher le sélecteur de fichiers.

### `log_start_app(self)`
Journalise le démarrage de l'application.


__________


# PasswordOperations

## Description
Classe utilitaire pour les opérations liées aux mots de passe.

## Attributs
Aucun attribut.

## Méthodes

### `verify_password_strength(password)`
Vérifie la force d'un mot de passe.

- **Arguments** :
  - `password` (`str`) : Le mot de passe à vérifier.
- **Retourne** : `bool` - `True` si le mot de passe est suffisamment fort, `False` sinon.

### `hash_password(password)`
Hache le mot de passe en utilisant l'algorithme SHA256.

- **Arguments** :
  - `password` (`str`) : Le mot de passe à hacher.
- **Retourne** : `str` - Le mot de passe haché.

### `verify_password(password, hashed_password)`
Vérifie si le mot de passe correspond au hachage.

- **Arguments** :
  - `password` (`str`) : Le mot de passe à vérifier.
  - `hashed_password` (`str`) : Le mot de passe haché.
- **Retourne** : `bool` - `True` si le mot de passe correspond au hachage, `False` sinon.



____________


# FingerprintActions

## Description
Cette classe gère les actions liées à l'empreinte digitale.

## Attributs
- **model** (`object`) : L'objet modèle utilisé pour les opérations liées à l'empreinte digitale.
- **view_ops** (`object`) : L'objet vue utilisé pour les opérations liées à l'interface utilisateur.
- **controller** (`object`) : L'objet contrôleur utilisé pour les opérations liées à la logique métier.
- **start_time** (`float`) : Le temps de démarrage de la vérification de l'empreinte digitale.
- **finger_detected** (`bool`) : Indique si une empreinte digitale a été détectée.

## Méthodes

### `__init__(self, model, view_ops, controller)`
Initialise une nouvelle instance de la classe `FingerprintActions`.

- **Arguments** :
  - `model` (`object`) : L'objet modèle utilisé pour les opérations liées à l'empreinte digitale.
  - `view_ops` (`object`) : L'objet vue utilisé pour les opérations liées à l'interface utilisateur.
  - `controller` (`object`) : L'objet contrôleur utilisé pour les opérations liées à la logique métier.

### `check_fingerprint(self, instance)`
Vérifie l'empreinte digitale pour l'authentification.

- **Arguments** :
  - `instance` (`object`) : L'instance de l'objet.

### `run_fingerprint_check(self, instance)`
Exécute le processus d'authentification par empreinte digitale.

- **Arguments** :
  - `instance` (`object`) : L'instance de l'objet.

### `check_finger(self, dt)`
Vérifie la présence d'un doigt sur le capteur.

- **Arguments** :
  - `dt` (`float`) : Le temps écoulé depuis la dernière vérification.
- **Retourne** : `bool` - `True` si la vérification doit continuer, `False` sinon.

### `_handle_fingerprint_timeout(self, finger_detected)`
Gère l'expiration du délai d'attente de l'empreinte digitale.

- **Arguments** :
  - `finger_detected` (`bool`) : Indique si une empreinte digitale a été détectée.

### `handle_fingerprint_match(self, id)`
Gère la correspondance de l'empreinte digitale avec un identifiant.

- **Arguments** :
  - `id` (`int`) : L'identifiant de l'empreinte digitale correspondante.

### `handle_fingerprint_mismatch(self)`
Gère l'absence de correspondance de l'empreinte digitale.


__________


# FileOperations

## Description
Classe qui représente les opérations de fichiers.

Cette classe permet de chiffrer et déchiffrer des dossiers en utilisant l'empreinte digitale comme clé d'encryption.

## Attributs
- **view_ops** : Vue principale de l'application.
- **controller** : Contrôleur de l'empreinte digitale.

## Méthodes

### `__init__(self, view_ops, controller)`
Initialise une nouvelle instance de la classe `FileOperations`.

- **Arguments** :
  - `view_ops` (`object`) : Vue principale de l'application.
  - `controller` (`object`) : Contrôleur de l'empreinte digitale.

### `encrypt_folder(self, folder_path)`
Encrypte un dossier en utilisant l'empreinte digitale.

- **Arguments** :
  - `folder_path` (`str`) : Chemin du dossier à encrypter.

### `decrypt_folder(self, folder_path)`
Décrypte un dossier en utilisant l'empreinte digitale.

- **Arguments** :
  - `folder_path` (`str`) : Chemin du dossier à décrypter.

### `_perform_folder_encryption(self, folder_path)`
Effectue le chiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.

- **Arguments** :
  - `folder_path` (`str`) : Chemin du dossier à encrypter.

### `_perform_folder_decryption(self, folder_path)`
Effectue le déchiffrement du dossier en utilisant une clé générée à partir de l'empreinte digitale.

- **Arguments** :
  - `folder_path` (`str`) : Chemin du dossier à décrypter.

### `_generate_encryption_key(self)`
Génère une clé d'encryption à partir de l'empreinte digitale.

- **Retourne** : `bytes` - Clé d'encryption générée.
