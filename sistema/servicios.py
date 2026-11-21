'''Servicios con impuesto y descuento opcionales expresados de 0 a 1.'''
from abc import abstractmethod  # Importa las clases o funciones utilizadas por el modulo.
from decimal import Decimal, ROUND_HALF_UP  # Importa las clases o funciones utilizadas por el modulo.
from math import isfinite  # Importa las clases o funciones utilizadas por el modulo.

if __package__:  # Selecciona imports relativos al usar sistema como paquete.
    from .entidad import Entidad  # Importa las clases o funciones utilizadas por el modulo.
    from .excepciones import CalculoInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError  # Importa las clases o funciones utilizadas por el modulo.
else:  # Ejecuta la alternativa o el bloque posterior al exito, segun el try o if precedente.
    from entidad import Entidad  # Importa las clases o funciones utilizadas por el modulo.
    from excepciones import CalculoInvalidoError, ServicioInvalidoError, ServicioNoDisponibleError  # Importa las clases o funciones utilizadas por el modulo.


def _numero_valido(valor):  # Implementa _numero_valido con los parametros del contrato.
    if isinstance(valor, bool) or not isinstance(valor, (int, float, Decimal)):  # Comprueba la condicion antes de aceptar los datos o la operacion.
        return False  # Devuelve el dato o el resultado validado al llamador.
    try:  # Protege la operacion que puede lanzar una excepcion.
        return isfinite(valor)  # Devuelve el dato o el resultado validado al llamador.
    except (ValueError, OverflowError):  # Controla el tipo de error indicado sin ocultar otros tipos.
        return False  # Devuelve el dato o el resultado validado al llamador.


class Servicio(Entidad):  # Define Servicio(Entidad) y su responsabilidad en el modelo.
    '''Contrato abstracto de los servicios, con atributos encapsulados.'''

    def __init__(self, nombre, precio_hora, disponible=True):  # Implementa __init__ con los parametros del contrato.
        super().__init__()  # Inicializa el identificador y los datos heredados.
        self.__nombre = nombre.strip() if isinstance(nombre, str) else nombre  # Actualiza el atributo privado despues de las validaciones previas.
        self.__precio_hora = precio_hora  # Actualiza el atributo privado despues de las validaciones previas.
        self.__disponible = disponible  # Actualiza el atributo privado despues de las validaciones previas.
        self.validar()  # Verifica la integridad de los datos antes de continuar.

    @property  # Permite consultar el atributo mediante una propiedad.
    def nombre(self):  # Implementa nombre con los parametros del contrato.
        return self.__nombre  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def precio_hora(self):  # Implementa precio_hora con los parametros del contrato.
        return self.__precio_hora  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def disponible(self):  # Implementa disponible con los parametros del contrato.
        return self.__disponible  # Devuelve el dato o el resultado validado al llamador.

    @disponible.setter  # Asocia este metodo a la propiedad indicada.
    def disponible(self, valor):  # Implementa disponible con los parametros del contrato.
        if not isinstance(valor, bool):  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioInvalidoError('La disponibilidad debe ser True o False.')  # Comunica el error y detiene solamente esta operacion.
        self.__disponible = valor  # Actualiza el atributo privado despues de las validaciones previas.

    def validar(self):  # Implementa validar con los parametros del contrato.
        if not isinstance(self.nombre, str) or not self.nombre:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioInvalidoError('El nombre del servicio es obligatorio.')  # Comunica el error y detiene solamente esta operacion.
        if not _numero_valido(self.precio_hora) or self.precio_hora <= 0:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioInvalidoError('El precio por hora debe ser positivo y finito.')  # Comunica el error y detiene solamente esta operacion.
        if not isinstance(self.disponible, bool):  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioInvalidoError('La disponibilidad debe ser True o False.')  # Comunica el error y detiene solamente esta operacion.
        return True  # Devuelve el dato o el resultado validado al llamador.

    def _validar_calculo(self, horas, impuesto, descuento):  # Implementa _validar_calculo con los parametros del contrato.
        self.validar()  # Verifica la integridad de los datos antes de continuar.
        if not self.disponible:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioNoDisponibleError(f'El servicio {self.nombre} no esta disponible.')  # Comunica el error y detiene solamente esta operacion.
        if not _numero_valido(horas) or horas <= 0:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise CalculoInvalidoError('Las horas deben ser positivas y finitas.')  # Comunica el error y detiene solamente esta operacion.
        for nombre, tasa in (('impuesto', impuesto), ('descuento', descuento)):  # Recorre los parametros o casos que comparten la misma validacion.
            if not _numero_valido(tasa) or not 0 <= tasa <= 1:  # Comprueba la condicion antes de aceptar los datos o la operacion.
                raise CalculoInvalidoError(f'El {nombre} debe estar entre 0 y 1.')  # Comunica el error y detiene solamente esta operacion.
        return True  # Devuelve el dato o el resultado validado al llamador.

    def _costo_por_horas(self, horas, impuesto, descuento):  # Implementa _costo_por_horas con los parametros del contrato.
        self.validar_parametros(horas, impuesto, descuento)  # Prepara los datos o completa la comprobacion del bloque actual.
        try:  # Protege la operacion que puede lanzar una excepcion.
            subtotal = Decimal(str(self.precio_hora)) * Decimal(str(horas))  # Calcula la tarifa por horas con aritmetica decimal.
            total = subtotal * (1 - Decimal(str(descuento))) * (1 + Decimal(str(impuesto)))  # Calcula o redondea el importe final antes de devolverlo.
            total = float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))  # Calcula o redondea el importe final antes de devolverlo.
            if not isfinite(total):  # Comprueba la condicion antes de aceptar los datos o la operacion.
                raise CalculoInvalidoError('El costo calculado no es finito.')  # Comunica el error y detiene solamente esta operacion.
            return total  # Devuelve el dato o el resultado validado al llamador.
        except ArithmeticError as error:  # Controla el tipo de error indicado sin ocultar otros tipos.
            raise CalculoInvalidoError('No se pudo representar el costo calculado.') from error  # Lanza el error de dominio conservando la causa original.

    @abstractmethod  # Obliga a las clases concretas a implementar este metodo.
    def calcular_costo(self, horas, impuesto=0, descuento=0):  # Implementa calcular_costo con los parametros del contrato.
        '''Calcula el costo con una, dos o tres entradas.'''

    @abstractmethod  # Obliga a las clases concretas a implementar este metodo.
    def validar_parametros(self, horas, impuesto=0, descuento=0):  # Implementa validar_parametros con los parametros del contrato.
        '''Valida los parametros del servicio concreto.'''


