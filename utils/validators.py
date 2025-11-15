"""
Validadores de datos para formularios
"""
import re
from datetime import datetime

class Validator:
    """Clase con métodos estáticos para validación de datos"""
    
    @staticmethod
    def validate_required(value, field_name):
        """Valida que un campo no esté vacío"""
        if not value or str(value).strip() == "":
            return False, f"El campo {field_name} es obligatorio"
        return True, ""
    
    @staticmethod
    def validate_number(value, field_name, min_value=None, max_value=None):
        """Valida que un valor sea numérico"""
        try:
            num = float(value)
            if min_value is not None and num < min_value:
                return False, f"{field_name} debe ser mayor o igual a {min_value}"
            if max_value is not None and num > max_value:
                return False, f"{field_name} debe ser menor o igual a {max_value}"
            return True, ""
        except ValueError:
            return False, f"{field_name} debe ser un número válido"
    
    @staticmethod
    def validate_year(value):
        """Valida que el año sea válido"""
        try:
            year = int(value)
            current_year = datetime.now().year
            if year < 1900 or year > current_year + 1:
                return False, f"El año debe estar entre 1900 y {current_year + 1}"
            return True, ""
        except ValueError:
            return False, "El año debe ser un número válido"
    
    @staticmethod
    def validate_email(value):
        """Valida formato de correo electrónico"""
        if not value:
            return True, ""  # Email es opcional
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, value):
            return True, ""
        return False, "Formato de correo electrónico inválido"
    
    @staticmethod
    def validate_phone(value):
        """Valida formato de teléfono"""
        if not value:
            return True, ""  # Teléfono es opcional
        # Acepta números, espacios, guiones y paréntesis
        pattern = r'^[\d\s\-$$$$]+$'
        if re.match(pattern, value) and len(value) >= 7:
            return True, ""
        return False, "Formato de teléfono inválido"
