"""
Sistema de Gestión de Venta de Autos
Punto de entrada principal de la aplicación
Compatible con Windows y Linux
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from view.main_view import MainApplication

def main():
    """Función principal que inicia la aplicación"""
    app = MainApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