class ReservaSala(Servicio):  # Define ReservaSala(Servicio) y su responsabilidad en el modelo.
    '''Reserva de sala por horas, incluidas fracciones de hora.'''

    def describir(self):  # Implementa describir con los parametros del contrato.
        return f'Sala: {self.nombre} | Precio por hora: {self.precio_hora}'  # Devuelve el dato o el resultado validado al llamador.

    def validar_parametros(self, horas, impuesto=0, descuento=0):  # Implementa validar_parametros con los parametros del contrato.
        return self._validar_calculo(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.

    def calcular_costo(self, horas, impuesto=0, descuento=0):  # Implementa calcular_costo con los parametros del contrato.
        return self._costo_por_horas(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.


class AlquilerEquipo(Servicio):  # Define AlquilerEquipo(Servicio) y su responsabilidad en el modelo.
    '''Alquiler de equipos segun su tarifa por hora.'''

    def describir(self):  # Implementa describir con los parametros del contrato.
        return f'Equipo: {self.nombre} | Precio por hora: {self.precio_hora}'  # Devuelve el dato o el resultado validado al llamador.

    def validar_parametros(self, horas, impuesto=0, descuento=0):  # Implementa validar_parametros con los parametros del contrato.
        return self._validar_calculo(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.

    def calcular_costo(self, horas, impuesto=0, descuento=0):  # Implementa calcular_costo con los parametros del contrato.
        return self._costo_por_horas(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.


class Asesoria(Servicio):  # Define Asesoria(Servicio) y su responsabilidad en el modelo.
    '''Asesoria profesional facturada por horas.'''

    def describir(self):  # Implementa describir con los parametros del contrato.
        return f'Asesoria: {self.nombre} | Precio por hora: {self.precio_hora}'  # Devuelve el dato o el resultado validado al llamador.

    def validar_parametros(self, horas, impuesto=0, descuento=0):  # Implementa validar_parametros con los parametros del contrato.
        return self._validar_calculo(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.

    def calcular_costo(self, horas, impuesto=0, descuento=0):  # Implementa calcular_costo con los parametros del contrato.
        return self._costo_por_horas(horas, impuesto, descuento)  # Devuelve el dato o el resultado validado al llamador.
