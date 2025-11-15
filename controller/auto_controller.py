"""
Controlador para la gestión de autos
Intermediario entre la vista y el modelo
"""
from model.auto_model import AutoModel
from utils.validators import Validator
from utils.paths import path_manager
import shutil
from pathlib import Path

class AutoController:
    """Controlador para operaciones de autos"""
    
    @staticmethod
    def validar_datos_auto(marca, modelo, anio, precio, color, transmision, combustible):
        """
        Valida los datos de un auto antes de guardar
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Validar campos requeridos
        valid, msg = Validator.validate_required(marca, "Marca")
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_required(modelo, "Modelo")
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_year(anio)
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_number(precio, "Precio", min_value=0)
        if not valid:
            return False, msg
        
        valid, msg = Validator.validate_required(color, "Color")
        if not valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def guardar_imagen(source_path):
        """
        Copia una imagen al directorio de imágenes de la aplicación
        
        Returns:
            str: Nombre del archivo guardado o None si hay error
        """
        if not source_path:
            return None
        
        try:
            source = Path(source_path)
            if not source.exists():
                return None
            
            # Generar nombre único si es necesario
            dest_filename = source.name
            dest_path = Path(path_manager.get_image_path(dest_filename))
            
            # Si el archivo ya existe, agregar un número
            counter = 1
            while dest_path.exists():
                name_parts = source.stem, counter, source.suffix
                dest_filename = f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                dest_path = Path(path_manager.get_image_path(dest_filename))
                counter += 1
            
            # Copiar el archivo
            shutil.copy2(source, dest_path)
            return dest_filename
        except Exception as e:
            print(f"Error al guardar imagen: {e}")
            return None
    
    @staticmethod
    def crear_auto(marca, modelo, anio, precio, color, transmision, combustible, imagen_path=None):
        """
        Crea un nuevo auto después de validar los datos
        
        Returns:
            tuple: (success, id_auto/error_message)
        """
        # Validar datos
        valid, msg = AutoController.validar_datos_auto(
            marca, modelo, anio, precio, color, transmision, combustible
        )
        if not valid:
            return False, msg
        
        # Guardar imagen si existe
        imagen_filename = None
        if imagen_path:
            imagen_filename = AutoController.guardar_imagen(imagen_path)
        
        # Crear el auto
        return AutoModel.crear_auto(
            marca, modelo, anio, precio, color, transmision, combustible, imagen_filename
        )
    
    @staticmethod
    def actualizar_auto(id_auto, marca, modelo, anio, precio, color, transmision, combustible, imagen_path=None):
        """
        Actualiza un auto existente después de validar los datos
        
        Returns:
            tuple: (success, message)
        """
        # Validar datos
        valid, msg = AutoController.validar_datos_auto(
            marca, modelo, anio, precio, color, transmision, combustible
        )
        if not valid:
            return False, msg
        
        # Guardar nueva imagen si existe
        imagen_filename = None
        if imagen_path:
            imagen_filename = AutoController.guardar_imagen(imagen_path)
        
        # Actualizar el auto
        return AutoModel.actualizar_auto(
            id_auto, marca, modelo, anio, precio, color, transmision, combustible, imagen_filename
        )
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los autos"""
        return AutoModel.obtener_todos()
    
    @staticmethod
    def obtener_por_id(id_auto):
        """Obtiene un auto por ID"""
        return AutoModel.obtener_por_id(id_auto)
    
    @staticmethod
    def eliminar_auto(id_auto):
        """Elimina un auto"""
        return AutoModel.eliminar_auto(id_auto)
    
    @staticmethod
    def buscar_autos(criterio):
        """Busca autos por criterio"""
        return AutoModel.buscar_autos(criterio)
