# Instructions pour utiliser l'application de transcription audio

## 1. Télécharger le dépôt GitHub
Pour utiliser l'application, commencez par télécharger le dépôt GitHub. Voici comment faire :

- Allez sur la page du dépôt GitHub (lien fourni).
- Cliquez sur le bouton vert **Code**, puis sur **Download ZIP**.
- Une fois le téléchargement terminé, **décompressez l'archive ZIP** dans un dossier de votre choix sur votre ordinateur.

## 2. Organisation des fichiers
Pour que l'application fonctionne correctement, assurez-vous que votre dossier est organisé comme suit :

- **Le dossier principal** contient :
  - `Whisper_App.exe`
  - Le dossier `models/` (déjà inclus dans le dépôt)
    - `tiny.pt`
    - `base.pt`
    - `small.pt`
  - Les autres fichiers et dossiers extraits du dépôt GitHub

## 3. Utilisation de l'application

1. **Essayer sur des fichiers d'exemple** :
   - Vous pouvez tester l'application avec des fichiers audio déjà disponibles dans le dossier `examples`.

2. **Lancer l'application** :
   - Double-cliquez sur `Whisper_App.exe` pour lancer l'application.

2. **Sélectionner les fichiers audio** :
   - Cliquez sur le bouton **"Sélectionner des fichiers audio"** et choisissez les fichiers que vous souhaitez transcrire (formats supportés : `.mp3`, `.wav`, `.flac`).

3. **Configurer les paramètres** :
   - Sélectionnez le **modèle Whisper** que vous souhaitez utiliser (`tiny`, `base`, `small`).
   - Choisissez la **langue** de l'audio (Français ou Anglais).

4. **Lancer la transcription** :
   - Cliquez sur **"Lancer la transcription"** pour démarrer le processus.
   - L'application affichera l'état de la transcription et ouvrira les fichiers texte générés une fois terminée.

5. **Transcriptions** :
   - Les fichiers transcrits seront sauvegardés dans le dossier `transcriptions` qui sera automatiquement créé à côté de l'exécutable.

N'hésitez pas à suivre ces instructions étape par étape, et tout devrait bien fonctionner pour vous permettre de transcrire vos fichiers audio facilement.

