"""
Controlador para la gestión de clientes
Intermediario entre la vista y el modelo
"""
from model.cliente_model import ClienteModel
from utils.validators import Validator

class ClienteController:
    """Controlador para operaciones de clientes"""
    
    @staticmethod
    def validar_datos_cliente(nombre, telefono, correo, direccion):
        """
        Valida los datos de un cliente antes de guardar
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Validar campos requeridos
        valid, msg = Validator.validate_required(nombre, "Nombre")
        if not valid:
            return False, msg
        
        # Validar teléfono (opcional pero con formato)
        if telefono:
            valid, msg = Validator.validate_phone(telefono)
            if not valid:
                return False, msg
        
        # Validar correo (opcional pero con formato)
        if correo:
            valid, msg = Validator.validate_email(correo)
            if not valid:
                return False, msg
        
        return True, ""
    
    @staticmethod
    def crear_cliente(nombre, telefono, correo, direccion):
        """
        Crea un nuevo cliente después de validar los datos
        
        Returns:
            tuple: (success, id_cliente/error_message)
        """
        # Validar datos
        valid, msg = ClienteController.validar_datos_cliente(nombre, telefono, correo, direccion)
        if not valid:
            return False, msg
        
        # Crear el cliente
        return ClienteModel.crear_cliente(nombre, telefono, correo, direccion)
    
    @staticmethod
    def actualizar_cliente(id_cliente, nombre, telefono, correo, direccion):
        """
        Actualiza un cliente existente después de validar los datos
        
        Returns:
            tuple: (success, message)
        """
        # Validar datos
        valid, msg = ClienteController.validar_datos_cliente(nombre, telefono, correo, direccion)
        if not valid:
            return False, msg
        
        # Actualizar el cliente
        return ClienteModel.actualizar_cliente(id_cliente, nombre, telefono, correo, direccion)
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los clientes"""
        return ClienteModel.obtener_todos()
    
    @staticmethod
    def obtener_por_id(id_cliente):
        """Obtiene un cliente por ID"""
        return ClienteModel.obtener_por_id(id_cliente)
    
    @staticmethod
    def eliminar_cliente(id_cliente):
        """Elimina un cliente"""
        return ClienteModel.eliminar_cliente(id_cliente)
    
    @staticmethod
    def buscar_clientes(criterio):
        """Busca clientes por criterio"""
        return ClienteModel.buscar_clientes(criterio)
