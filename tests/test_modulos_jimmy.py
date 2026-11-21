'''Pruebas de contrato; ClientePrueba no reemplaza al cliente de produccion.'''
import math  # Importa las clases o funciones utilizadas por el modulo.
import unittest  # Importa las clases o funciones utilizadas por el modulo.
from decimal import Decimal  # Importa las clases o funciones utilizadas por el modulo.
from unittest.mock import patch  # Importa las clases o funciones utilizadas por el modulo.

from sistema.entidad import Entidad  # Importa las clases o funciones utilizadas por el modulo.
from sistema.excepciones import (  # Importa las clases o funciones utilizadas por el modulo.
    CalculoInvalidoError, ClienteInvalidoError, OperacionNoPermitidaError,  # Prepara los datos o completa la comprobacion del bloque actual.
    ReservaInvalidaError, ServicioInvalidoError, ServicioNoDisponibleError,  # Prepara los datos o completa la comprobacion del bloque actual.
)  # Completa la expresion o los datos del bloque anterior.
from sistema.servicios import Servicio, ReservaSala, AlquilerEquipo, Asesoria  # Importa las clases o funciones utilizadas por el modulo.
from sistema.reserva import Reserva  # Importa las clases o funciones utilizadas por el modulo.


class ClientePrueba(Entidad):  # Define ClientePrueba(Entidad) y su responsabilidad en el modelo.
    def __init__(self):  # Implementa __init__ con los parametros del contrato.
        super().__init__()  # Inicializa el identificador y los datos heredados.
        self.nombre = 'Cliente de prueba'  # Prepara los datos o completa la comprobacion del bloque actual.
        self.documento = '123456'  # Prepara los datos o completa la comprobacion del bloque actual.
        self.correo = 'prueba@example.com'  # Prepara los datos o completa la comprobacion del bloque actual.

    def describir(self):  # Implementa describir con los parametros del contrato.
        return self.nombre  # Devuelve el dato o el resultado validado al llamador.

    def validar(self):  # Implementa validar con los parametros del contrato.
        if not self.correo:  # Comprueba la condicion antes de aceptar los datos o la operacion.
            raise ClienteInvalidoError('Correo obligatorio.')  # Comunica el error y detiene solamente esta operacion.
        return True  # Devuelve el dato o el resultado validado al llamador.


class EntidadTests(unittest.TestCase):  # Define EntidadTests(unittest.TestCase) y su responsabilidad en el modelo.
    def test_contrato_abstracto(self):  # Implementa test_contrato_abstracto con los parametros del contrato.
        with self.assertRaises(TypeError):  # Exige que el caso sea rechazado con la excepcion indicada.
            Entidad()  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(TypeError):  # Exige que el caso sea rechazado con la excepcion indicada.
            Servicio('Generico', 100)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_identificador_unico_y_solo_lectura(self):  # Implementa test_identificador_unico_y_solo_lectura con los parametros del contrato.
        uno, otro = ClientePrueba(), ClientePrueba()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertNotEqual(uno.id, otro.id)  # Comprueba el resultado esperado del escenario.
        with self.assertRaises(AttributeError):  # Exige que el caso sea rechazado con la excepcion indicada.
            uno.id = 'cambio'  # Prepara los datos o completa la comprobacion del bloque actual.


