"""Módulo de la clase Cliente de Software FJ.

Un cliente guarda sus datos personales de forma privada
y los valida al momento de crearse.
"""

# Importa la clase abstracta de la que hereda Cliente (mismo paquete, por eso el punto)
from .entidad import Entidad
# Importa el error que se lanza cuando un dato del cliente es inválido
from .excepciones import ClienteInvalidoError


# Cliente hereda de Entidad (así obtiene su id)
class Cliente(Entidad):
    """Cliente que puede hacer reservas."""

    # Constructor: recibe los tres datos del cliente
    def __init__(self, nombre, documento, correo):
        # Llama al constructor de Entidad, que asigna el id con el contador
        super().__init__()
        # Guarda el nombre privado; si es texto, le quita espacios sobrantes
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre
        # Guarda el documento privado; si es texto, le quita espacios sobrantes
        self.__documento = documento.strip() if isinstance(documento, str) else documento
        # Guarda el correo privado; si es texto, le quita espacios sobrantes
        self.__correo = correo.strip() if isinstance(correo, str) else correo
        # Valida los datos; si alguno es inválido, lanza ClienteInvalidoError
        self.validar()
        
    # Propiedad para leer el nombre sin poder modificarlo
    @property
    def nombre(self):
        """Nombre del cliente (solo lectura)."""
        # Devuelve el nombre privado
        return self.__nombre

    # Propiedad para leer el documento sin poder modificarlo
    @property
    def documento(self):
        """Documento del cliente (solo lectura)."""
        # Devuelve el documento privado
        return self.__documento

    # Propiedad para leer el correo sin poder modificarlo
    @property
    def correo(self):
        """Correo del cliente (solo lectura)."""
        # Devuelve el correo privado
        return self.__correo
    