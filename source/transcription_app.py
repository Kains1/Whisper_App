import os
import sys
import torch
import whisper
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QFileDialog, QLabel, QWidget,
    QCheckBox, QScrollArea, QHBoxLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal


def get_absolute_path(relative_path):
    if getattr(sys, 'frozen', False):  # Si le script est empaqueté en exécutable
        # Utilise le répertoire de l'exécutable
        base_path = os.path.dirname(sys.executable)
    else:
        # Utilise le répertoire du script actuel
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

def verifier_disponibilite_device():
    return "cuda" if torch.cuda.is_available() else "cpu"


def transcrire_audio(dossier_transcriptions, modele, langue, fichiers, callback=None):
    device = verifier_disponibilite_device()
    if callback:
        callback(f"Utilisation du périphérique : {device}")

    models_path = get_absolute_path("models")
    model_path = os.path.join(models_path, f"{modele}.pt")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Le modèle {modele} est introuvable dans {models_path}.")

    if callback:
        callback(f"Chargement du modèle {modele} depuis : {model_path}")
    model = whisper.load_model(model_path, device=device)

    os.makedirs(dossier_transcriptions, exist_ok=True)

    for fichier in fichiers:
        if callback:
            callback(f"Transcription en cours : {os.path.basename(fichier)}")
        try:
            result = model.transcribe(fichier, language=langue)
            fichier_texte = os.path.splitext(os.path.basename(fichier))[0] + ".txt"
            chemin_transcription = os.path.join(dossier_transcriptions, fichier_texte)

            with open(chemin_transcription, "w", encoding="utf-8") as f:
                f.write(result["text"])

            if callback:
                callback(f"✅ Transcription terminée pour : {os.path.basename(fichier)}")
        except Exception as e:
            if callback:
                callback(f"❌ Erreur lors de la transcription de {os.path.basename(fichier)} : {e}")

    if callback:
        callback(f"📁 Toutes les transcriptions sont sauvegardées dans : {dossier_transcriptions}")


class TranscriptionThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(list)

    def __init__(self, fichiers, dossier_transcriptions, modele, langue):
        super().__init__()
        self.fichiers = fichiers
        self.dossier_transcriptions = dossier_transcriptions
        self.modele = modele
        self.langue = langue

    def run(self):
        fichiers_transcrits = []
        try:
            def callback(message):
                self.progress.emit(message)

            transcrire_audio(
                dossier_transcriptions=self.dossier_transcriptions,
                modele=self.modele,
                langue=self.langue,
                fichiers=self.fichiers,
                callback=callback
            )
            for fichier in self.fichiers:
                fichier_texte = os.path.splitext(os.path.basename(fichier))[0] + ".txt"
                chemin_transcription = os.path.join(self.dossier_transcriptions, fichier_texte)
                fichiers_transcrits.append(chemin_transcription)
        except Exception as e:
            self.progress.emit(f"❌ Erreur : {e}")
        finally:
            self.finished.emit(fichiers_transcrits)


class TranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transcription Audio avec Whisper")
        self.setGeometry(300, 100, 600, 600)
        self.setWindowIcon(QIcon("resources/icons/app.ico"))
        
        # Vérification du dossier models au lancement
        if not self.verifier_dossier_models_on_start():
            sys.exit(1)  # Quitte l'application si le dossier models est absent

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.instructions_label = QLabel(
            "1: Sélectionnez les fichiers audio.\n2: Configurez les paramètres.\n3: Lancez la transcription.")
        layout.addWidget(self.instructions_label)

        self.cuda_status_label = QLabel()
        self.check_cuda_availability()
        layout.addWidget(self.cuda_status_label)

        self.select_files_button = QPushButton("Sélectionner des fichiers audio")
        self.select_files_button.setIcon(QIcon("resources/icons/folder.png"))
        self.select_files_button.clicked.connect(self.select_audio_files)
        layout.addWidget(self.select_files_button)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.file_list_widget = QWidget()
        self.file_list_layout = QVBoxLayout(self.file_list_widget)
        self.scroll_area.setWidget(self.file_list_widget)
        layout.addWidget(self.scroll_area)

        buttons_layout = QHBoxLayout()
        self.select_all_button = QPushButton("Tout sélectionner")
        self.select_all_button.clicked.connect(self.select_all_files)
        buttons_layout.addWidget(self.select_all_button)

        self.deselect_all_button = QPushButton("Tout désélectionner")
        self.deselect_all_button.clicked.connect(self.deselect_all_files)
        buttons_layout.addWidget(self.deselect_all_button)
        layout.addLayout(buttons_layout)

        self.remove_files_button = QPushButton("Supprimer les fichiers sélectionnés")
        self.remove_files_button.clicked.connect(self.remove_selected_files)
        layout.addWidget(self.remove_files_button)

        # Ajout du bouton pour jouer le fichier audio
        self.play_audio_button = QPushButton("Jouer le fichier audio")
        self.play_audio_button.clicked.connect(self.play_audio_file)
        layout.addWidget(self.play_audio_button)

        self.model_label = QLabel("Modèle Whisper :")
        layout.addWidget(self.model_label)
        self.model_combobox = QComboBox()
        self.model_combobox.addItems(["tiny", "base", "small"])
        layout.addWidget(self.model_combobox)

        self.language_label = QLabel("Langue :")
        layout.addWidget(self.language_label)
        self.language_combobox = QComboBox()
        self.language_combobox.addItems(["Français", "Anglais"])
        layout.addWidget(self.language_combobox)

        self.transcription_button = QPushButton("Lancer la transcription")
        self.transcription_button.clicked.connect(self.start_transcription)
        layout.addWidget(self.transcription_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.selected_files = []

# Ajout de la méthode pour jouer un fichier audio avec le lecteur par défaut de Windows 11
    def play_audio_file(self):
        selected_files = [
            self.file_list_layout.itemAt(i).widget().toolTip()
            for i in range(self.file_list_layout.count())
            if isinstance(self.file_list_layout.itemAt(i).widget(), QCheckBox) and
            self.file_list_layout.itemAt(i).widget().isChecked()
        ]

        if not selected_files:
            QMessageBox.warning(self, "Avertissement", "Aucun fichier sélectionné pour la lecture.")
            return

        for file in selected_files:
            try:
                # Utilise "start" pour ouvrir avec le lecteur multimédia par défaut
                subprocess.Popen(["start", "", file], shell=True)  # Windows 11 ouvrira le lecteur par défaut
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier audio : {e}")

    def check_cuda_availability(self):
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            self.cuda_status_label.setText(f"✅ CUDA détecté : {gpu_name}.")
            self.cuda_status_label.setStyleSheet("color: green;")
        else:
            self.cuda_status_label.setText("❌ CUDA non détecté : CPU utilisé.")
            self.cuda_status_label.setStyleSheet("color: red;")

    def verifier_dossier_models_on_start(self):
        """Vérifie au lancement de l'application que le dossier models existe."""
        models_path = get_absolute_path("models")
        if not os.path.exists(models_path):
            QMessageBox.critical(
                self,
                "Erreur critique",
                "Le dossier 'models' est introuvable.\n"
                "Veuillez le placer dans le même répertoire que l'exécutable avant de relancer l'application."
            )
            return False
        return True
    
    def verifier_dossier_models(self):
        models_path = get_absolute_path("models")
        if not os.path.exists(models_path):
            QMessageBox.critical(self, "Erreur", "Le dossier 'models' est introuvable. "
                                                 "Veuillez le placer dans le même répertoire que l'exécutable.")
            return False

        modele = self.model_combobox.currentText()
        model_path = os.path.join(models_path, f"{modele}.pt")
        if not os.path.exists(model_path):
            QMessageBox.critical(self, "Erreur", f"Le modèle '{modele}.pt' est introuvable dans le dossier 'models'.")
            return False

        return True

    def select_audio_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Sélectionner des fichiers audio", "", "Fichiers audio (*.mp3 *.wav *.flac)")
        if files:
            self.selected_files = files
            self.update_file_list()

    def update_file_list(self):
        for i in reversed(range(self.file_list_layout.count())):
            widget = self.file_list_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for file in self.selected_files:
            checkbox = QCheckBox(os.path.basename(file))
            checkbox.setToolTip(file)
            checkbox.setChecked(True)
            self.file_list_layout.addWidget(checkbox)

    def select_all_files(self):
        for i in range(self.file_list_layout.count()):
            checkbox = self.file_list_layout.itemAt(i).widget()
            if isinstance(checkbox, QCheckBox):
                checkbox.setChecked(True)

    def deselect_all_files(self):
        for i in range(self.file_list_layout.count()):
            checkbox = self.file_list_layout.itemAt(i).widget()
            if isinstance(checkbox, QCheckBox):
                checkbox.setChecked(False)

    def remove_selected_files(self):
        self.selected_files = [
            self.file_list_layout.itemAt(i).widget().toolTip()
            for i in range(self.file_list_layout.count())
            if isinstance(self.file_list_layout.itemAt(i).widget(), QCheckBox) and
            not self.file_list_layout.itemAt(i).widget().isChecked()
        ]
        self.update_file_list()

    def start_transcription(self):
        if not self.verifier_dossier_models():
            return

        files_to_transcribe = [
            self.file_list_layout.itemAt(i).widget().toolTip()
            for i in range(self.file_list_layout.count())
            if isinstance(self.file_list_layout.itemAt(i).widget(), QCheckBox) and
            self.file_list_layout.itemAt(i).widget().isChecked()
        ]

        if not files_to_transcribe:
            QMessageBox.warning(self, "Avertissement", "Aucun fichier sélectionné.")
            return

        model = self.model_combobox.currentText()
        selected_language = self.language_combobox.currentText()
        language_code = "fr" if selected_language == "Français" else "en"

        output_folder = os.path.join(os.getcwd(), "transcriptions")
        os.makedirs(output_folder, exist_ok=True)

        self.thread = TranscriptionThread(files_to_transcribe, output_folder, model, language_code)
        self.thread.progress.connect(self.update_status)
        self.thread.finished.connect(self.on_transcription_finished)
        self.status_label.setText("🚀 Transcription démarrée...")
        self.thread.start()

    def update_status(self, message):
        self.status_label.setText(message)

    def on_transcription_finished(self, fichiers_transcrits):
        self.status_label.setText("✅ Transcription terminée.")
        for fichier in fichiers_transcrits:
            try:
                subprocess.Popen(["notepad.exe", fichier])
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le fichier : {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TranscriptionApp()
    window.show()
    sys.exit(app.exec_())