class ServicioTests(unittest.TestCase):  # Define ServicioTests(unittest.TestCase) y su responsabilidad en el modelo.
    def test_tres_formas_de_calculo_y_polimorfismo(self):  # Implementa test_tres_formas_de_calculo_y_polimorfismo con los parametros del contrato.
        for tipo in (ReservaSala, AlquilerEquipo, Asesoria):  # Recorre los parametros o casos que comparten la misma validacion.
            with self.subTest(tipo=tipo.__name__):  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
                servicio = tipo('Servicio', 100)  # Prepara los datos o completa la comprobacion del bloque actual.
                self.assertEqual(servicio.calcular_costo(2), 200)  # Comprueba el resultado esperado del escenario.
                self.assertEqual(servicio.calcular_costo(2, .19), 238)  # Comprueba el resultado esperado del escenario.
                self.assertEqual(servicio.calcular_costo(2, .19, .10), 214.20)  # Comprueba el resultado esperado del escenario.
                self.assertEqual(servicio.calcular_costo(2, descuento=1), 0)  # Comprueba el resultado esperado del escenario.
                self.assertIn('Servicio', servicio.describir())  # Comprueba el resultado esperado del escenario.

    def test_redondeo_monetario_y_fracciones(self):  # Implementa test_redondeo_monetario_y_fracciones con los parametros del contrato.
        self.assertEqual(Asesoria('A', Decimal('10.005')).calcular_costo(1), 10.01)  # Comprueba el resultado esperado del escenario.
        self.assertEqual(ReservaSala('A', 100).calcular_costo(.5), 50)  # Comprueba el resultado esperado del escenario.

    def test_datos_invalidos(self):  # Implementa test_datos_invalidos con los parametros del contrato.
        for nombre, precio, disponible in (  # Recorre los parametros o casos que comparten la misma validacion.
            ('', 10, True), ('  ', 10, True), (None, 10, True),  # Prepara los datos o completa la comprobacion del bloque actual.
            ('A', 0, True), ('A', -1, True), ('A', True, True),  # Prepara los datos o completa la comprobacion del bloque actual.
            ('A', '10', True), ('A', math.nan, True), ('A', math.inf, True),  # Prepara los datos o completa la comprobacion del bloque actual.
            ('A', 10, 1),  # Prepara los datos o completa la comprobacion del bloque actual.
        ):  # Completa la expresion o los datos del bloque anterior.
            with self.subTest(datos=(nombre, precio, disponible)):  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
                with self.assertRaises(ServicioInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
                    ReservaSala(nombre, precio, disponible)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_parametros_invalidos(self):  # Implementa test_parametros_invalidos con los parametros del contrato.
        servicio = Asesoria('A', 100)  # Prepara los datos o completa la comprobacion del bloque actual.
        for parametros in (  # Recorre los parametros o casos que comparten la misma validacion.
            (0,), (-1,), (True,), ('2',), (math.nan,), (math.inf,),  # Prepara los datos o completa la comprobacion del bloque actual.
            (1, -.1), (1, 19), (1, True), (1, math.nan),  # Prepara los datos o completa la comprobacion del bloque actual.
            (1, 0, -.1), (1, 0, 10), (1, 0, False),  # Prepara los datos o completa la comprobacion del bloque actual.
        ):  # Completa la expresion o los datos del bloque anterior.
            with self.subTest(parametros=parametros):  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
                with self.assertRaises(CalculoInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
                    servicio.calcular_costo(*parametros)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_costo_fuera_de_rango(self):  # Implementa test_costo_fuera_de_rango con los parametros del contrato.
        with self.assertRaises(CalculoInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
            Asesoria('A', 1e308).calcular_costo(1e308)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_disponibilidad_validada(self):  # Implementa test_disponibilidad_validada con los parametros del contrato.
        servicio = AlquilerEquipo('A', 100, False)  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(ServicioNoDisponibleError):  # Exige que el caso sea rechazado con la excepcion indicada.
            servicio.calcular_costo(1)  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(ServicioInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
            servicio.disponible = 'si'  # Prepara los datos o completa la comprobacion del bloque actual.
        servicio.disponible = True  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(servicio.calcular_costo(1), 100)  # Comprueba el resultado esperado del escenario.


class ReservaTests(unittest.TestCase):  # Define ReservaTests(unittest.TestCase) y su responsabilidad en el modelo.
    def setUp(self):  # Implementa setUp con los parametros del contrato.
        self.cliente = ClientePrueba()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.servicio = ReservaSala('Sala A', 100)  # Prepara los datos o completa la comprobacion del bloque actual.
        self.reserva = Reserva(self.cliente, self.servicio, 2)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_flujo_correcto_y_encapsulamiento(self):  # Implementa test_flujo_correcto_y_encapsulamiento con los parametros del contrato.
        self.assertEqual(self.reserva.estado, 'pendiente')  # Comprueba el resultado esperado del escenario.
        self.assertIsNone(self.reserva.costo_total)  # Comprueba el resultado esperado del escenario.
        self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'confirmada')  # Comprueba el resultado esperado del escenario.
        self.assertEqual(self.reserva.procesar(.19, .10), 214.20)  # Comprueba el resultado esperado del escenario.
        self.assertEqual(self.reserva.estado, 'procesada')  # Comprueba el resultado esperado del escenario.
        self.assertEqual(self.reserva.costo_total, 214.20)  # Comprueba el resultado esperado del escenario.
        self.assertIn(self.reserva.id, self.reserva.describir())  # Comprueba el resultado esperado del escenario.
        with self.assertRaises(AttributeError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.estado = 'pendiente'  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_no_procesar_sin_confirmar(self):  # Implementa test_no_procesar_sin_confirmar con los parametros del contrato.
        with self.assertRaises(OperacionNoPermitidaError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.procesar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'pendiente')  # Comprueba el resultado esperado del escenario.

    def test_cancelar_pendiente_o_confirmada(self):  # Implementa test_cancelar_pendiente_o_confirmada con los parametros del contrato.
        for confirmar in (False, True):  # Recorre los parametros o casos que comparten la misma validacion.
            with self.subTest(confirmar=confirmar):  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
                reserva = Reserva(self.cliente, self.servicio, 1)  # Prepara los datos o completa la comprobacion del bloque actual.
                if confirmar:  # Comprueba la condicion antes de aceptar los datos o la operacion.
                    reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
                reserva.cancelar()  # Prepara los datos o completa la comprobacion del bloque actual.
                self.assertEqual(reserva.estado, 'cancelada')  # Comprueba el resultado esperado del escenario.
                for accion in (reserva.confirmar, reserva.cancelar, reserva.procesar):  # Recorre los parametros o casos que comparten la misma validacion.
                    with self.assertRaises(OperacionNoPermitidaError):  # Exige que el caso sea rechazado con la excepcion indicada.
                        accion()  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_procesada_es_terminal(self):  # Implementa test_procesada_es_terminal con los parametros del contrato.
        self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.reserva.procesar()  # Prepara los datos o completa la comprobacion del bloque actual.
        for accion in (self.reserva.confirmar, self.reserva.cancelar, self.reserva.procesar):  # Recorre los parametros o casos que comparten la misma validacion.
            with self.assertRaises(OperacionNoPermitidaError):  # Exige que el caso sea rechazado con la excepcion indicada.
                accion()  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_error_calculo_preserva_estado_y_permite_reintento(self):  # Implementa test_error_calculo_preserva_estado_y_permite_reintento con los parametros del contrato.
        self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(CalculoInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.procesar(descuento=2)  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'confirmada')  # Comprueba el resultado esperado del escenario.
        self.assertIsNone(self.reserva.costo_total)  # Comprueba el resultado esperado del escenario.
        self.assertEqual(self.reserva.procesar(), 200)  # Comprueba el resultado esperado del escenario.

    def test_servicio_no_disponible_al_confirmar_o_procesar(self):  # Implementa test_servicio_no_disponible_al_confirmar_o_procesar con los parametros del contrato.
        self.servicio.disponible = False  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(ServicioNoDisponibleError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'pendiente')  # Comprueba el resultado esperado del escenario.
        self.servicio.disponible = True  # Prepara los datos o completa la comprobacion del bloque actual.
        self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.servicio.disponible = False  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(ServicioNoDisponibleError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.procesar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'confirmada')  # Comprueba el resultado esperado del escenario.

    def test_datos_reserva_invalidos(self):  # Implementa test_datos_reserva_invalidos con los parametros del contrato.
        for cliente, servicio, horas in (  # Recorre los parametros o casos que comparten la misma validacion.
            (None, self.servicio, 1), (object(), self.servicio, 1),  # Prepara los datos o completa la comprobacion del bloque actual.
            (self.cliente, None, 1), (self.cliente, self.servicio, 0),  # Prepara los datos o completa la comprobacion del bloque actual.
            (self.cliente, self.servicio, -1), (self.cliente, self.servicio, True),  # Prepara los datos o completa la comprobacion del bloque actual.
            (self.cliente, self.servicio, math.nan),  # Prepara los datos o completa la comprobacion del bloque actual.
        ):  # Completa la expresion o los datos del bloque anterior.
            with self.subTest(horas=horas):  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
                with self.assertRaises(ReservaInvalidaError):  # Exige que el caso sea rechazado con la excepcion indicada.
                    Reserva(cliente, servicio, horas)  # Prepara los datos o completa la comprobacion del bloque actual.

    def test_cliente_se_revalida(self):  # Implementa test_cliente_se_revalida con los parametros del contrato.
        self.cliente.correo = ''  # Prepara los datos o completa la comprobacion del bloque actual.
        with self.assertRaises(ClienteInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
            self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertEqual(self.reserva.estado, 'pendiente')  # Comprueba el resultado esperado del escenario.

    def test_registro_de_exito_y_error(self):  # Implementa test_registro_de_exito_y_error con los parametros del contrato.
        with patch('sistema.reserva.registrar_evento') as evento:  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
            self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
            evento.assert_called_once()  # Prepara los datos o completa la comprobacion del bloque actual.
        with patch('sistema.reserva.registrar_error') as error:  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
            with self.assertRaises(OperacionNoPermitidaError):  # Exige que el caso sea rechazado con la excepcion indicada.
                self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
            error.assert_called_once()  # Prepara los datos o completa la comprobacion del bloque actual.


    def test_finally_registra_cierre_con_exito_y_error(self):  # Implementa test_finally_registra_cierre_con_exito_y_error con los parametros del contrato.
        self.reserva.confirmar()  # Prepara los datos o completa la comprobacion del bloque actual.
        with patch('sistema.reserva.registrar_evento') as evento:  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
            with self.assertRaises(CalculoInvalidoError):  # Exige que el caso sea rechazado con la excepcion indicada.
                self.reserva.procesar(descuento=2)  # Prepara los datos o completa la comprobacion del bloque actual.
            self.assertIn('intento de procesamiento finalizado', evento.call_args.args[0])  # Comprueba el resultado esperado del escenario.
            self.assertEqual(self.reserva.estado, 'confirmada')  # Comprueba el resultado esperado del escenario.
        with patch('sistema.reserva.registrar_evento') as evento:  # Mantiene el contexto de prueba y restaura sus recursos al finalizar.
            self.reserva.procesar()  # Prepara los datos o completa la comprobacion del bloque actual.
            self.assertIn('intento de procesamiento finalizado', evento.call_args.args[0])  # Comprueba el resultado esperado del escenario.
            self.assertEqual(self.reserva.estado, 'procesada')  # Comprueba el resultado esperado del escenario.

    def test_calculo_no_representable_conserva_causa(self):  # Implementa test_calculo_no_representable_conserva_causa con los parametros del contrato.
        with self.assertRaises(CalculoInvalidoError) as captura:  # Exige que el caso sea rechazado con la excepcion indicada.
            Asesoria('Tarifa grande', 1e308).calcular_costo(1e308)  # Prepara los datos o completa la comprobacion del bloque actual.
        self.assertIsInstance(captura.exception.__cause__, ArithmeticError)  # Comprueba el resultado esperado del escenario.


if __name__ == '__main__':  # Comprueba la condicion antes de aceptar los datos o la operacion.
    unittest.main()  # Prepara los datos o completa la comprobacion del bloque actual.
