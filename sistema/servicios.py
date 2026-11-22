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
        self.validar()  # Revalida tambien los cargos de la especialidad.
        if not self.disponible:  # La disponibilidad se consulta de nuevo en cada calculo.
            raise ServicioNoDisponibleError(f'El servicio {self.nombre} no esta disponible.')
        if not _numero_valido(horas) or horas <= 0:  # No se permiten reservas de duracion nula, negativa o no finita.
            raise CalculoInvalidoError('Las horas deben ser positivas y finitas.')
        for nombre, tasa in (('impuesto', impuesto), ('descuento', descuento)):
            if not _numero_valido(tasa) or not 0 <= tasa <= 1:  # Las tasas son proporciones: 0.19 significa 19 %, no 19.
                raise CalculoInvalidoError(f'El {nombre} debe estar entre 0 y 1.')
        return True

    def _costo_por_horas(self, horas, impuesto, descuento, ajustar_subtotal=None):
        self.validar_parametros(horas, impuesto, descuento)
        try:
            subtotal = Decimal(str(self.precio_hora)) * Decimal(str(horas))  # Convierte desde texto para no incorporar la aproximacion binaria del float.
            if ajustar_subtotal is not None:
                subtotal = ajustar_subtotal(subtotal)  # Aplica la regla concreta dentro del manejo de errores aritmeticos.
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
    '''Sala por horas con un cargo de limpieza fijo por reserva.'''

    def __init__(self, nombre, precio_hora, disponible=True, *, cargo_limpieza=0):
        self.__cargo_limpieza = cargo_limpieza
        super().__init__(nombre, precio_hora, disponible)

    @property
    def cargo_limpieza(self):
        return self.__cargo_limpieza

    def validar(self):
        super().validar()
        if not _numero_valido(self.cargo_limpieza) or self.cargo_limpieza < 0:
            raise ServicioInvalidoError('El cargo de limpieza debe ser no negativo y finito.')
        return True

    def describir(self):
        return f'Sala: {self.nombre} | Precio por hora: {self.precio_hora} | Limpieza fija: {self.cargo_limpieza}'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # La limpieza se suma una sola vez, antes del descuento y del impuesto.
        return self._costo_por_horas(
            horas, impuesto, descuento,
            ajustar_subtotal=lambda base: base + Decimal(str(self.cargo_limpieza)),
        )


class AlquilerEquipo(Servicio):
    '''Alquiler por horas con seguro proporcional al valor del alquiler.'''

    def __init__(self, nombre, precio_hora, disponible=True, *, tasa_seguro=0):
        self.__tasa_seguro = tasa_seguro
        super().__init__(nombre, precio_hora, disponible)

    @property
    def tasa_seguro(self):
        return self.__tasa_seguro

    def validar(self):
        super().validar()
        if not _numero_valido(self.tasa_seguro) or not 0 <= self.tasa_seguro <= 1:
            raise ServicioInvalidoError('La tasa del seguro debe estar entre 0 y 1.')
        return True

    def describir(self):
        return f'Equipo: {self.nombre} | Precio por hora: {self.precio_hora} | Tasa de seguro: {self.tasa_seguro}'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # El seguro crece con el valor del alquiler, antes de descuento e impuesto.
        return self._costo_por_horas(
            horas, impuesto, descuento,
            ajustar_subtotal=lambda base: base * (1 + Decimal(str(self.tasa_seguro))),
        )


class Asesoria(Servicio):
    '''Asesoria por horas cuyo recargo depende del nivel profesional.'''

    __RECARGOS = {'basico': Decimal('0'), 'intermedio': Decimal('0.15'), 'avanzado': Decimal('0.30')}

    def __init__(self, nombre, precio_hora, disponible=True, *, nivel='basico'):
        self.__nivel = nivel.strip().casefold().replace('á', 'a') if isinstance(nivel, str) else nivel
        super().__init__(nombre, precio_hora, disponible)

    @property
    def nivel(self):
        return self.__nivel

    @property
    def recargo_nivel(self):
        return self.__RECARGOS[self.nivel]

    def validar(self):
        super().validar()
        if not isinstance(self.nivel, str) or self.nivel not in self.__RECARGOS:
            raise ServicioInvalidoError('El nivel debe ser basico, intermedio o avanzado.')
        return True

    def describir(self):
        return f'Asesoria: {self.nombre} | Precio por hora: {self.precio_hora} | Nivel: {self.nivel} | Recargo: {self.recargo_nivel * 100}%'

    def validar_parametros(self, horas, impuesto=0, descuento=0):
        return self._validar_calculo(horas, impuesto, descuento)

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        # Cada nivel aplica su porcentaje sobre las horas de asesoria contratadas.
        return self._costo_por_horas(
            horas, impuesto, descuento,
            ajustar_subtotal=lambda base: base * (1 + self.recargo_nivel),
        )
