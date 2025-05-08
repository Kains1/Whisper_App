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

# Force l'utilisation du CPU uniquement pour PyTorch
def verifier_disponibilite_device():
    return "cpu"

# Fonction pour obtenir le chemin absolu
def get_absolute_path(relative_path):
    if getattr(sys, 'frozen', False):  # Si le script est empaqueté en exécutable
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# Fonction principale pour la transcription
def transcrire_audio(dossier_transcriptions, modele, langue, fichiers, callback=None):
    device = verifier_disponibilite_device()
    if callback:
        callback(f"Utilisation du périphérique : {device}")

    # Spécifiez le chemin d'accès local pour charger le modèle
    models_path = get_absolute_path("models")
    model_path = os.path.join(models_path, f"{modele}.pt")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Le modèle {modele} est introuvable dans {models_path}.")

    if callback:
        callback(f"Chargement du modèle {modele} depuis : {model_path}")

    # Charger le modèle depuis le fichier local
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
                for segment in result["segments"]:
                    start = segment["start"]
                    end = segment["end"]
                    text = segment["text"]
                    start_time = f"{int(start // 3600):02}:{int((start % 3600) // 60):02}:{int(start % 60):02}"
                    end_time = f"{int(end // 3600):02}:{int((end % 3600) // 60):02}:{int(end % 60):02}"
                    f.write(f"[{start_time} - {end_time}] {text}\n")

            if callback:
                callback(f"✅ Transcription terminée pour : {os.path.basename(fichier)}")
        except Exception as e:
            if callback:
                callback(f"❌ Erreur lors de la transcription de {os.path.basename(fichier)} : {e}")

    if callback:
        callback(f"📁 Toutes les transcriptions sont sauvegardées dans : {dossier_transcriptions}")

# Thread pour la transcription
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

# Interface principale de l'application
class TranscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Transcription Audio avec Whisper")
        self.setGeometry(300, 100, 600, 600)
        self.setWindowIcon(QIcon("resources/icons/app.ico"))
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.instructions_label = QLabel(
            "1: Sélectionnez les fichiers audio.\n2: Configurez les paramètres.\n3: Lancez la transcription.")
        layout.addWidget(self.instructions_label)

        self.cuda_status_label = QLabel("❌ CUDA non détecté : CPU utilisé.")
        self.cuda_status_label.setStyleSheet("color: red;")
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
                subprocess.Popen(["start", "", file], shell=True)  # Windows 11 ouvrira le lecteur par défaut
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de lire le fichier audio : {e}")

    def start_transcription(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Avertissement", "Aucun fichier sélectionné.")
            return

        model = self.model_combobox.currentText()
        selected_language = self.language_combobox.currentText()
        language_code = "fr" if selected_language == "Français" else "en"

        output_folder = os.path.join(os.getcwd(), "transcriptions")
        os.makedirs(output_folder, exist_ok=True)

        self.thread = TranscriptionThread(self.selected_files, output_folder, model, language_code)
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
