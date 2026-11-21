"""Módulo de excepciones personalizadas de Software FJ.

Define una jerarquía propia para distinguir los errores del negocio
de los errores genéricos de Python.
"""


# Clase padre de todos los errores del sistema
class SoftwareFJError(Exception):
    """Excepción base del sistema; todas las demás heredan de ella."""

    # Constructor: recibe el mensaje del error (tiene uno por defecto)
    def __init__(self, mensaje="Error en Software FJ"):
        # Se guarda el mensaje para poder mostrarlo o registrarlo después
        self.mensaje = mensaje
        # Se llama al constructor de Exception para que str(error) funcione
        super().__init__(mensaje)
        

# Error cuando el nombre, documento o correo del cliente no son válidos
class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


# Error cuando un servicio se crea con nombre o precio incorrectos
class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando un servicio se crea con datos incorrectos."""


# Error al intentar reservar un servicio que no está disponible
class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta usar un servicio marcado como no disponible."""


# Error cuando la reserva no cumple las reglas (ej. horas negativas)
class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva tiene datos inválidos."""


# Error al hacer una acción que el estado no permite (ej. confirmar una cancelada)
class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se pide una operación que el estado actual no permite."""


# Error cuando el impuesto o el descuento del costo no tienen sentido
class CalculoInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un cálculo de costo son incorrectos."""  