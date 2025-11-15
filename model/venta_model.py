"""
Modelo de datos para la tabla de ventas
Implementa todas las operaciones CRUD
"""
from model.conexion import db

class VentaModel:
    """Clase para gestionar operaciones CRUD de ventas"""
    
    @staticmethod
    def crear_venta(id_auto, id_cliente, monto, metodo_pago, fecha_venta=None):
        """
        Crea un nuevo registro de venta
        
        Returns:
            tuple: (success, id_venta/error_message)
        """
        if fecha_venta:
            query = """
                INSERT INTO ventas (id_auto, id_cliente, monto, metodo_pago, fecha_venta)
                VALUES (%s, %s, %s, %s, %s)
            """
            params = (id_auto, id_cliente, monto, metodo_pago, fecha_venta)
        else:
            query = """
                INSERT INTO ventas (id_auto, id_cliente, monto, metodo_pago)
                VALUES (%s, %s, %s, %s)
            """
            params = (id_auto, id_cliente, monto, metodo_pago)
        
        return db.execute_query(query, params)
    
    @staticmethod
    def obtener_todas():
        """
        Obtiene todas las ventas con información de autos y clientes
        
        Returns:
            tuple: (success, list_of_ventas/error_message)
        """
        query = """
            SELECT v.*, 
                   a.marca as auto_marca, a.modelo as auto_modelo, 
                   a.anio as auto_anio, a.color as auto_color, a.imagen as auto_imagen,
                   c.nombre as cliente_nombre, c.telefono as cliente_telefono,
                   c.correo as cliente_correo, c.direccion as cliente_direccion
            FROM ventas v
            INNER JOIN autos a ON v.id_auto = a.id_auto
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            ORDER BY v.fecha_venta DESC
        """
        return db.fetch_all(query)
    
    @staticmethod
    def obtener_por_id(id_venta):
        """
        Obtiene una venta por su ID con información completa
        
        Returns:
            tuple: (success, venta_data/error_message)
        """
        query = """
            SELECT v.*, 
                   a.marca as auto_marca, a.modelo as auto_modelo, 
                   a.anio as auto_anio, a.color as auto_color, a.imagen as auto_imagen,
                   a.precio as auto_precio, a.transmision as auto_transmision,
                   a.combustible as auto_combustible,
                   c.nombre as cliente_nombre, c.telefono as cliente_telefono,
                   c.correo as cliente_correo, c.direccion as cliente_direccion
            FROM ventas v
            INNER JOIN autos a ON v.id_auto = a.id_auto
            INNER JOIN clientes c ON v.id_cliente = c.id_cliente
            WHERE v.id_venta = %s
        """
        return db.fetch_one(query, (id_venta,))
    
    @staticmethod
    def actualizar_venta(id_venta, id_auto, id_cliente, monto, metodo_pago, fecha_venta):
        """
        Actualiza los datos de una venta existente
        
        Returns:
            tuple: (success, message)
        """
        query = """
            UPDATE ventas 
            SET id_auto=%s, id_cliente=%s, monto=%s, metodo_pago=%s, fecha_venta=%s
            WHERE id_venta=%s
        """
        params = (id_auto, id_cliente, monto, metodo_pago, fecha_venta, id_venta)
        return db.execute_query(query, params)
    
    @staticmethod
    def eliminar_venta(id_venta):
        """
        Elimina una venta por su ID
        
        Returns:
            tuple: (success, message)
        """
        query = "DELETE FROM ventas WHERE id_venta = %s"
        return db.execute_query(query, (id_venta,))
    
    @staticmethod
    def obtener_ventas_por_cliente(id_cliente):
        """
        Obtiene todas las ventas de un cliente específico
        
        Returns:
            tuple: (success, list_of_ventas/error_message)
        """
        query = """
            SELECT v.*, 
                   a.marca as auto_marca, a.modelo as auto_modelo, 
                   a.anio as auto_anio, a.color as auto_color
            FROM ventas v
            INNER JOIN autos a ON v.id_auto = a.id_auto
            WHERE v.id_cliente = %s
            ORDER BY v.fecha_venta DESC
        """
        return db.fetch_all(query, (id_cliente,))
    
    @staticmethod
    def obtener_estadisticas():
        """
        Obtiene estadísticas generales de ventas
        
        Returns:
            tuple: (success, stats_data/error_message)
        """
        query = """
            SELECT 
                COUNT(*) as total_ventas,
                SUM(monto) as monto_total,
                AVG(monto) as monto_promedio,
                MAX(monto) as venta_mayor,
                MIN(monto) as venta_menor
            FROM ventas
        """
        return db.fetch_one(query)
