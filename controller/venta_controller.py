"""
Controlador para la gestión de ventas
Intermediario entre la vista y el modelo
"""
from model.venta_model import VentaModel
from utils.validators import Validator

class VentaController:
    """Controlador para operaciones de ventas"""
    
    @staticmethod
    def validar_datos_venta(id_auto, id_cliente, monto, metodo_pago):
        """
        Valida los datos de una venta antes de guardar
        
        Returns:
            tuple: (is_valid, error_message)
        """
        # Validar que se haya seleccionado un auto
        if not id_auto or id_auto <= 0:
            return False, "Debe seleccionar un auto"
        
        # Validar que se haya seleccionado un cliente
        if not id_cliente or id_cliente <= 0:
            return False, "Debe seleccionar un cliente"
        
        # Validar monto
        valid, msg = Validator.validate_number(monto, "Monto", min_value=0)
        if not valid:
            return False, msg
        
        # Validar método de pago
        valid, msg = Validator.validate_required(metodo_pago, "Método de pago")
        if not valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def crear_venta(id_auto, id_cliente, monto, metodo_pago, fecha_venta=None):
        """
        Crea una nueva venta después de validar los datos
        
        Returns:
            tuple: (success, id_venta/error_message)
        """
        # Validar datos
        valid, msg = VentaController.validar_datos_venta(id_auto, id_cliente, monto, metodo_pago)
        if not valid:
            return False, msg
        
        # Crear la venta
        return VentaModel.crear_venta(id_auto, id_cliente, monto, metodo_pago, fecha_venta)
    
    @staticmethod
    def actualizar_venta(id_venta, id_auto, id_cliente, monto, metodo_pago, fecha_venta):
        """
        Actualiza una venta existente después de validar los datos
        
        Returns:
            tuple: (success, message)
        """
        # Validar datos
        valid, msg = VentaController.validar_datos_venta(id_auto, id_cliente, monto, metodo_pago)
        if not valid:
            return False, msg
        
        # Actualizar la venta
        return VentaModel.actualizar_venta(id_venta, id_auto, id_cliente, monto, metodo_pago, fecha_venta)
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las ventas"""
        return VentaModel.obtener_todas()
    
    @staticmethod
    def obtener_por_id(id_venta):
        """Obtiene una venta por ID"""
        return VentaModel.obtener_por_id(id_venta)
    
    @staticmethod
    def eliminar_venta(id_venta):
        """Elimina una venta"""
        return VentaModel.eliminar_venta(id_venta)
    
    @staticmethod
    def obtener_ventas_por_cliente(id_cliente):
        """Obtiene ventas de un cliente"""
        return VentaModel.obtener_ventas_por_cliente(id_cliente)
    
    @staticmethod
    def obtener_estadisticas():
        """Obtiene estadísticas de ventas"""
        return VentaModel.obtener_estadisticas()
