from enum import Enum

class TipoRelevo(str, Enum):
    SUBIDA = "Subida"
    DESCIDA = "Descida"
    PLANO = "Plano"
class ColorByRelevo(str, Enum):
    SUBIDA = "#E74C3C"    
    DESCIDA = "#1D8348"  
    PLANO = "#3498DB"      
