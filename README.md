# AutoGest - Sistema de Gestión de Venta de Autos

Sistema completo de gestión para concesionarias de autos desarrollado en Python con interfaz gráfica moderna usando CustomTkinter.

## Características

- **Gestión de Autos**: CRUD completo con soporte para imágenes
- **Gestión de Clientes**: Registro y administración de clientes
- **Gestión de Ventas**: Registro de ventas con relación auto-cliente
- **Reportes**: Estadísticas y generación de PDFs profesionales
- **Interfaz Moderna**: Diseño profesional con paleta de colores azules y verde lima
- **Multiplataforma**: Compatible con Windows y Linux

## Paleta de Colores

- **Fondo principal**: Azul oscuro translúcido (#1E2A38)
- **Fondo claro**: Blanco humo (#F5F7FA)
- **Botones principales**: Azul medio (#3B82F6)
- **Botones secundarios**: Verde lima (#10B981)
- **Resaltado**: Azul eléctrico (#2563EB)
- **Texto principal**: Gris oscuro (#1F2937)
- **Texto secundario**: Gris medio (#6B7280)

## Requisitos del Sistema

- Python 3.8 o superior
- MySQL 5.7 o superior
- Sistema operativo: Windows 10/11 o Linux (Ubuntu 20.04+)

## Instalación

### 1. Clonar o descargar el proyecto

\`\`\`bash
git clone <url-del-repositorio>
cd car-sales-app
\`\`\`

### 2. Crear entorno virtual (recomendado)

**Windows:**
\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

**Linux:**
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Instalar dependencias

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Configurar MySQL

Asegúrese de que MySQL esté instalado y en ejecución.

**Windows:**
- Descargue MySQL desde https://dev.mysql.com/downloads/installer/
- Instale y configure con usuario `root` y contraseña de su elección

**Linux (Ubuntu/Debian):**
\`\`\`bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
\`\`\`

### 5. Configurar la base de datos

Edite el archivo `model/conexion.py` con sus credenciales de MySQL:

\`\`\`python
self.host = "localhost"
self.user = "root"  # Su usuario de MySQL
self.password = ""  # Su contraseña de MySQL
self.database = "venta_autos_db"
\`\`\`

### 6. Crear la base de datos

Ejecute el script SQL ubicado en `database/create_database.sql`:

**Opción 1 - Desde MySQL CLI:**
\`\`\`bash
mysql -u root -p < database/create_database.sql
\`\`\`

**Opción 2 - Desde la aplicación:**
La aplicación creará automáticamente la base de datos al iniciar si no existe.

## Uso

### Iniciar la aplicación

\`\`\`bash
python main.py
\`\`\`

### Navegación

La aplicación cuenta con un **sidebar lateral** con las siguientes secciones:

- **Autos**: Gestión completa de vehículos
- **Clientes**: Administración de clientes
- **Ventas**: Registro de ventas
- **Reportes**: Estadísticas y reportes

### Funcionalidades principales

#### Gestión de Autos
- Agregar nuevos autos con imagen
- Editar información de autos existentes
- Eliminar autos
- Buscar autos por marca, modelo o color
- Generar PDF con ficha técnica del vehículo

#### Gestión de Clientes
- Registrar nuevos clientes
- Editar información de clientes
- Eliminar clientes
- Buscar clientes por nombre, teléfono o correo

#### Gestión de Ventas
- Registrar nuevas ventas
- Asociar auto y cliente a la venta
- Seleccionar método de pago
- Generar comprobante de venta en PDF
- Ver historial de ventas

#### Reportes
- Total de ventas realizadas
- Monto total de ventas
- Venta promedio
- Venta mayor y menor

### Generación de PDFs

Los PDFs se generan automáticamente en la carpeta `output/` con las siguientes características:

- **Fichas de autos**: Incluyen imagen, datos técnicos y precio
- **Comprobantes de venta**: Incluyen datos del cliente, auto y monto total
- **Diseño profesional**: Logo, tablas organizadas y fecha de generación
- **Apertura automática**: Opción de abrir el PDF inmediatamente después de generarlo

## Estructura del Proyecto

\`\`\`
car-sales-app/
├── main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Este archivo
├── model/                 # Modelos y conexión a BD
│   ├── conexion.py
│   ├── auto_model.py
│   ├── cliente_model.py
│   └── venta_model.py
├── view/                  # Interfaces gráficas
│   ├── main_view.py
│   ├── auto_view.py
│   ├── cliente_view.py
│   ├── venta_view.py
│   ├── report_view.py
│   └── img/              # Imágenes de autos
├── controller/            # Lógica de negocio
│   ├── auto_controller.py
│   ├── cliente_controller.py
│   └── venta_controller.py
├── utils/                 # Utilidades
│   ├── paths.py          # Gestión de rutas multiplataforma
│   ├── validators.py     # Validaciones
│   └── printer.py        # Generación de PDFs
├── database/             # Scripts SQL
│   └── create_database.sql
└── output/               # PDFs generados
\`\`\`

## Solución de Problemas

### Error de conexión a MySQL

**Problema**: "Error de conexión: Access denied for user 'root'@'localhost'"

**Solución**:
1. Verifique que MySQL esté en ejecución
2. Confirme que las credenciales en `model/conexion.py` sean correctas
3. En MySQL, ejecute:
\`\`\`sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'su_contraseña';
FLUSH PRIVILEGES;
\`\`\`

### Error al importar módulos

**Problema**: "ModuleNotFoundError: No module named 'customtkinter'"

**Solución**:
\`\`\`bash
pip install --upgrade -r requirements.txt
\`\`\`

### Imágenes no se muestran en PDFs

**Problema**: Las imágenes no aparecen en los PDFs generados

**Solución**:
- Verifique que las imágenes estén en la carpeta `view/img/`
- Asegúrese de que los formatos sean JPG, PNG o similares
- Compruebe los permisos de lectura de la carpeta

### PDFs no se abren automáticamente

**Problema**: El PDF se genera pero no se abre

**Solución**:
- **Windows**: Verifique que tenga un lector de PDF instalado (Adobe Reader, Edge, etc.)
- **Linux**: Instale un visor de PDF:
\`\`\`bash
sudo apt install evince  # o xdg-utils
\`\`\`

## Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje de programación
- **CustomTkinter**: Framework para interfaz gráfica moderna
- **MySQL**: Base de datos relacional
- **ReportLab**: Generación de PDFs
- **Pillow (PIL)**: Procesamiento de imágenes
- **mysql-connector-python**: Conector de MySQL

## Características de Diseño

### Interfaz de Usuario
- Sidebar con navegación intuitiva
- Tablas con filas alternadas y hover effects
- Formularios con campos estilizados
- Botones con colores semánticos (verde para crear, azul para editar, rojo para eliminar)
- Búsqueda en tiempo real
- Mensajes de confirmación para acciones críticas

### Experiencia de Usuario
- Enfoque automático en primer campo de formularios
- Validaciones en tiempo real
- Mensajes claros de éxito y error
- Transiciones suaves entre vistas
- Diseño responsive y adaptable

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Soporte

Para reportar problemas o solicitar nuevas características, por favor abra un issue en el repositorio del proyecto.

## Autor

Desarrollado con Python y CustomTkinter para gestión profesional de concesionarias de autos.
