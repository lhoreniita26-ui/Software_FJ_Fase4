'''Servicios con impuesto y descuento opcionales expresados de 0 a 1.'''
from abc import abstractmethod
from decimal import Decimal, ROUND_HALF_UP  # Realiza el calculo decimal y define el redondeo a centavos.
from math import isfinite  # Permite descartar NaN e infinitos antes de calcular.

if __package__:  # Admite importar sistema como paquete o ejecutar desde su carpeta.
    from .entidad import Entidad
    from .excepciones import CalculoInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError
else:
    from entidad import Entidad
    from excepciones import CalculoInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError


def _numero_valido(valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float, Decimal)):  # True y False son enteros en Python, pero no son horas ni precios validos.
        return False
    try:
        return isfinite(valor)
    except (ValueError, OverflowError):  # Un numero no representable tampoco se admite como entrada.
        return False


class Servicio(Entidad):
    '''Contrato abstracto de los servicios, con atributos encapsulados.'''

    def __init__(self, nombre, precio_hora, disponible=True):
        super().__init__()
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre  # Normaliza espacios; conserva los tipos incorrectos para que validar() los rechace.
        self.__precio_hora = precio_hora
        self.__disponible = disponible
        self.validar()  # Impide terminar la construccion con una tarifa o un nombre incorrectos.

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio_hora(self):
        return self.__precio_hora

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):  # La disponibilidad admite exclusivamente True o False.
            raise ServicioInvalidoError('La disponibilidad debe ser True o False.')
        self.__disponible = valor

    def validar(self):
        if not isinstance(self.nombre, str) or not self.nombre:
            raise ServicioInvalidoError('El nombre del servicio es obligatorio.')
        if not _numero_valido(self.precio_hora) or self.precio_hora <= 0:  # Las tarifas deben ser positivas y finitas.
            raise ServicioInvalidoError('El precio por hora debe ser positivo y finito.')
        if not isinstance(self.disponible, bool):
            raise ServicioInvalidoError('La disponibilidad debe ser True o False.')
        return True

    def _validar_calculo(self, horas, impuesto, descuento):
        self.validar()  # Impide terminar la construccion con una tarifa o un nombre incorrectos.
        if not self.disponible:  # La disponibilidad se consulta de nuevo en cada calculo.
            raise ServicioNoDisponibleError(f'El servicio {self.nombre} no esta disponible.')
        if not _numero_valido(horas) or horas <= 0:  # No se permiten reservas de duracion nula, negativa o no finita.
            raise CalculoInvalidoError('Las horas deben ser positivas y finitas.')
        for nombre, tasa in (('impuesto', impuesto), ('descuento', descuento)):
            if not _numero_valido(tasa) or not 0 <= tasa <= 1:  # Las tasas son proporciones: 0.19 significa 19 %, no 19.
                raise CalculoInvalidoError(f'El {nombre} debe estar entre 0 y 1.')
        return True

    def _costo_por_horas(self, horas, impuesto, descuento):
        self.validar_parametros(horas, impuesto, descuento)
        try:
            subtotal = Decimal(str(self.precio_hora)) * Decimal(str(horas))  # Convierte desde texto para no incorporar la aproximacion binaria del float.
            total = subtotal * (1 - Decimal(str(descuento))) * (1 + Decimal(str(impuesto)))  # Aplica primero el descuento y despues el impuesto.
            total = float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))  # Redondea al final y conserva el tipo float del contrato grupal.
            if not isfinite(total):
                raise CalculoInvalidoError('El costo calculado no es finito.')
            return total
        except ArithmeticError as error:
            raise CalculoInvalidoError('No se pudo representar el costo calculado.') from error  # Vincula el error de negocio con la causa aritmetica original.

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        '''Calcula el costo con una, dos o tres entradas.'''

    @abstractmethod
    def validar_parametros(self, horas, impuesto=0, descuento=0):
        '''Valida los parametros del servicio concreto.'''


class ReservaSala(Servicio):
    '''Reserva de sala por horas, incluidas fracciones de hora.'''

    def describir(self):
        return f'Sala: {self.nombre} | Precio por hora: {self.precio_hora}'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self._costo_por_horas(horas, impuesto, descuento)


class AlquilerEquipo(Servicio):
    '''Alquiler de equipos segun su tarifa por hora.'''

    def describir(self):
        return f'Equipo: {self.nombre} | Precio por hora: {self.precio_hora}'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self._costo_por_horas(horas, impuesto, descuento)


class Asesoria(Servicio):
    '''Asesoria profesional facturada por horas.'''

    def describir(self):
        return f'Asesoria: {self.nombre} | Precio por hora: {self.precio_hora}'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        return self._costo_por_horas(horas, impuesto, descuento)
