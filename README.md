Instructions pour utiliser l'application de transcription audio
================================================================

Cette application utilise Whisper, un modèle d'OpenAI pour la transcription audio. 
Voici comment installer et configurer l'application, ainsi que deux méthodes pour récupérer les modèles nécessaires.

1. Télécharger le dépôt GitHub
---------------------------------
Pour commencer, récupérez le projet depuis GitHub :

- Allez sur la page du dépôt GitHub.
- Cliquez sur le bouton vert "Code", puis sur "Download ZIP".
- Une fois le téléchargement terminé, décompressez l'archive ZIP dans un dossier de votre choix.

Pour télécharger directement l'exécutable précompilé, utilisez le lien suivant :
[Whisper_App.exe sur Google Drive](https://drive.google.com/file/d/1ex8Y1h1wlVRBy5Zid6ETFGmlHwXN9-R4/view?usp=drive_link)

2. Récupération des modèles nécessaires
------------------------------------------
L'application Whisper nécessite des modèles pré-entraînés pour fonctionner. Vous pouvez les obtenir de deux façons :

OPTION 1 : Télécharger depuis Google Drive
    - Rendez-vous sur le lien suivant : [Models sur Google Drive](https://drive.google.com/drive/folders/1RCqBgtcg_dw6Hbhca59ufit_4QOXk94X?usp=drive_link)
    - Téléchargez les fichiers suivants :
        - tiny.pt
        - base.pt
        - small.pt
    - Placez les fichiers téléchargés dans le dossier `models/` à côté de l'exécutable (Whisper_App.exe). 
      Si le dossier `models/` n'existe pas, créez-le manuellement.

OPTION 2 : Utiliser le script `Download_models.py`
    - Le script Python `Download_models.py`, situé dans le dossier `source`, permet de télécharger les modèles automatiquement.
    - Instructions :
        1. Assurez-vous que Python 3 et Whisper sont installés :
           pip install openai-whisper
        2. Accédez au dossier `source` où se trouve le script :
           cd source
        3. Lancez le script :
           python Download_models.py
    - Les modèles téléchargés seront placés dans le dossier `models/`.

3. Organisation des fichiers
-----------------------------
Pour que l'application fonctionne correctement, assurez-vous que votre dossier est organisé comme suit :

Whisper_Transcript/
├── Whisper_App.exe
├── models/
│   ├── tiny.pt
│   ├── base.pt
│   ├── small.pt
├── source/
│   ├── Download_models.py
│   ├── transcription_app.py
├── examples/
├── resources/
├── README

4. Utilisation de l'application
-------------------------------
Étapes :
1. Double-cliquez sur `Whisper_App.exe` pour lancer l'application.
2. Cliquez sur "Sélectionner des fichiers audio" et choisissez les fichiers à transcrire (.mp3, .wav, .flac).
3. Configurez les paramètres :
    - Modèle Whisper (tiny, base, small).
    - Langue (Français ou Anglais).
4. Lancez la transcription en cliquant sur "Lancer la transcription".
5. Les fichiers transcrits seront enregistrés dans le dossier `transcriptions`.

Remarque importante :
    - Le modèle à utiliser dépend de vos besoins :
        - tiny.pt : Plus rapide mais moins précis.
        - base.pt : Bon équilibre entre rapidité et précision.
        - small.pt : Plus précis mais plus lent.

Si vous avez des questions ou des problèmes, consultez la documentation officielle de Whisper ou ouvrez une issue sur GitHub.
