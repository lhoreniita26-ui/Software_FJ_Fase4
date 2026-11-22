'''Pruebas de contrato; ClientePrueba no reemplaza al cliente de produccion.'''
import math
import unittest
from decimal import Decimal
from unittest.mock import patch

from sistema.entidad import Entidad
from sistema.excepciones import (
    CalculoInvalidoError, ClienteInvalidoError, OperacionNoPermitidaError,
    ReservaInvalidaError, ServicioInvalidoError, ServicioNoDisponibleError,
)
from sistema.servicios import Servicio, ReservaSala, AlquilerEquipo, Asesoria
from sistema.reserva import Reserva


class ClientePrueba(Entidad):
    def __init__(self):
        super().__init__()
        self.nombre = 'Cliente de prueba'
        self.documento = '123456'
        self.correo = 'prueba@example.com'

    def describir(self):
        return self.nombre

    def validar(self):
        if not self.correo:
            raise ClienteInvalidoError('Correo obligatorio.')
        return True


class EntidadTests(unittest.TestCase):
    def test_contrato_abstracto(self):
        with self.assertRaises(TypeError):
            Entidad()
        with self.assertRaises(TypeError):
            Servicio('Generico', 100)

    def test_identificador_unico_y_solo_lectura(self):
        uno, otro = ClientePrueba(), ClientePrueba()
        self.assertNotEqual(uno.id, otro.id)
        with self.assertRaises(AttributeError):
            uno.id = 'cambio'


class ServicioTests(unittest.TestCase):
    def test_tres_formas_de_calculo_y_polimorfismo(self):
        for tipo in (ReservaSala, AlquilerEquipo, Asesoria):
            with self.subTest(tipo=tipo.__name__):
                servicio = tipo('Servicio', 100)
                self.assertEqual(servicio.calcular_costo(2), 200)
                self.assertEqual(servicio.calcular_costo(2, .19), 238)
                self.assertEqual(servicio.calcular_costo(2, .19, .10), 214.20)
                self.assertEqual(servicio.calcular_costo(2, descuento=1), 0)
                self.assertIn('Servicio', servicio.describir())

    def test_redondeo_monetario_y_fracciones(self):
        self.assertEqual(Asesoria('A', Decimal('10.005')).calcular_costo(1), 10.01)
        self.assertEqual(ReservaSala('A', 100).calcular_costo(.5), 50)

    def test_datos_invalidos(self):
        for nombre, precio, disponible in (
            ('', 10, True), ('  ', 10, True), (None, 10, True),
            ('A', 0, True), ('A', -1, True), ('A', True, True),
            ('A', '10', True), ('A', math.nan, True), ('A', math.inf, True),
            ('A', 10, 1),
        ):
            with self.subTest(datos=(nombre, precio, disponible)):
                with self.assertRaises(ServicioInvalidoError):
                    ReservaSala(nombre, precio, disponible)

    def test_parametros_invalidos(self):
        servicio = Asesoria('A', 100)
        for parametros in (
            (0,), (-1,), (True,), ('2',), (math.nan,), (math.inf,),
            (1, -.1), (1, 19), (1, True), (1, math.nan),
            (1, 0, -.1), (1, 0, 10), (1, 0, False),
        ):
            with self.subTest(parametros=parametros):
                with self.assertRaises(CalculoInvalidoError):
                    servicio.calcular_costo(*parametros)

    def test_costo_fuera_de_rango(self):
        with self.assertRaises(CalculoInvalidoError):
            Asesoria('A', 1e308).calcular_costo(1e308)

    def test_disponibilidad_validada(self):
        servicio = AlquilerEquipo('A', 100, False)
        with self.assertRaises(ServicioNoDisponibleError):
            servicio.calcular_costo(1)
        with self.assertRaises(ServicioInvalidoError):
            servicio.disponible = 'si'
        servicio.disponible = True
        self.assertEqual(servicio.calcular_costo(1), 100)


