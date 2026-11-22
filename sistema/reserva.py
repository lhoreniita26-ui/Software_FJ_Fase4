'''Reservas con validacion, transiciones de estado y registro de eventos.'''
if __package__:  # Los dos estilos de importacion usan el mismo contrato de Entidad y Servicio.
    from .entidad import Entidad
    from .servicios import Servicio, _numero_valido
    from .excepciones import SoftwareFJError, ReservaInvalidaError, OperacionNoPermitidaError, ServicioNoDisponibleError
    from .logger import registrar_evento, registrar_error
else:
    from entidad import Entidad
    from servicios import Servicio, _numero_valido
    from excepciones import SoftwareFJError, ReservaInvalidaError, OperacionNoPermitidaError, ServicioNoDisponibleError
    from logger import registrar_evento, registrar_error


class Reserva(Entidad):
    '''Flujo: pendiente -> confirmada -> procesada; cancelacion antes de procesar.'''

    def __init__(self, cliente, servicio, horas):
        super().__init__()
        self.__cliente = cliente
        self.__servicio = servicio
        self.__horas = horas
        self.__estado = 'pendiente'
        self.__costo_total = None  # None distingue una reserva sin procesar de una con descuento total.
        try:
            self.validar()
        except SoftwareFJError as error:
            registrar_error(f'Reserva {self.id}: creacion rechazada: {error}')
            raise  # Registra y propaga la misma excepcion para que main.py la gestione.
        registrar_evento(f'Reserva {self.id} creada en estado pendiente.')

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def horas(self):
        return self.__horas

    @property
    def estado(self):
        return self.__estado

    @property
    def costo_total(self):
        return self.__costo_total

    def validar(self):

        if not isinstance(self.cliente, Entidad):
            raise ReservaInvalidaError('La reserva requiere un cliente valido.')
        if self.cliente.validar() is False:  # Tambien admite validar() sin retorno explicito si no lanza una excepcion.
            raise ReservaInvalidaError('El cliente no supero la validacion.')
        if not all(
            isinstance(getattr(self.cliente, atributo, None), str)
            and getattr(self.cliente, atributo).strip()
            for atributo in ('nombre', 'documento', 'correo')
        ):
            raise ReservaInvalidaError('La reserva requiere un cliente valido.')
        if not isinstance(self.servicio, Servicio):
            raise ReservaInvalidaError('La reserva requiere un servicio valido.')
        self.servicio.validar()  # Revisa el servicio asociado sin crear ni copiar otro objeto.
        if not _numero_valido(self.horas) or self.horas <= 0:  # Protege la reserva frente a ceros, negativos, booleanos, NaN e infinitos.
            raise ReservaInvalidaError('Las horas deben ser positivas y finitas.')
        return True

    def describir(self):
        return (
            f'Reserva {self.id} | Cliente: {self.cliente.nombre} | '
            f'Servicio: {self.servicio.nombre} | Horas: {self.horas} | Estado: {self.estado}'
        )

    def _exigir_estado(self, *permitidos):
        if self.estado not in permitidos:  # Centraliza las transiciones permitidas para impedir saltos de estado.
            raise OperacionNoPermitidaError(f'Operacion no permitida en estado {self.estado}.')

    def _comprobar_disponibilidad(self):
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError(f'El servicio {self.servicio.nombre} no esta disponible.')

    def confirmar(self):
        try:
            self._exigir_estado('pendiente')
            self.validar()
            self._comprobar_disponibilidad()  # Confirmar no garantiza la disponibilidad futura; procesar() vuelve a comprobarla.
        except SoftwareFJError as error:
            registrar_error(f'Reserva {self.id}: confirmacion rechazada: {error}')
            raise  # Registra y propaga la misma excepcion para que main.py la gestione.
        self.__estado = 'confirmada'
        registrar_evento(f'Reserva {self.id} confirmada.')

    def cancelar(self):
        try:
            self._exigir_estado('pendiente', 'confirmada')  # Una reserva procesada o cancelada no puede cancelarse otra vez.
        except SoftwareFJError as error:
            registrar_error(f'Reserva {self.id}: cancelacion rechazada: {error}')
            raise  # Registra y propaga la misma excepcion para que main.py la gestione.
        self.__estado = 'cancelada'
        registrar_evento(f'Reserva {self.id} cancelada.')

    def procesar(self, impuesto=0, descuento=0):
        try:
            self._exigir_estado('confirmada')
            self.validar()
            total = self.servicio.calcular_costo(self.horas, impuesto, descuento)  # El objeto concreto del servicio resuelve el calculo polimorfico.
        except SoftwareFJError as error:
            registrar_error(f'Reserva {self.id}: procesamiento rechazado: {error}')
            raise  # Registra y propaga la misma excepcion para que main.py la gestione.
        else:

            self.__costo_total = total  # Se ejecuta dentro de else: los errores no asignan un costo parcial.
            self.__estado = 'procesada'  # El cambio de estado ocurre unicamente tras un calculo correcto.
            registrar_evento(f'Reserva {self.id} procesada. Costo total: {total:.2f}.')
            return total
        finally:  # Deja constancia del intento tanto si el calculo termina como si falla.
            registrar_evento(f'Reserva {self.id}: intento de procesamiento finalizado; estado={self.estado}.')
