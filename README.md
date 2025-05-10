# Guide d'installation et d'utilisation de Whisper App

Whisper App utilise **Whisper**, un modèle d'OpenAI pour la transcription audio. Voici comment installer et configurer l'application, ainsi que deux méthodes pour obtenir les modèles nécessaires.
Cette application a été réalisée avec l'aide du tutoriel écrit par le CNRS a destination des chercheurs en sciences humaines qui réalisent des entretiens **_[CNRS Tutoriel][1]_**.

> *L'application a été testée sur un ordinateur équipé d’un Intel Core i5-9300H, de 16 Go de RAM et d’un GPU NVIDIA GeForce GTX 1650.  
> Les performances peuvent varier selon la configuration de votre machine.*

---

## Installation de l'application

Pour commencer, téléchargez le projet depuis GitHub :

1. Rendez-vous sur la page du dépôt GitHub.
2. Cliquez sur le bouton vert **Code**, puis sélectionnez **Download ZIP**.
3. Une fois le téléchargement terminé, **décompressez l'archive ZIP** dans un dossier de votre choix.

Pour télécharger directement l'exécutable précompilé, utilisez le lien suivant :
**[Whisper\_App.exe sur Google Drive](https://drive.google.com/file/d/1ex8Y1h1wlVRBy5Zid6ETFGmlHwXN9-R4/view?usp=drive_link)**

---

## Récupération des modèles nécessaires

L'application Whisper nécessite des modèles préentraînés pour fonctionner. Vous pouvez les obtenir de deux façons :

### Option 1 : Télécharger depuis Google Drive

1. Accédez au lien suivant : **[Models sur Google Drive](https://drive.google.com/drive/folders/1RCqBgtcg_dw6Hbhca59ufit_4QOXk94X?usp=drive_link)**
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

## Organisation des fichiers

Pour que l'application fonctionne correctement, assurez-vous que votre dossier est organisé comme suit :

```
WHISPER_APP/
├── examples/
├── models/
│   ├── base.pt
│   ├── small.pt
│   ├── tiny.pt
│   ├── README.md
├── resources/
├── source/
├── transcriptions/
├── LICENSE
├── README.md
```

---

## Utilisation de l'application

### Tester avec des fichiers d'exemple

Vous pouvez tester l'application avec les fichiers audio déjà disponibles dans le dossier `examples/`.

### Lancer l'application

1. **Lancer l'application**
   - Double-cliquez sur `Whisper_App.exe` pour ouvrir l'application.
2. **Sélectionner des fichiers audio**
   - Cliquez sur **"Sélectionner des fichiers audio"** et choisissez les fichiers que vous souhaitez transcrire (formats supportés : `.mp3`, `.wav`, `.flac`).
3. **Configurer les paramètres**
   - Sélectionnez le **modèle Whisper** que vous souhaitez utiliser (`tiny`, `base`, `small`).
   > *Note importante : Il existe d'autres modèles plus puissants (`medium` et `large`) qui sont disponibles à cette addresse : [Medium Model sur HuggingFace](https://huggingface.co/openai/whisper-medium) et  [Large_V3 Model sur HuggingFace](https://huggingface.co/openai/whisper-large-v3)* 
   - Choisissez la **langue** de l'audio (également supporté : Français ou Anglais).
4. **Lancer la transcription**
   - Cliquez sur **"Lancer la transcription"** pour démarrer le processus. L'application affichera l'état de la transcription et ouvrira les fichiers texte générés une fois terminée.
5. **Récupérer les transcriptions**
   - Les fichiers transcrits seront sauvegardés dans le dossier `transcriptions/`, qui sera automatiquement créé à côté de l'exécutable.

---

## Choisir le bon modèle

- **`tiny.pt`** : Modèle rapide, mais moins précis.
- **`base.pt`** : Bon équilibre entre rapidité et précision.
- **`small.pt`** : Modèle plus précis, mais plus lent.

Le choix du modèle dépend de vos besoins : si vous avez besoin d'une transcription rapide, utilisez `tiny.pt`, mais pour des résultats de meilleure qualité, `small.pt` est recommandé.

---

## Activer l'accélération GPU (CUDA)

Si votre ordinateur est équipé d'une **carte graphique NVIDIA**, vous pouvez bénéficier de l'accélération matérielle via **CUDA** pour accélérer considérablement les transcriptions avec Whisper App.

### Étapes pour activer CUDA avec PyTorch

1. **Vérifiez la compatibilité CUDA de votre GPU**  
   Consultez la liste officielle ici :  
     [https://developer.nvidia.com/cuda-gpus](https://developer.nvidia.com/cuda-gpus)

2. **Installez les derniers pilotes NVIDIA**  
   Téléchargez les drivers appropriés pour votre carte graphique :  
     [https://www.nvidia.fr/Download/index.aspx](https://www.nvidia.fr/Download/index.aspx)

3. **Installez PyTorch avec le support CUDA**  
   Rendez-vous sur la page d'installation :  
     [https://pytorch.org/get-started/locally](https://pytorch.org/get-started/locally)  
   Sélectionnez les options suivantes :
   - **OS** : Windows  
   - **Package** : pip  
   - **Language** : Python  
   - **Compute Platform** : CUDA (choisissez **11.8** si vous avez une GeForce GTX 1060, 1650, etc.)

   Ou installez directement via cette commande recommandée :
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

---
## Résultats de test

L’application a été testée à partir de l'enregistrement de l’appel du 18 juin du général de Gaulle (version diffusée le 22 juin), en utilisant deux modèles différents afin de comparer leur précision. L’évaluation a été réalisée avec la bibliothèque Jiwer **_[Morris et al., 2004][2]_**, permettant une analyse fine entre la transcription de référence et celle générée par Whisper.
Le discours comporte 1 191 mots pour une durée totale d’environ 5 minutes et 50 secondes, ce qui constitue un bon support pour mesurer les performances de transcription automatique.

### Résultat avec le modèle `tiny.pt`

| **Indicateur**                         | **Valeur**            | **Interprétation**                                                                          |
| -------------------------------------- | --------------------- | ------------------------------------------------------------------------------------------- |
| **WER** (Word Error Rate)            | **41,65 %**            | Élevé : près d’un mot sur deux comporte une erreur (substitution, insertion ou suppression). |
| **MER** (Match Error Rate)           | **37,20 %**            | Confirme que plus d’un mot sur trois est incorrectement transcrit.                          |
| **WIL** (Word Information Lost)      | **55,52 %**            | Plus de la moitié de l'information est mal restituée.                                       |
| **WIP** (Word Information Preserved) | **44,48 %**            | Moins de la moitié du contenu a été correctement conservé.                                  |
| **Substitutions**                   | **140 mots**           | Beaucoup de mots mal reconnus.                                                              |
| **Insertions**                      | **58 mots**            | Ajouts de mots non prononcés.                                                               |
| **Suppressions**                    | **4 mots**             | Mots manquants ou ignorés par le modèle.                                                    |

---

### Résultat avec le modèle `small.pt`

| **Indicateur**                         | **Valeur**            | **Interprétation**                                                                           |
| -------------------------------------- | --------------------- | -------------------------------------------------------------------------------------------- |
| **WER** (Word Error Rate)            | **3,92 %**             | Excellent taux d'erreur. En dessous de 5 %, on considère la transcription comme très fidèle. |
| **MER** (Match Error Rate)           | **3,90 %**             | Proportion d’erreurs sur l’ensemble des mots.                                                |
| **WIL** (Word Information Lost)      | **7,27 %**             | Faible perte d’information globale.                                                          |
| **WIP** (Word Information Preserved) | **92,73 %**            | Indique que la quasi-totalité du contenu a été bien retranscrit.                             |
| **Substitutions**                   | **17 mots**            | Exemple : “bon **sang**” au lieu de “bon **sens**”.                                          |
| **Insertions**                      | **2 mots**             | Ex. : “indépendant” à la fin au lieu de “indépendance”.                                      |
| **Suppressions**                    | **0 mot**              | Aucun mot manquant détecté.                                                                  |

---

## Conclusion

Le modèle `small.pt` a permis d’atteindre **92,7 % de transcription correcte**, contre seulement **44,5 %** avec le modèle `tiny.pt`.

Dans le cadre d’entretiens contenant des informations confidentielles ou sensibles, l’application **garantit la sécurité des données** :  
- Aucune donnée audio ou texte n’est envoyée en ligne.  
- L’intégralité du traitement est réalisée **en local**, sur la machine de l’utilisateur.  
- Aucun transfert vers des services cloud ou des tiers n’est effectué, assurant ainsi la **conformité RGPD** et la confidentialité des échanges.
- 


## Réferences 

[1] CNRS. *[Tutorial] Whisper pour retranscrire des entretiens.* https://www.css.cnrs.fr/fr/whisper-pour-retranscrire-des-entretiens/

[2] Andrew C. Morris, Viktoria Maier, and Phil Green. *From WER and RIL to MER and WIL: improved evaluation measures for connected speech recognition*. In Proceedings of Interspeech 2004. DOI: [10.21437/Interspeech.2004-668](https://doi.org/10.21437/Interspeech.2004-668)