class ReservaTests(unittest.TestCase):
    def setUp(self):
        self.cliente = ClientePrueba()
        self.servicio = ReservaSala('Sala A', 100)
        self.reserva = Reserva(self.cliente, self.servicio, 2)

    def test_flujo_correcto_y_encapsulamiento(self):
        self.assertEqual(self.reserva.estado, 'pendiente')
        self.assertIsNone(self.reserva.costo_total)
        self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, 'confirmada')
        self.assertEqual(self.reserva.procesar(.19, .10), 214.20)
        self.assertEqual(self.reserva.estado, 'procesada')
        self.assertEqual(self.reserva.costo_total, 214.20)
        self.assertIn(str(self.reserva.id), self.reserva.describir())
        with self.assertRaises(AttributeError):
            self.reserva.estado = 'pendiente'

    def test_no_procesar_sin_confirmar(self):
        with self.assertRaises(OperacionNoPermitidaError):
            self.reserva.procesar()
        self.assertEqual(self.reserva.estado, 'pendiente')

    def test_cancelar_pendiente_o_confirmada(self):
        for confirmar in (False, True):
            with self.subTest(confirmar=confirmar):
                reserva = Reserva(self.cliente, self.servicio, 1)
                if confirmar:
                    reserva.confirmar()
                reserva.cancelar()
                self.assertEqual(reserva.estado, 'cancelada')
                for accion in (reserva.confirmar, reserva.cancelar, reserva.procesar):
                    with self.assertRaises(OperacionNoPermitidaError):
                        accion()

    def test_procesada_es_terminal(self):
        self.reserva.confirmar()
        self.reserva.procesar()
        for accion in (self.reserva.confirmar, self.reserva.cancelar, self.reserva.procesar):
            with self.assertRaises(OperacionNoPermitidaError):
                accion()

    def test_error_calculo_preserva_estado_y_permite_reintento(self):
        self.reserva.confirmar()
        with self.assertRaises(CalculoInvalidoError):
            self.reserva.procesar(descuento=2)
        self.assertEqual(self.reserva.estado, 'confirmada')
        self.assertIsNone(self.reserva.costo_total)
        self.assertEqual(self.reserva.procesar(), 200)

    def test_servicio_no_disponible_al_confirmar_o_procesar(self):
        self.servicio.disponible = False
        with self.assertRaises(ServicioNoDisponibleError):
            self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, 'pendiente')
        self.servicio.disponible = True
        self.reserva.confirmar()
        self.servicio.disponible = False
        with self.assertRaises(ServicioNoDisponibleError):
            self.reserva.procesar()
        self.assertEqual(self.reserva.estado, 'confirmada')

    def test_datos_reserva_invalidos(self):
        for cliente, servicio, horas in (
            (None, self.servicio, 1), (object(), self.servicio, 1),
            (self.cliente, None, 1), (self.cliente, self.servicio, 0),
            (self.cliente, self.servicio, -1), (self.cliente, self.servicio, True),
            (self.cliente, self.servicio, math.nan),
        ):
            with self.subTest(horas=horas):
                with self.assertRaises(ReservaInvalidaError):
                    Reserva(cliente, servicio, horas)

    def test_cliente_se_revalida(self):
        self.cliente.correo = ''
        with self.assertRaises(ClienteInvalidoError):
            self.reserva.confirmar()
        self.assertEqual(self.reserva.estado, 'pendiente')

    def test_registro_de_exito_y_error(self):
        with patch('sistema.reserva.registrar_evento') as evento:
            self.reserva.confirmar()
            evento.assert_called_once()
        with patch('sistema.reserva.registrar_error') as error:
            with self.assertRaises(OperacionNoPermitidaError):
                self.reserva.confirmar()
            error.assert_called_once()


    def test_finally_registra_cierre_con_exito_y_error(self):
        self.reserva.confirmar()
        with patch('sistema.reserva.registrar_evento') as evento:
            with self.assertRaises(CalculoInvalidoError):
                self.reserva.procesar(descuento=2)
            self.assertIn('intento de procesamiento finalizado', evento.call_args.args[0])
            self.assertEqual(self.reserva.estado, 'confirmada')
        with patch('sistema.reserva.registrar_evento') as evento:
            self.reserva.procesar()
            self.assertIn('intento de procesamiento finalizado', evento.call_args.args[0])
            self.assertEqual(self.reserva.estado, 'procesada')

    def test_calculo_no_representable_conserva_causa(self):
        with self.assertRaises(CalculoInvalidoError) as captura:
            Asesoria('Tarifa grande', 1e308).calcular_costo(1e308)
        self.assertIsInstance(captura.exception.__cause__, ArithmeticError)


if __name__ == '__main__':
    unittest.main()
