"""Módulo de la clase abstracta base de Software FJ.

Define Entidad, de la que heredan Cliente, Servicio y Reserva.
Cada entidad recibe un identificador único y obliga a sus
subclases a implementar describir() y validar().
"""

# Importa ABC (clase abstracta) y abstractmethod (método abstracto)
from abc import ABC, abstractmethod


# Clase abstracta: no se puede instanciar, solo heredar de ella
class Entidad(ABC):
    """Representa cualquier objeto del sistema que tiene un identificador."""

    # Contador de clase: lleva la cuenta de entidades creadas (1, 2, 3...)
    __contador = 0

    # Constructor: se ejecuta cada vez que se crea una entidad
    def __init__(self):
        # Suma 1 al contador compartido por todas las entidades
        Entidad.__contador += 1
        # Guarda el número como id privado de esta entidad
        self.__id = Entidad.__contador

    # Propiedad: permite leer el id como entidad.id, sin poder modificarlo
    @property
    def id(self):
        """Identificador único de la entidad (solo lectura)."""
        # Devuelve el id privado
        return self.__id

    # Método abstracto: cada subclase debe decir cómo se describe
    @abstractmethod
    def describir(self):
        """Devuelve un texto que describe la entidad."""

    # Método abstracto: cada subclase debe validar sus propios datos
    @abstractmethod
    def validar(self):
        """Valida los datos; lanza una excepción si son inválidos."""
               