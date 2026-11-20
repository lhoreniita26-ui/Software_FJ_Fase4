"""Módulo de excepciones personalizadas de Software FJ.

Define una jerarquía propia para distinguir los errores del negocio
de los errores genéricos de Python.
"""


class SoftwareFJError(Exception):
    """Excepción base del sistema; todas las demás heredan de ella."""

    def __init__(self, mensaje="Error en Software FJ"):
        # Se guarda el mensaje para poder mostrarlo o registrarlo después
        self.mensaje = mensaje
        # Se llama al constructor de Exception para que str(error) funcione
        super().__init__(mensaje)


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando un servicio se crea con datos incorrectos."""