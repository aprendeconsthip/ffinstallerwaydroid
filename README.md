🚀 FFINSTALLERWAYDROID
Instalador rápido y sencillo para Waydroid, con soporte para Free Fire, diseñado especialmente para usuarios de Linux.

📦 Requisitos
Sistema Linux compatible

Acceso a terminal con privilegios sudo

Conexión a internet

ADB instalado (ver tabla abajo)

🛠️ Instalación
1. Descargar el instalador
Ve a la sección de Releases y descarga el archivo ZIP más reciente.

2. Descomprimir y dar permisos
Extrae el contenido del ZIP y otorga permisos de ejecución al instalador:

bash
Copiar
Editar
chmod +x install.sh
3. Ejecutar el instalador
Inicia la instalación con permisos de superusuario:

bash
Copiar
Editar
sudo ./install.sh
🔧 Instalación de ADB
ADB (Android Debug Bridge) es necesario para ejecutar correctamente Waydroid. Usa el siguiente comando según tu distribución de Linux:


Distribución	Comando de instalación
Debian / Ubuntu	sudo apt install adb
Arch / Manjaro	sudo pacman -S android-tools
Fedora	sudo dnf install android-tools
openSUSE	sudo zypper install android-tools
Void Linux	sudo xbps-install -S android-tools
Solus	sudo eopkg install android-tools
Gentoo	emerge --ask dev-util/android-tools
✅ ¡Todo listo!
Una vez completados estos pasos, Waydroid estará instalado y listo para correr Free Fire.
¿Problemas o dudas? Abre un Issue y con gusto te ayudamos.
