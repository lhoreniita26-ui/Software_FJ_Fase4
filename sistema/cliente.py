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
    
    # Método abstracto de Entidad: valida nombre, documento y correo
    def validar(self):
        """Verifica los datos; lanza ClienteInvalidoError si alguno es inválido."""
        # El nombre debe ser texto y no estar vacío
        if not isinstance(self.__nombre, str) or not self.__nombre:
            # Lanza el error personalizado con un mensaje claro
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        # Sin contar los espacios, el nombre debe tener solo letras (admite tildes y ñ)
        if not self.__nombre.replace(" ", "").isalpha():
            # Lanza el error si hay números o símbolos en el nombre
            raise ClienteInvalidoError("El nombre solo puede contener letras.")
        # El documento debe ser texto y contener solo dígitos
        if not isinstance(self.__documento, str) or not self.__documento.isdigit():
            # Lanza el error si no es texto o tiene caracteres que no son números
            raise ClienteInvalidoError("El documento debe contener solo números.")
        # El documento debe tener entre 6 y 10 dígitos
        if len(self.__documento) < 6 or len(self.__documento) > 10:
            # Lanza el error si la longitud está fuera del rango permitido
            raise ClienteInvalidoError("El documento debe tener entre 6 y 10 dígitos.")
        # El correo debe ser texto y tener exactamente una arroba
        if not isinstance(self.__correo, str) or self.__correo.count("@") != 1:
            # Lanza el error si no es texto o la cantidad de arrobas no es 1
            raise ClienteInvalidoError("El correo debe tener una sola arroba (@).")
        # Separa el correo en la parte antes y después de la arroba
        usuario, dominio = self.__correo.split("@")
        # El usuario no puede estar vacío y el dominio debe contener un punto
        if not usuario or "." not in dominio:
            # Lanza el error si falta el usuario o el punto del dominio
            raise ClienteInvalidoError("El correo no tiene un formato válido.")
        # Si pasó todas las validaciones, indica que los datos son correctos
        return True
    
    # Método abstracto de Entidad: devuelve el resumen del cliente
    def describir(self):
        """Resumen del cliente."""
        # Arma el texto con id, nombre, documento y correo
        return f"[{self.id}] {self.__nombre} - Doc: {self.__documento} - {self.__correo}"