# 🐧 Guía de Instalación en Linux

## 🚀 Instalación Rápida

```bash
# 1. Dar permisos de ejecución
chmod +x install.sh run.sh

# 2. Ejecutar instalador
./install.sh

# 3. Configurar base de datos MySQL
sudo mysql -u root -p < database/venta_autos_db.sql

# 4. Editar archivo .env con tus credenciales
nano .env

# 5. Ejecutar aplicación
./run.sh
```

## 📋 Requisitos del Sistema

El script `install.sh` detecta automáticamente tu distribución e instala las dependencias necesarias.

### Ubuntu/Debian/Linux Mint
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-tk mysql-server
```

### Fedora/RHEL/CentOS
```bash
sudo dnf install python3 python3-pip python3-tkinter mariadb-server
```

### Arch Linux/Manjaro
```bash
sudo pacman -S python python-pip tk mysql
```

### openSUSE
```bash
sudo zypper install python3 python3-pip python3-tk mysql-community-server
```

**Nota:** El instalador automático (`install.sh`) detecta tu distribución y ejecuta los comandos correctos.

## ⚙️ Configuración de MariaDB

```bash
# Iniciar el servicio de MariaDB
# En Fedora:
sudo systemctl start mariadb
sudo systemctl enable mariadb

# En Ubuntu/Debian (puede ser mysql o mariadb):
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

### Opción 1: Usar root sin contraseña (Fedora por defecto)
```bash
# Importar base de datos directamente
sudo mysql -u root < database/venta_autos_db.sql

# Configurar .env
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_NAME=venta_autos_db
```

### Opción 2: Crear usuario específico
```bash
# Acceder a MariaDB
sudo mysql -u root
```

Dentro de MariaDB:
```sql
CREATE DATABASE IF NOT EXISTS venta_autos_db;
CREATE USER 'autogest'@'localhost' IDENTIFIED BY 'tu_contraseña';
GRANT ALL PRIVILEGES ON venta_autos_db.* TO 'autogest'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Luego importa la estructura:
```bash
mysql -u autogest -p venta_autos_db < database/venta_autos_db.sql
```

## 🔐 Configuración del .env

Edita el archivo `.env`:
```bash
nano .env
```

Configura tus credenciales:
```env
# Base de Datos (para root sin contraseña en Fedora)
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=venta_autos_db

# Cloudinary
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

## 🔧 Solución de Problemas

### Error: "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora/RHEL/CentOS
sudo dnf install python3-tkinter

# Arch/Manjaro
sudo pacman -S tk

# openSUSE
sudo zypper install python3-tk
```

### Error: "Cannot connect to MariaDB/MySQL"
```bash
# Verificar estado del servicio
sudo systemctl status mariadb

# Iniciar servicio
# Fedora/RHEL/CentOS:
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Ubuntu/Debian:
sudo systemctl start mariadb  # o mysql
sudo systemctl enable mariadb

# Ver logs
sudo journalctl -u mariadb

# Si usas root sin contraseña, accede así:
sudo mysql -u root

# Si configuraste contraseña:
mysql -u root -p
```

### Error: "Permission denied" al ejecutar scripts
```bash
chmod +x install.sh run.sh
```

### Error con Pillow/PIL
```bash
# Ubuntu/Debian
sudo apt install python3-pil python3-pil.imagetk

# Fedora/RHEL/CentOS
sudo dnf install python3-pillow python3-pillow-tk

# Arch/Manjaro
sudo pacman -S python-pillow

# O reinstalar con pip
pip install --upgrade Pillow
```

### Problemas con CustomTkinter
```bash
pip uninstall customtkinter
pip install customtkinter --upgrade
```

## 📦 Gestión del Entorno Virtual

### Activar manualmente
```bash
source venv/bin/activate
```

### Desactivar
```bash
deactivate
```

### Reinstalar entorno virtual
```bash
rm -rf venv
./install.sh
```

## 🖨️ Configuración de Impresión

Instala un visor de PDF:

**Ubuntu/Debian:**
```bash
sudo apt install evince
```

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install evince
```

**Arch/Manjaro:**
```bash
sudo pacman -S evince
```

**openSUSE:**
```bash
sudo zypper install evince
```

## ▶️ Ejecutar la Aplicación

```bash
# Método recomendado
./run.sh

# O manualmente
source venv/bin/activate
python3 main.py
```

## 🔄 Actualizar el Proyecto

```bash
# Si usas Git
git pull origin main

# Activar entorno virtual
source venv/bin/activate

# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Aplicar cambios en la BD si los hay
mysql -u autogest -p venta_autos_db < database/venta_autos_db.sql
```

## ✅ Verificar Instalación

```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar paquetes
pip list

# Verificar importaciones
python3 -c "import customtkinter; import mysql.connector; import cloudinary; print('✅ Todo correcto')"

# Verificar MySQL
mysql -u autogest -p -e "SHOW DATABASES;"
```

---

## 📞 Soporte Adicional

- Consulta `README.md` para más información
- Revisa `INSTALACION_MULTIPLATAFORMA.md` para otros sistemas
- Verifica `CLOUDINARY_SETUP.md` para configurar almacenamiento de imágenes

**¡Listo! AutoGest funcionando en Linux! 🎉**
