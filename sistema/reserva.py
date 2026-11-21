'''Reservas con validacion, transiciones de estado y registro de eventos.'''
if __package__:  # Selecciona imports relativos al usar sistema como paquete.
    from .entidad import Entidad  # Importa las clases o funciones utilizadas por el modulo.
    from .servicios import Servicio, _numero_valido  # Importa las clases o funciones utilizadas por el modulo.
    from .excepciones import SoftwareFJError, ReservaInvalidaError, OperacionNoPermitidaError, ServicioNoDisponibleError  # Importa las clases o funciones utilizadas por el modulo.
    from .logger import registrar_evento, registrar_error  # Importa las clases o funciones utilizadas por el modulo.
else:  # Ejecuta la alternativa o el bloque posterior al exito, segun el try o if precedente.
    from entidad import Entidad  # Importa las clases o funciones utilizadas por el modulo.
    from servicios import Servicio, _numero_valido  # Importa las clases o funciones utilizadas por el modulo.
    from excepciones import SoftwareFJError, ReservaInvalidaError, OperacionNoPermitidaError, ServicioNoDisponibleError  # Importa las clases o funciones utilizadas por el modulo.
    from logger import registrar_evento, registrar_error  # Importa las clases o funciones utilizadas por el modulo.


class Reserva(Entidad):  # Define Reserva(Entidad) y su responsabilidad en el modelo.
    '''Flujo: pendiente -> confirmada -> procesada; cancelacion antes de procesar.'''

    def __init__(self, cliente, servicio, horas):  # Implementa __init__ con los parametros del contrato.
        super().__init__()  # Inicializa el identificador y los datos heredados.
        self.__cliente = cliente  # Actualiza el atributo privado despues de las validaciones previas.
        self.__servicio = servicio  # Actualiza el atributo privado despues de las validaciones previas.
        self.__horas = horas  # Actualiza el atributo privado despues de las validaciones previas.
        self.__estado = 'pendiente'  # Actualiza el atributo privado despues de las validaciones previas.
        self.__costo_total = None  # Actualiza el atributo privado despues de las validaciones previas.
        try:  # Protege la operacion que puede lanzar una excepcion.
            self.validar()  # Verifica la integridad de los datos antes de continuar.
        except SoftwareFJError as error:  # Controla el tipo de error indicado sin ocultar otros tipos.
            registrar_error(f'Reserva {self.id}: creacion rechazada: {error}')  # Registra el motivo del rechazo mediante el logger compartido.
            raise  # Propaga la excepcion original despues de registrarla.
        registrar_evento(f'Reserva {self.id} creada en estado pendiente.')  # Registra el resultado o el cierre del intento con el logger compartido.

    @property  # Permite consultar el atributo mediante una propiedad.
    def cliente(self):  # Implementa cliente con los parametros del contrato.
        return self.__cliente  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def servicio(self):  # Implementa servicio con los parametros del contrato.
        return self.__servicio  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def horas(self):  # Implementa horas con los parametros del contrato.
        return self.__horas  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def estado(self):  # Implementa estado con los parametros del contrato.
        return self.__estado  # Devuelve el dato o el resultado validado al llamador.

    @property  # Permite consultar el atributo mediante una propiedad.
    def costo_total(self):  # Implementa costo_total con los parametros del contrato.
        return self.__costo_total  # Devuelve el dato o el resultado validado al llamador.

    def validar(self):  # Implementa validar con los parametros del contrato.
        # Cliente sera aportado por otro modulo; se comprueba el contrato comun.
        if not isinstance(self.cliente, Entidad):  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ReservaInvalidaError('La reserva requiere un cliente valido.')  # Comunica el error y detiene solamente esta operacion.
        if self.cliente.validar() is False:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ReservaInvalidaError('El cliente no supero la validacion.')  # Comunica el error y detiene solamente esta operacion.
        if not all(  # Comprueba la condicion antes de aceptar los datos o la operacion.
            isinstance(getattr(self.cliente, atributo, None), str)  # Prepara los datos o completa la comprobacion del bloque actual.
            and getattr(self.cliente, atributo).strip()  # Prepara los datos o completa la comprobacion del bloque actual.
            for atributo in ('nombre', 'documento', 'correo')  # Recorre los parametros o casos que comparten la misma validacion.
        ):  # Completa la expresion o los datos del bloque anterior.
            raise ReservaInvalidaError('La reserva requiere un cliente valido.')  # Comunica el error y detiene solamente esta operacion.
        if not isinstance(self.servicio, Servicio):  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ReservaInvalidaError('La reserva requiere un servicio valido.')  # Comunica el error y detiene solamente esta operacion.
        self.servicio.validar()  # Revalida el servicio asociado a la reserva.
        if not _numero_valido(self.horas) or self.horas <= 0:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ReservaInvalidaError('Las horas deben ser positivas y finitas.')  # Comunica el error y detiene solamente esta operacion.
        return True  # Devuelve el dato o el resultado validado al llamador.

    def describir(self):  # Implementa describir con los parametros del contrato.
        return (  # Devuelve el dato o el resultado validado al llamador.
            f'Reserva {self.id} | Cliente: {self.cliente.nombre} | '  # Prepara los datos o completa la comprobacion del bloque actual.
            f'Servicio: {self.servicio.nombre} | Horas: {self.horas} | Estado: {self.estado}'  # Prepara los datos o completa la comprobacion del bloque actual.
        )  # Completa la expresion o los datos del bloque anterior.

    def _exigir_estado(self, *permitidos):  # Implementa _exigir_estado con los parametros del contrato.
        if self.estado not in permitidos:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise OperacionNoPermitidaError(f'Operacion no permitida en estado {self.estado}.')  # Comunica el error y detiene solamente esta operacion.

    def _comprobar_disponibilidad(self):  # Implementa _comprobar_disponibilidad con los parametros del contrato.
        if not self.servicio.disponible:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ServicioNoDisponibleError(f'El servicio {self.servicio.nombre} no esta disponible.')  # Comunica el error y detiene solamente esta operacion.

    def confirmar(self):  # Implementa confirmar con los parametros del contrato.
        try:  # Protege la operacion que puede lanzar una excepcion.
            self._exigir_estado('pendiente')  # Impide una transicion no permitida desde el estado actual.
            self.validar()  # Verifica la integridad de los datos antes de continuar.
            self._comprobar_disponibilidad()  # Verifica que el servicio siga disponible.
        except SoftwareFJError as error:  # Controla el tipo de error indicado sin ocultar otros tipos.
            registrar_error(f'Reserva {self.id}: confirmacion rechazada: {error}')  # Registra el motivo del rechazo mediante el logger compartido.
            raise  # Propaga la excepcion original despues de registrarla.
        self.__estado = 'confirmada'  # Actualiza el atributo privado despues de las validaciones previas.
        registrar_evento(f'Reserva {self.id} confirmada.')  # Registra el resultado o el cierre del intento con el logger compartido.

    def cancelar(self):  # Implementa cancelar con los parametros del contrato.
        try:  # Protege la operacion que puede lanzar una excepcion.
            self._exigir_estado('pendiente', 'confirmada')  # Impide una transicion no permitida desde el estado actual.
        except SoftwareFJError as error:  # Controla el tipo de error indicado sin ocultar otros tipos.
            registrar_error(f'Reserva {self.id}: cancelacion rechazada: {error}')  # Registra el motivo del rechazo mediante el logger compartido.
            raise  # Propaga la excepcion original despues de registrarla.
        self.__estado = 'cancelada'  # Actualiza el atributo privado despues de las validaciones previas.
        registrar_evento(f'Reserva {self.id} cancelada.')  # Registra el resultado o el cierre del intento con el logger compartido.

    def procesar(self, impuesto=0, descuento=0):  # Implementa procesar con los parametros del contrato.
        try:  # Protege la operacion que puede lanzar una excepcion.
            self._exigir_estado('confirmada')  # Impide una transicion no permitida desde el estado actual.
            self.validar()  # Verifica la integridad de los datos antes de continuar.
            total = self.servicio.calcular_costo(self.horas, impuesto, descuento)  # Calcula o redondea el importe final antes de devolverlo.
        except SoftwareFJError as error:  # Controla el tipo de error indicado sin ocultar otros tipos.
            registrar_error(f'Reserva {self.id}: procesamiento rechazado: {error}')  # Registra el motivo del rechazo mediante el logger compartido.
            raise  # Propaga la excepcion original despues de registrarla.
        else:  # Ejecuta la alternativa o el bloque posterior al exito, segun el try o if precedente.
            # El costo y el estado cambian solo despues de un calculo exitoso.
            self.__costo_total = total  # Actualiza el atributo privado despues de las validaciones previas.
            self.__estado = 'procesada'  # Actualiza el atributo privado despues de las validaciones previas.
            registrar_evento(f'Reserva {self.id} procesada. Costo total: {total:.2f}.')  # Registra el resultado o el cierre del intento con el logger compartido.
            return total  # Devuelve el dato o el resultado validado al llamador.
        finally:  # Garantiza el registro de cierre aunque la operacion falle.
            registrar_evento(f'Reserva {self.id}: intento de procesamiento finalizado; estado={self.estado}.')  # Registra el resultado o el cierre del intento con el logger compartido.
