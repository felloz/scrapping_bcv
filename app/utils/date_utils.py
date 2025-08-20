import datetime
import re

def format_date_to_custom(date_obj):
    """
    Convierte un objeto datetime al formato personalizado "24/08/2025, 12:10 AM"
    """
    if isinstance(date_obj, str):
        try:
            date_obj = datetime.datetime.strptime(date_obj, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            try:
                date_obj = datetime.datetime.strptime(date_obj, '%Y-%m-%d %H:%M')
            except ValueError:
                date_obj = datetime.datetime.now()
    
    return date_obj.strftime('%d/%m/%Y, %I:%M %p')

def parse_custom_date(date_str):
    """
    Convierte una fecha en formato "24/08/2025, 12:10 AM" a objeto datetime
    """
    if not date_str:
        return datetime.datetime.now()
    
    try:
        # Manejar formato "24/08/2025, 12:10 AM"
        return datetime.datetime.strptime(date_str, '%d/%m/%Y, %I:%M %p')
    except ValueError:
        try:
            # Fallback para otros formatos
            return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M')
        except ValueError:
            return datetime.datetime.now()

def get_current_date_custom():
    """
    Obtiene la fecha actual en formato personalizado
    """
    return datetime.datetime.now().strftime('%d/%m/%Y, %I:%M %p')

def parse_bcv_date(fecha_str):
    """
    Parsea fechas del BCV al formato personalizado
    """
    if not fecha_str:
        return get_current_date_custom()
    
    # Mapeo de meses en español a números
    meses_spanish = {
        'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
        'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
        'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
    }
    
    try:
        # Limpiar la fecha (remover día de la semana y comas, normalizar espacios)
        fecha_limpia = re.sub(r'^[A-Za-z]+,\s*', '', fecha_str)  # Remover "Lunes, "
        fecha_limpia = re.sub(r'\s+', ' ', fecha_limpia).strip()  # Normalizar espacios múltiples
        
        # Extraer día, mes y año usando regex
        match = re.match(r'([0-9]{1,2})\s+([A-Za-z]+)\s+([0-9]{4})', fecha_limpia)
        
        if match:
            dia = match.group(1).zfill(2)
            mes_texto = match.group(2).lower()
            anio = match.group(3)
            
            # Convertir mes de texto a número
            mes_num = meses_spanish.get(mes_texto)
            
            if mes_num:
                # Crear objeto datetime y convertir al formato personalizado
                fecha_dt = datetime.datetime(int(anio), int(mes_num), int(dia), 12, 0)
                return format_date_to_custom(fecha_dt)
        
        return get_current_date_custom()
        
    except Exception as e:
        print(f"Error parseando fecha BCV: {e}")
        return get_current_date_custom()
