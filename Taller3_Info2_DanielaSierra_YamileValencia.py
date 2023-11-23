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
        self.cmap_combobox = None
        self.zoom_factor = 1.0
        self.drag_start = None

        self.canvas.mpl_connect("button_press_event", self.on_mouse_press)
        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_move)
        self.canvas.mpl_connect("button_release_event", self.on_mouse_release)

        # Definir botones de Zoom antes de llamar a initUI
        self.zoom_in_button = QPushButton("+", self)
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button = QPushButton("-", self)
        self.zoom_out_button.clicked.connect(self.zoom_out)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Agregar ComboBox y botones de zoom
        self.cmap_combobox = QComboBox(self)
        self.cmap_combobox.addItems(['viridis', 'inferno', 'plasma', 'magma', 'cividis', 'twilight'])
        self.cmap_combobox.currentIndexChanged.connect(self.update_image)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.valueChanged[int].connect(self.slider_changed)

        # Añadir widgets al layout
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        layout.addWidget(self.cmap_combobox)
        layout.addWidget(self.zoom_in_button)
        layout.addWidget(self.zoom_out_button)

        self.setLayout(layout)

    def slider_changed(self, value):
        self.model.current_image_index = value
        self.update_image()

    def zoom_in(self):
        if self.zoom_factor > 0.1:  # Evitar un zoom demasiado pequeño
            self.zoom_factor /= 1.2  # Reducir el zoom (acercar)
            self.update_image()

    def zoom_out(self):
        self.zoom_factor *= 1.2  # Aumentar el zoom (alejar)
        self.update_image()

    def update_image(self):
        dicom_files_exist = bool(self.model.dicom_files)
        if dicom_files_exist:
            dicom_image = self.model.get_current_image()
            self.figure.clf()
            ax = self.figure.add_subplot(111)
            cmap_name = self.cmap_combobox.currentText()
            
            # Calcular los límites de visualización
            width, height = dicom_image.pixel_array.shape[1], dicom_image.pixel_array.shape[0]
            xlim = width * self.zoom_factor / 2
            ylim = height * self.zoom_factor / 2
            center_x, center_y = width / 2, height / 2

            # Aplicar el zoom
            ax.imshow(dicom_image.pixel_array, cmap=cmap_name, aspect='auto')
            ax.set_xlim([center_x - xlim, center_x + xlim])
            ax.set_ylim([center_y + ylim, center_y - ylim])

            self.canvas.draw()
    
    def on_mouse_press(self, event):
        if event.button == 1:  # Botón izquierdo del ratón
            self.drag_start = (event.xdata, event.ydata)

    def on_mouse_move(self, event):
        if event.button == 1 and self.drag_start:
            dx = self.drag_start[0] - event.xdata
            dy = self.drag_start[1] - event.ydata
            self.drag_start = (event.xdata, event.ydata)
            self.pan_image(dx, dy)

    def on_mouse_release(self, event):
        if event.button == 1:
            self.drag_start = None

    def pan_image(self, dx, dy):
        if not bool(self.model.dicom_files):
            return

        ax = self.figure.axes[0]
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
        ax.set_ylim(ylim[0] + dy, ylim[1] + dy)

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


