'''Contrato comun para entidades de Software FJ.'''
from abc import ABC, abstractmethod  # Importa las clases o funciones utilizadas por el modulo.
from uuid import uuid4  # Importa las clases o funciones utilizadas por el modulo.


class Entidad(ABC):  # Define Entidad(ABC) y su responsabilidad en el modelo.
    '''Entidad identificable con descripcion y validacion propias.'''

    def __init__(self, identificador=None):  # Implementa __init__ con los parametros del contrato.
        if identificador is None:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            identificador = str(uuid4())  # Genera un identificador unico cuando no se proporciona uno.
        if isinstance(identificador, bool) or not isinstance(identificador, (str, int)):  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ValueError('El identificador debe ser texto o entero.')  # Comunica el error y detiene solamente esta operacion.
        if isinstance(identificador, str) and not identificador.strip():  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ValueError('El identificador no puede estar vacio.')  # Comunica el error y detiene solamente esta operacion.
        self.__id = identificador  # Actualiza el atributo privado despues de las validaciones previas.

    @property  # Permite consultar el atributo mediante una propiedad.
    def id(self):  # Implementa id con los parametros del contrato.
        return self.__id  # Devuelve el dato o el resultado validado al llamador.

    @abstractmethod  # Obliga a las clases concretas a implementar este metodo.
    def describir(self):  # Implementa describir con los parametros del contrato.
        '''Devuelve una descripcion legible.'''

    @abstractmethod  # Obliga a las clases concretas a implementar este metodo.
    def validar(self):  # Implementa validar con los parametros del contrato.
        '''Lanza una excepcion si los datos son invalidos.'''
