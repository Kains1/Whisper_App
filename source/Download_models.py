import os
import shutil
import whisper

# Chemin vers le dossier où tu veux sauvegarder les modèles
models_dir = "models/"

# Crée le dossier s'il n'existe pas
os.makedirs(models_dir, exist_ok=True)

# Liste des modèles à télécharger
models_to_download = ["tiny", "base", "small"]

for model_name in models_to_download:
    print(f"Téléchargement du modèle {model_name}...")
    model = whisper.load_model(model_name)  # Télécharge le modèle
    cache_path = os.path.expanduser("~/.cache/whisper")  # Chemin par défaut des fichiers téléchargés
    model_file = os.path.join(cache_path, f"{model_name}.pt")
    
    # Copie le fichier téléchargé dans ton dossier "models"
    if os.path.exists(model_file):
        shutil.copy(model_file, os.path.join(models_dir, f"{model_name}.pt"))
        print(f"{model_name}.pt sauvegardé dans {models_dir}")
    else:
        print(f"Erreur : {model_name}.pt introuvable dans le cache !")
