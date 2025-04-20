# 🚀 FFINSTALLERWAYDROID  

Instalador rápido y sencillo de **Waydroid**, con soporte optimizado para **Free Fire**.  
Desarrollado en **Python** para usuarios de **Linux**.

---

## 📦 Requisitos

- Sistema operativo **Linux** compatible  
- Acceso a la terminal con privilegios **sudo**  
- **Conexión a Internet** activa  
- **ADB** instalado (consulta más abajo cómo verificarlo)

---

## 🛠️ Instalación

### 1. Descargar el Release  
Ve a la sección de **[Releases](https://github.com/tuusuario/tu-repositorio/releases)** y descarga el archivo **ZIP más reciente** del instalador.

---

### 2. Descomprimir y dar permisos  
Extrae el contenido del archivo ZIP descargado. Luego, abre una terminal en esa carpeta y ejecuta:

```bash
chmod +x install.sh


## 🔧 Instalación de ADB

ADB (Android Debug Bridge) es necesario para ejecutar el proyecto correctamente Usa el siguiente comando según tu distribución de Linux:

| Distribución     | Comando de instalación                          |
|------------------|-------------------------------------------------|
| **Debian / Ubuntu**  | `sudo apt install adb`                         |
| **Arch / Manjaro**   | `sudo pacman -S android-tools`                |
| **Fedora**           | `sudo dnf install android-tools`              |
| **openSUSE**         | `sudo zypper install android-tools`           |
| **Void Linux**       | `sudo xbps-install -S android-tools`          |
| **Solus**            | `sudo eopkg install android-tools`            |
| **Gentoo**           | `emerge --ask dev-util/android-tools`         |

