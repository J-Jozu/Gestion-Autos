"""
Gestión de rutas multiplataforma (Windows/Linux)
Utiliza pathlib para compatibilidad total
"""
from pathlib import Path
import os

class PathManager:
    """Gestor de rutas dinámicas para la aplicación"""
    
    def __init__(self):
        # Directorio raíz del proyecto
        self.root_dir = Path(__file__).parent.parent
        
        # Directorios principales
        self.images_dir = self.root_dir / "view" / "img"
        self.output_dir = self.root_dir / "output"
        self.database_dir = self.root_dir / "database"
        
        # Crear directorios si no existen
        self._create_directories()
    
    def _create_directories(self):
        """Crea los directorios necesarios si no existen"""
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.database_dir.mkdir(parents=True, exist_ok=True)
    
    def get_image_path(self, filename):
        """Retorna la ruta completa para una imagen"""
        if not filename:
            return None
        return str(self.images_dir / filename)
    
    def get_output_path(self, filename):
        """Retorna la ruta completa para un archivo de salida (PDF)"""
        return str(self.output_dir / filename)
    
    def get_relative_image_path(self, absolute_path):
        """Convierte una ruta absoluta a relativa para guardar en BD"""
        if not absolute_path:
            return None
        path = Path(absolute_path)
        return path.name

# Instancia global del gestor de rutas
path_manager = PathManager()
