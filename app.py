import subprocess
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox, QLineEdit, QHBoxLayout,
    QProgressBar, QDialog, QInputDialog, QFrame
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon, QPixmap
import time
import webbrowser
import sys
import qtawesome as qta

class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Acerca de")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(500, 400)  # Increase the size of the window

        # Hacer la ventana semi-transparente
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)  # Añadir márgenes para el contenido

        # Fondo semi-transparente
        background = QWidget()
        background.setStyleSheet("background-color: rgba(40, 44, 52, 0.9); border-radius: 15px;")
        background_layout = QVBoxLayout(background)
        background_layout.setContentsMargins(20, 20, 20, 20)

        # Logo
        logo_label = QLabel(self)
        pixmap = QPixmap("icon.png").scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        background_layout.addWidget(logo_label)

        # Título
        title_label = QLabel("Instalador de FreeFire para Waydroid", self)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #61dafb; margin-bottom: 15px;")
        background_layout.addWidget(title_label)

        # Versión
        version_label = QLabel("Versión 1.0", self)
        version_label.setFont(QFont("Arial", 12))
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #abb2bf;")
        background_layout.addWidget(version_label)

        # Descripción
        desc_label = QLabel("Herramienta profesional para instalar FreeFire en Waydroid", self)
        desc_label.setFont(QFont("Arial", 10))  # Decrease the font size here
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setStyleSheet("color: #abb2bf; margin: 20px 0;")
        background_layout.addWidget(desc_label)

        # Link a YouTube
        developed_by_label = QLabel('Desarrollado por <a href="https://www.youtube.com/@AprendeConSthip" style="color: #61dafb;">Aprende con Sthip</a>', self)
        developed_by_label.setFont(QFont("Arial", 10))
        developed_by_label.setAlignment(Qt.AlignCenter)
        developed_by_label.setStyleSheet("color: #abb2bf;")  # Set the same color as other text
        developed_by_label.setOpenExternalLinks(True)
        background_layout.addWidget(developed_by_label)

        # Botón de cerrar
        close_button = QPushButton(qta.icon("fa5s.times", color="white"), " Cerrar", self)
        close_button.setFont(QFont("Arial", 12))
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #e06c75;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #be5046;
            }
        """)
        close_button.clicked.connect(self.close)
        background_layout.addWidget(close_button)

        layout.addWidget(background)
        self.setLayout(layout)

class FreeFireInstaller(QWidget):
    def __init__(self):
        super().__init__()
        self.password = self.get_password()
        if not self.password:
            QMessageBox.critical(self, "Error", "La contraseña es requerida para continuar")
            self.close()
            return

        # Configurar ventana principal
        self.setWindowTitle("Instalador de FreeFire en Waydroid")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(200, 200, 650, 550)
        self.center()  # Centrar la ventana en la pantalla

        # Estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #282c34;
                color: #ffffff;
                font-family: 'Segoe UI', Arial;
            }
            QLabel {
                font-size: 13px;
                margin: 5px 0;
            }
            QLineEdit {
                background-color: #3e4451;
                border: 1px solid #3e4451;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #61dafb;
            }
            QProgressBar {
                border: 1px solid #3e4451;
                border-radius: 4px;
                text-align: center;
                height: 20px;
                background-color: #3e4451;
            }
            QProgressBar::chunk {
                background-color: #61dafb;
                border-radius: 3px;
            }
            QFrame {
                border: 1px solid #3e4451;
                border-radius: 5px;
            }
            QInputDialog QLineEdit {
                background-color: #3e4451;
                border: 1px solid #61dafb;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
                font-size: 13px;
            }
        """)

        self.setup_ui()
        self.setup_directories()
        self.load_ip()
        self.check_adb_installation()

    def center(self):
        # Centrar la ventana en la pantalla
        qr = self.frameGeometry()
        cp = QApplication.desktop().screenGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Sección de estado
        status_frame = QFrame()
        status_frame.setStyleSheet("background-color: #3e4451; border-radius: 5px;")
        status_layout = QVBoxLayout(status_frame)

        status_title = QLabel("Estado del Sistema")
        status_title.setFont(QFont("Arial", 11, QFont.Bold))
        status_title.setStyleSheet("color: #61dafb; margin-bottom: 10px;")
        status_layout.addWidget(status_title)

        self.status_label = QLabel("Estado: Preparado")
        self.status_label.setStyleSheet("font-weight: bold; color: #98c379;")
        status_layout.addWidget(self.status_label)

        self.version_label = QLabel("Versión: Desconocida")
        status_layout.addWidget(self.version_label)

        main_layout.addWidget(status_frame)

        # Sección de configuración ADB
        config_frame = QFrame()
        config_frame.setStyleSheet("background-color: #3e4451; border-radius: 5px;")
        config_layout = QVBoxLayout(config_frame)

        config_title = QLabel("Configuración ADB")
        config_title.setFont(QFont("Arial", 11, QFont.Bold))
        config_title.setStyleSheet("color: #61dafb; margin-bottom: 10px;")
        config_layout.addWidget(config_title)

        # Configuración de IP
        ip_layout = QHBoxLayout()
        ip_layout.addWidget(QLabel("IP de Waydroid:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ejemplo: 192.168.100.2")
        ip_layout.addWidget(self.ip_input)

        # Botones para IP con iconos
        self.save_ip_button = QPushButton(qta.icon("fa5.save", color="white"), "")
        self.save_ip_button.setToolTip("Guardar IP")
        self.save_ip_button.setFixedSize(30, 30)
        self.save_ip_button.clicked.connect(self.save_ip)

        self.edit_ip_button = QPushButton(qta.icon("fa5.edit", color="white"), "")
        self.edit_ip_button.setToolTip("Editar IP")
        self.edit_ip_button.setFixedSize(30, 30)
        self.edit_ip_button.clicked.connect(self.enable_ip_edit)

        ip_button_layout = QHBoxLayout()
        ip_button_layout.addWidget(self.edit_ip_button)
        ip_button_layout.addWidget(self.save_ip_button)
        ip_layout.addLayout(ip_button_layout)

        config_layout.addLayout(ip_layout)

        # Botón de prueba de conexión con icono
        self.test_connection_button = QPushButton(qta.icon("fa5s.plug", color="white"), " Probar Conexión ADB")
        self.test_connection_button.clicked.connect(self.test_adb_connection)
        config_layout.addWidget(self.test_connection_button)

        main_layout.addWidget(config_frame)

        # Sección de descargas
        download_frame = QFrame()
        download_frame.setStyleSheet("background-color: #3e4451; border-radius: 5px;")
        download_layout = QVBoxLayout(download_frame)

        download_title = QLabel("Gestión de Archivos")
        download_title.setFont(QFont("Arial", 11, QFont.Bold))
        download_title.setStyleSheet("color: #61dafb; margin-bottom: 10px;")
        download_layout.addWidget(download_title)

        # Botones de descarga con iconos
        button_layout = QHBoxLayout()

        self.download_button = QPushButton(qta.icon("fa5s.download", color="white"), " Descargar Archivos")
        self.download_button.clicked.connect(self.download_files)
        button_layout.addWidget(self.download_button)

        self.check_update_button = QPushButton(qta.icon("fa5s.sync-alt", color="white"), " Verificar Actualización")
        self.check_update_button.clicked.connect(self.check_for_updates)
        button_layout.addWidget(self.check_update_button)

        download_layout.addLayout(button_layout)

        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        download_layout.addWidget(self.progress_bar)

        main_layout.addWidget(download_frame)

        # Sección de instalación
        install_frame = QFrame()
        install_frame.setStyleSheet("background-color: #3e4451; border-radius: 5px;")
        install_layout = QVBoxLayout(install_frame)

        install_title = QLabel("Instalación")
        install_title.setFont(QFont("Arial", 11, QFont.Bold))
        install_title.setStyleSheet("color: #61dafb; margin-bottom: 10px;")
        install_layout.addWidget(install_title)

        # Botón de instalación principal con icono
        self.install_button = QPushButton(qta.icon("fa5s.gamepad", color="white"), " Instalar FreeFire")
        self.install_button.clicked.connect(self.install_freefire)
        self.install_button.setEnabled(False)
        install_layout.addWidget(self.install_button)

        # Botón para instalar Magisk Delta con icono
        self.magisk_button = QPushButton(qta.icon("fa5s.magic", color="white"), " Instalar Magisk Delta")
        self.magisk_button.clicked.connect(self.install_magisk_delta)
        self.magisk_button.setStyleSheet("""
            QPushButton {
                background-color: #98c379;
                color: white;
            }
            QPushButton:hover {
                background-color: #7a9f60;
            }
        """)
        install_layout.addWidget(self.magisk_button)

        main_layout.addWidget(install_frame)

        # Barra de herramientas inferior
        tool_frame = QFrame()
        tool_layout = QHBoxLayout(tool_frame)
        tool_layout.setContentsMargins(0, 0, 0, 0)

        # Botón Acerca de con icono
        self.about_button = QPushButton(qta.icon("fa5s.info-circle", color="white"), " Acerca de")
        self.about_button.clicked.connect(self.show_about)
        tool_layout.addWidget(self.about_button)

        tool_layout.addStretch()

        # Botón Salir con icono
        self.exit_button = QPushButton(qta.icon("fa5s.sign-out-alt", color="white"), " Salir")
        self.exit_button.clicked.connect(self.confirm_exit)
        tool_layout.addWidget(self.exit_button)

        main_layout.addWidget(tool_frame)

        # Estilo para botones
        button_style = """
            QPushButton {
                background-color: #61dafb;
                color: #282c34;
                border: none;
                padding: 8px 12px;
                font-size: 13px;
                border-radius: 4px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #21a1f1;
            }
            QPushButton:disabled {
                background-color: #5c6370;
                color: #abb2bf;
            }
            QPushButton[accessibleName="danger"] {
                background-color: #e06c75;
                color: white;
            }
            QPushButton[accessibleName="danger"]:hover {
                background-color: #be5046;
            }
            QPushButton[accessibleName="success"] {
                background-color: #98c379;
                color: white;
            }
            QPushButton[accessibleName="success"]:hover {
                background-color: #7a9f60;
            }
        """

        # Aplicar estilos a los botones
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(button_style)
            btn.setCursor(Qt.PointingHandCursor)

        # Estilos especiales para botones específicos
        self.exit_button.setAccessibleName("danger")
        self.install_button.setAccessibleName("success")

        self.setLayout(main_layout)

    def setup_directories(self):
        self.download_dir = os.path.join(os.getcwd(), "downloads")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def get_password(self):
        """Solicitar la contraseña del usuario al iniciar el programa."""
        password, ok = QInputDialog.getText(
            self, "Autenticación requerida",
            "Por favor ingrese su contraseña:",
            QLineEdit.Password
        )
        if ok and password:
            return password
        return None

    def enable_ip_edit(self):
        self.ip_input.setReadOnly(False)
        self.ip_input.setFocus()

    def check_adb_installation(self):
        try:
            # Verificar si ADB está instalado
            result = subprocess.run(
                ["adb", "--version"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True
            )
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args)
            self.status_label.setText("ADB está instalado correctamente")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.status_label.setText("ADB no está instalado - Funcionalidad limitada")
            self.install_button.setEnabled(False)
            return False

    def test_adb_connection(self):
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Error", "Por favor ingresa la IP de Waydroid")
            return
        try:
            self.status_label.setText("Conectando al dispositivo...")
            self.progress_bar.setValue(20)
            QApplication.processEvents()

            # Usar sudo para comandos ADB que requieren permisos
            connect_cmd = f"echo {self.password} | sudo -S adb connect {ip}"
            result = subprocess.run(
                connect_cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=True
            )

            if "connected" in result.stdout:
                # Verificar autorización
                devices_cmd = f"echo {self.password} | sudo -S adb devices"
                devices_result = subprocess.run(
                    devices_cmd,
                    stderr=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    text=True,
                    shell=True
                )

                if "unauthorized" in devices_result.stdout:
                    self.status_label.setText("Esperando autorización...")
                    self.progress_bar.setValue(40)
                    QMessageBox.information(
                        self, "Autorización requerida",
                        "Por favor acepta la autorización ADB en el dispositivo Waydroid"
                    )
                    # Esperar y volver a verificar
                    time.sleep(5)
                    self.test_adb_connection()
                else:
                    self.status_label.setText("Dispositivo conectado y autorizado")
                    self.progress_bar.setValue(100)
                    self.install_button.setEnabled(True)
                    QMessageBox.information(self, "Éxito", "Conexión ADB establecida correctamente")
            else:
                error_msg = f"No se pudo conectar al dispositivo:\n{result.stdout}\n{result.stderr}"
                raise Exception(error_msg)
        except Exception as e:
            self.status_label.setText("Error de conexión ADB")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, "Error", str(e))

    def download_files(self):
        self.status_label.setText("Verificando archivos existentes...")
        self.progress_bar.setValue(10)
        QApplication.processEvents()

        try:
            api_url = "https://api.github.com/repos/xyberapp/ffapps/releases/latest"
            response = requests.get(api_url)
            response.raise_for_status()
            release_data = response.json()

            latest_version = release_data.get('tag_name', 'Desconocida')
            current_version = self.version_label.text().replace("Versión: ", "")

            # Buscar todos los assets .apk y .obb
            assets = {asset['name']: asset['browser_download_url'] for asset in release_data.get('assets', [])}
            apk_found = None
            obb_found = None
            for name, url in assets.items():
                if name.endswith('.apk'):
                    apk_found = (name, url)
                elif name.endswith('.obb'):
                    obb_found = (name, url)
                if apk_found and obb_found:
                    break

            if not apk_found or not obb_found:
                QMessageBox.critical(self, "Error", "No se encontraron los archivos necesarios en el release")
                return

            apk_local_path = os.path.join(self.download_dir, apk_found[0])
            obb_local_path = os.path.join(self.download_dir, obb_found[0])

            # Verificar si los archivos ya existen
            apk_exists = os.path.exists(apk_local_path)
            obb_exists = os.path.exists(obb_local_path)

            if apk_exists and obb_exists:
                if current_version == latest_version:
                    QMessageBox.information(self, "Última versión", "Ya tienes la última versión descargada.")
                else:
                    QMessageBox.information(self, "Archivos existentes", "Los archivos APK y OBB ya están descargados.")
                self.apk_path = apk_local_path
                self.obb_path = obb_local_path
                self.version_label.setText(f"Versión: {latest_version}")
                self.install_button.setEnabled(True)
                return

            # Si no existen o hay una nueva versión, proceder a descargar
            if not apk_exists or not obb_exists or current_version != latest_version:
                reply = QMessageBox.question(
                    self, "Descarga requerida",
                    "Los archivos no están completos o hay una nueva versión disponible. ¿Deseas descargarlos ahora?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    if not apk_exists or current_version != latest_version:
                        self._download_with_progress(apk_found[1], apk_found[0])
                    if not obb_exists or current_version != latest_version:
                        self._download_with_progress(obb_found[1], obb_found[0])
                    self.version_label.setText(f"Versión: {latest_version}")
                    self.status_label.setText("Descarga completada")
                    self.progress_bar.setValue(100)
                    self.install_button.setEnabled(True)
                else:
                    self.status_label.setText("Descarga cancelada")
                    self.progress_bar.setValue(0)
        except Exception as e:
            self.status_label.setText("Error en la descarga")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, 'Error', f"Error al descargar archivos:\n{str(e)}")

    def _download_with_progress(self, url, filename):
        local_path = os.path.join(self.download_dir, filename)
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    downloaded += len(chunk)
                    progress = int((downloaded / total_size) * 80) + 10  # 10-90%

                    # Mostrar qué archivo se está descargando
                    self.status_label.setText(f"Descargando {filename}... ({progress}%)")
                    self.progress_bar.setValue(progress)
                    QApplication.processEvents()
                    f.write(chunk)

        if filename.endswith('.apk'):
            self.apk_path = local_path
        elif filename.endswith('.obb'):
            self.obb_path = local_path

    def install_freefire(self):
        if not hasattr(self, 'apk_path') or not hasattr(self, 'obb_path'):
            QMessageBox.warning(self, "Error", "Primero debes descargar los archivos APK y OBB")
            return
        ip = self.ip_input.text().strip()
        if not ip:
            QMessageBox.warning(self, "Error", "Por favor ingresa la IP de Waydroid")
            return
        try:
            # Paso 1: Verificar conexión
            self.status_label.setText("Verificando conexión...")
            self.progress_bar.setValue(10)
            QApplication.processEvents()
            self.test_adb_connection()

            # Paso 2: Instalar APK
            self.status_label.setText("Instalando APK...")
            self.progress_bar.setValue(30)
            QApplication.processEvents()
            install_cmd = f"echo {self.password} | sudo -S adb -s {ip} install -r -t '{self.apk_path}'"
            install_result = subprocess.run(
                install_cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=True
            )
            if "Success" not in install_result.stdout:
                raise Exception(f"Error al instalar APK:\n{install_result.stdout}\n{install_result.stderr}")

            # Paso 3: Copiar OBB
            self.status_label.setText("Copiando archivos OBB...")
            self.progress_bar.setValue(60)
            QApplication.processEvents()
            package_name = "com.dts.freefiremax"
            obb_filename = os.path.basename(self.obb_path)
            temp_obb_path = f"/sdcard/{obb_filename}"
            final_obb_path = f"/sdcard/Android/obb/{package_name}/{obb_filename}"

            # Crear directorio temporal
            mkdir_temp_cmd = f"echo {self.password} | sudo -S adb -s {ip} shell mkdir -p '/sdcard/'"
            subprocess.run(mkdir_temp_cmd, check=True, shell=True)

            # Copiar OBB a /sdcard/
            push_temp_cmd = f"echo {self.password} | sudo -S adb -s {ip} push '{self.obb_path}' '{temp_obb_path}'"
            push_temp_result = subprocess.run(
                push_temp_cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=True
            )
            if push_temp_result.returncode != 0:
                raise Exception(f"Error al copiar OBB a sdcard:\n{push_temp_result.stdout}\n{push_temp_result.stderr}")

            # Crear directorio final
            mkdir_final_cmd = f"echo {self.password} | sudo -S adb -s {ip} shell mkdir -p '/sdcard/Android/obb/{package_name}'"
            subprocess.run(mkdir_final_cmd, check=True, shell=True)

            # Mover OBB al directorio final
            move_cmd = f"echo {self.password} | sudo -S adb -s {ip} shell mv '{temp_obb_path}' '{final_obb_path}'"
            move_result = subprocess.run(
                move_cmd,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
                shell=True
            )
            if move_result.returncode != 0:
                raise Exception(f"Error al mover OBB:\n{move_result.stdout}\n{move_result.stderr}")

            # Ajustar permisos
            chmod_cmd = f"echo {self.password} | sudo -S adb -s {ip} shell chmod 666 '{final_obb_path}'"
            subprocess.run(chmod_cmd, check=True, shell=True)

            # Éxito
            self.status_label.setText("Instalación completada!")
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Éxito", "FreeFire se instaló correctamente en Waydroid")
        except Exception as e:
            self.status_label.setText("Error en la instalación")
            self.progress_bar.setValue(0)
            QMessageBox.critical(self, 'Error', f"Error durante la instalación:\n{str(e)}")

    def save_ip(self):
        ip = self.ip_input.text().strip()
        if ip:
            with open("saved_ip.txt", "w") as file:
                file.write(ip)
            self.status_label.setText(f"IP guardada: {ip}")
            self.ip_input.setReadOnly(True)
        else:
            QMessageBox.warning(self, "Error", "La dirección IP no puede estar vacía")

    def load_ip(self):
        if os.path.exists("saved_ip.txt"):
            with open("saved_ip.txt", "r") as file:
                ip = file.read().strip()
                self.ip_input.setText(ip)
                self.ip_input.setReadOnly(True)

    def check_for_updates(self):
        try:
            self.status_label.setText("Buscando actualizaciones...")
            self.progress_bar.setValue(20)
            QApplication.processEvents()
            api_url = "https://api.github.com/repos/xyberapp/ffapps/releases/latest"
            response = requests.get(api_url)
            response.raise_for_status()
            release_data = response.json()
            latest_version = release_data.get('tag_name', 'Desconocida')
            current_version = self.version_label.text().replace("Versión: ", "")
            if current_version == "Desconocida":
                self.version_label.setText(f"Versión disponible: {latest_version}")
                QMessageBox.information(self, "Actualización",
                                     f"Versión más reciente disponible: {latest_version}")
            elif current_version != latest_version:
                reply = QMessageBox.question(
                    self, "Actualización disponible",
                    f"Hay una nueva versión disponible ({latest_version}). ¿Deseas actualizar?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.download_files()
            else:
                QMessageBox.information(self, "Actualización",
                                      "Ya tienes la versión más reciente instalada")
            self.progress_bar.setValue(100)
        except Exception as e:
            self.status_label.setText("Error al buscar actualizaciones")
            self.progress_bar.setValue(0)
            QMessageBox.warning(self, "Error", f"No se pudo verificar actualizaciones:\n{str(e)}")

    def install_magisk_delta(self):
        webbrowser.open("https://github.com/casualsnek/waydroid_script")

    def confirm_exit(self):
        reply = QMessageBox.question(
            self, "Confirmar salida",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

    def show_about(self):
        about_dialog = AboutDialog()
        about_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Establecer estilo de la aplicación
    app.setStyle('Fusion')

    # Verificar si qtawesome está instalado
    try:
        import qtawesome
    except ImportError:
        QMessageBox.critical(None, "Error", "La librería qtawesome no está instalada.\n"
                             "Por favor instálela con: pip install qtawesome")
        sys.exit(1)

    window = FreeFireInstaller()
    window.show()
    sys.exit(app.exec_())
