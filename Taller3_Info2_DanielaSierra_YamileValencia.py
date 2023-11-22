# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 16:33:36 2023

@author: Yami
"""

import os
import sys
import unicodedata
from pydicom import dcmread
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QSlider,
    QMessageBox,
    QVBoxLayout,
    QMainWindow,
    QDialog,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QComboBox,
)
from PyQt5.QtGui import QPalette, QColor
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MedVisLogin(QDialog):
    def __init__(self, parent=None):
        super(MedVisLogin, self).__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MedVis Login")

        # Crear y configurar layout
        layout = QVBoxLayout(self)

        # Crear widgets
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Usuario")
        self.password = QLineEdit(self)
        self.password.setPlaceholderText("Contraseña")
        self.password.setEchoMode(QLineEdit.Password)
        self.loginButton = QPushButton("Login", self)
        self.loginButton.clicked.connect(self.check_credentials)

        # Añadir widgets al layout
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.loginButton)

    def check_credentials(self):
        # Normalizar y remover diacríticos (tildes, etc.)
        normalized_username = self.normalize_string(self.username.text())
        normalized_correct_username = self.normalize_string("medicoAnalítico")

        if (
            normalized_username == normalized_correct_username
            and self.password.text() == "bio12345"
        ):
            self.accept()
        else:
            self.show_error("Usuario o contraseña incorrectos")

    def normalize_string(self, input_str):
        # Remueve diacríticos (tildes, etc.)
        nfkd_form = unicodedata.normalize("NFKD", input_str)
        only_ascii = nfkd_form.encode("ASCII", "ignore")
        return only_ascii.decode("ASCII")

    def show_error(self, message):
        QMessageBox.warning(self, "Error", message)


class MedVisDicomModel:
    def __init__(self):
        self.dicom_files = []
        self.current_image_index = 0

    def get_current_image(self):
        # Retorna la imagen DICOM actual basada en el índice actual
        return (
            self.dicom_files[self.current_image_index]
            if self.dicom_files
            else None
        )

    def load_dicom_folder(self, path):
        for filename in os.listdir(path):
            if filename.endswith(".dcm"):
                # Usa dcmread para leer el archivo DICOM
                dicom_path = os.path.join(path, filename)
                self.dicom_files.append(dcmread(dicom_path))
        self.dicom_files.sort(key=lambda x: x.InstanceNumber)  # Asegurarse de que están en orden


class MedVisDicomViewer(QWidget):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.cmap_combobox = None  # Nuevo: ComboBox para elegir el mapa de colores
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Agregar ComboBox para elegir mapa de colores
        self.cmap_combobox = QComboBox(self)
        self.cmap_combobox.addItems(['viridis', 'inferno', 'plasma', 'magma', 'cividis', 'twilight'])
        self.cmap_combobox.currentIndexChanged.connect(self.update_image)

        # El slider determina la imagen actual que se muestra
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.valueChanged[int].connect(self.slider_changed)

        # Añadir el canvas de Matplotlib, el slider y el ComboBox al layout
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        layout.addWidget(self.cmap_combobox)

        self.setLayout(layout)

    def slider_changed(self, value):
        # Cambiar la imagen mostrada al valor actual del slider
        self.model.current_image_index = value
        self.update_image()

    def update_image(self):
        # Asegurarse de que hay una imagen para mostrar
        dicom_files_exist = bool(self.model.dicom_files)
        if dicom_files_exist:
            dicom_image = self.model.get_current_image()
            # Limpiar la figura y mostrar la nueva imagen con el mapa de colores seleccionado
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            cmap_name = self.cmap_combobox.currentText()
            ax.imshow(dicom_image.pixel_array, cmap=cmap_name)
            self.canvas.draw()


class MedVisController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_login()

    def init_login(self):
        login = MedVisLogin()
        if login.exec_() == QDialog.Accepted:
            self.init_ui()
        else:
            sys.exit(0)  # Salir de la aplicación si el login falla

    def init_ui(self):
        self.model = MedVisDicomModel()
        self.viewer = MedVisDicomViewer(self.model)
        self.setCentralWidget(self.viewer)

        # Configurar estilo de la aplicación
        self.set_application_style()

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("MedVis - Visualizador DICOM")

        # Botón de logout
        self.logoutButton = QPushButton("Logout", self)
        self.logoutButton.clicked.connect(self.logout)
        self.statusBar().addPermanentWidget(self.logoutButton)

        # Diálogo para seleccionar la carpeta DICOM
        dicom_folder_path = QFileDialog.getExistingDirectory(self, "Seleccione la carpeta DICOM")
        if dicom_folder_path:
            self.model.load_dicom_folder(dicom_folder_path)
            self.viewer.slider.setMaximum(len(self.model.dicom_files) - 1)
            if self.model.dicom_files:
                self.viewer.update_image()

        self.show()

    def set_application_style(self):
        # Cambiar el estilo de la aplicación a Fusion y configurar colores
        app_palette = QPalette()
        app_palette.setColor(QPalette.Window, QColor(255, 239, 219))  # Pastel
        app_palette.setColor(QPalette.WindowText, Qt.black)
        app_palette.setColor(QPalette.Button, QColor(255, 239, 219))
        app_palette.setColor(QPalette.ButtonText, Qt.black)
        app_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        app_palette.setColor(QPalette.Highlight, QColor(173, 216, 230))  # Color resaltado
        app_palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(app_palette)

    def logout(self):
        self.close()
        self.init_login()


def main():
    app = QApplication(sys.argv)
    medvis_app = MedVisController()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


