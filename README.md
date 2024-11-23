# Guide d'installation et d'utilisation de Whisper App

Whisper App utilise **Whisper**, un modèle d'OpenAI pour la transcription audio. Voici comment installer et configurer l'application, ainsi que deux méthodes pour obtenir les modèles nécessaires.

---

## 💻 Installation de l'application

Pour commencer, téléchargez le projet depuis GitHub :

1. Rendez-vous sur la page du dépôt GitHub.
2. Cliquez sur le bouton vert **Code**, puis sélectionnez **Download ZIP**.
3. Une fois le téléchargement terminé, **décompressez l'archive ZIP** dans un dossier de votre choix.

Pour télécharger directement l'exécutable précompilé, utilisez le lien suivant :
[**Whisper_App.exe sur Google Drive**](https://drive.google.com/file/d/1ex8Y1h1wlVRBy5Zid6ETFGmlHwXN9-R4/view?usp=drive_link)

---

## 🛠️ Récupération des modèles nécessaires

L'application Whisper nécessite des modèles préentraînés pour fonctionner. Vous pouvez les obtenir de deux façons :

### Option 1 : Télécharger depuis Google Drive

1. Accédez au lien suivant : [**Models sur Google Drive**](https://drive.google.com/drive/folders/1RCqBgtcg_dw6Hbhca59ufit_4QOXk94X?usp=drive_link)
2. Téléchargez les fichiers suivants :
   - `tiny.pt`
   - `base.pt`
   - `small.pt`
3. Placez les fichiers téléchargés dans le dossier `models/` à côté de l'exécutable (`Whisper_App.exe`). Si le dossier `models/` n'existe pas, créez-le manuellement.

### Option 2 : Utiliser le script Python `Download_models.py`

1. Le script Python `Download_models.py`, situé dans le dossier `source`, permet de télécharger les modèles automatiquement.
2. Instructions :
   - Assurez-vous d'avoir **Python 3** et **Whisper** installés :
     ```bash
     pip install openai-whisper
     ```
   - Accédez au dossier `source` :
     ```bash
     cd source
     ```
   - Lancez le script :
     ```bash
     python Download_models.py
     ```
3. Les modèles téléchargés seront placés dans le dossier `models/`.

Note : Une version future intègrera un bouton pour télécharger automatiquement les modèles dès le lancement de l'application.
---

## 📁 Organisation des fichiers

Pour que l'application fonctionne correctement, assurez-vous que votre dossier est organisé comme suit :

```
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
└── README
```

---

## 🔢 Utilisation de l'application

### 🔎 Tester avec des fichiers d'exemple
Vous pouvez tester l'application avec les fichiers audio déjà disponibles dans le dossier `examples/`.

### 🛠️ Lancer l'application

1. **Lancer l'application**
   - Double-cliquez sur `Whisper_App.exe` pour ouvrir l'application.
2. **Sélectionner des fichiers audio**
   - Cliquez sur **"Sélectionner des fichiers audio"** et choisissez les fichiers que vous souhaitez transcrire (formats supportés : `.mp3`, `.wav`, `.flac`).
3. **Configurer les paramètres**
   - Sélectionnez le **modèle Whisper** que vous souhaitez utiliser (`tiny`, `base`, `small`).
   - Choisissez la **langue** de l'audio (également supporté : Français ou Anglais).
4. **Lancer la transcription**
   - Cliquez sur **"Lancer la transcription"** pour démarrer le processus. L'application affichera l'état de la transcription et ouvrira les fichiers texte générés une fois terminée.
5. **Récupérer les transcriptions**
   - Les fichiers transcrits seront sauvegardés dans le dossier `transcriptions/`, qui sera automatiquement créé à côté de l'exécutable.

---

## 🚀 Choisir le bon modèle

- **`tiny.pt`** : Modèle rapide, mais moins précis.
- **`base.pt`** : Bon équilibre entre rapidité et précision.
- **`small.pt`** : Modèle plus précis, mais plus lent.

Le choix du modèle dépend de vos besoins : si vous avez besoin d'une transcription rapide, utilisez `tiny.pt`, mais pour des résultats de meilleure qualité, `small.pt` est recommandé.

---

