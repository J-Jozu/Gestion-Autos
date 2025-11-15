"""
Modelo de datos para la tabla de clientes
Implementa todas las operaciones CRUD
"""
from model.conexion import db

class ClienteModel:
    """Clase para gestionar operaciones CRUD de clientes"""
    
    @staticmethod
    def crear_cliente(nombre, telefono, correo, direccion):
        """
        Crea un nuevo registro de cliente
        
        Returns:
            tuple: (success, id_cliente/error_message)
        """
        query = """
            INSERT INTO clientes (nombre, telefono, correo, direccion)
            VALUES (%s, %s, %s, %s)
        """
        params = (nombre, telefono, correo, direccion)
        return db.execute_query(query, params)
    
    @staticmethod
    def obtener_todos():
        """
        Obtiene todos los clientes registrados
        
        Returns:
            tuple: (success, list_of_clientes/error_message)
        """
        query = "SELECT * FROM clientes ORDER BY nombre"
        return db.fetch_all(query)
    
    @staticmethod
    def obtener_por_id(id_cliente):
        """
        Obtiene un cliente por su ID
        
        Returns:
            tuple: (success, cliente_data/error_message)
        """
        query = "SELECT * FROM clientes WHERE id_cliente = %s"
        return db.fetch_one(query, (id_cliente,))
    
    @staticmethod
    def actualizar_cliente(id_cliente, nombre, telefono, correo, direccion):
        """
        Actualiza los datos de un cliente existente
        
        Returns:
            tuple: (success, message)
        """
        query = """
            UPDATE clientes 
            SET nombre=%s, telefono=%s, correo=%s, direccion=%s
            WHERE id_cliente=%s
        """
        params = (nombre, telefono, correo, direccion, id_cliente)
        return db.execute_query(query, params)
    
    @staticmethod
    def eliminar_cliente(id_cliente):
        """
        Elimina un cliente por su ID
        
        Returns:
            tuple: (success, message)
        """
        query = "DELETE FROM clientes WHERE id_cliente = %s"
        return db.execute_query(query, (id_cliente,))
    
    @staticmethod
    def buscar_clientes(criterio):
        """
        Busca clientes por nombre, teléfono o correo
        
        Returns:
            tuple: (success, list_of_clientes/error_message)
        """
        query = """
            SELECT * FROM clientes 
            WHERE nombre LIKE %s OR telefono LIKE %s OR correo LIKE %s
            ORDER BY nombre
        """
        search_term = f"%{criterio}%"
        return db.fetch_all(query, (search_term, search_term, search_term))
