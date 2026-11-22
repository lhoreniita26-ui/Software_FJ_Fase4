'''Costos propios de cada servicio y su integracion con Cliente y Reserva.'''
import math
import unittest
from decimal import Decimal
from sistema.cliente import Cliente
from sistema.servicios import ReservaSala, AlquilerEquipo, Asesoria
from sistema.reserva import Reserva
from sistema.excepciones import ServicioInvalidoError


class SalaEspecializadaTests(unittest.TestCase):
    def test_limpieza_fija_no_se_multiplica_por_horas(self):
        sala = ReservaSala('Sala', 100, cargo_limpieza=20)
        self.assertEqual(sala.calcular_costo(2), 220)
        self.assertEqual(sala.calcular_costo(4), 420)
        self.assertIn('Limpieza fija: 20', sala.describir())

    def test_limpieza_tasas_y_redondeo_final(self):
        sala = ReservaSala('Sala', 100, cargo_limpieza=20)
        self.assertEqual(sala.calcular_costo(2, .19, .10), 235.62)
        self.assertEqual(sala.calcular_costo(2, descuento=1), 0)
        fraccion = ReservaSala('Fraccion', Decimal('10.004'), cargo_limpieza=Decimal('.004'))
        self.assertEqual(fraccion.calcular_costo(1), 10.01)

    def test_limpieza_invalida(self):
        for cargo in (-1, True, '20', None, math.nan, math.inf, Decimal('sNaN')):
            with self.subTest(cargo=cargo):
                with self.assertRaises(ServicioInvalidoError):
                    ReservaSala('Sala', 100, cargo_limpieza=cargo)

    def test_limpieza_es_de_solo_lectura(self):
        sala = ReservaSala('Sala', 100, cargo_limpieza=20)
        with self.assertRaises(AttributeError):
            sala.cargo_limpieza = 30

    def test_reserva_real_incluye_limpieza(self):
        cliente = Cliente('Ana Gomez', '123456', 'ana@example.com')
        reserva = Reserva(cliente, ReservaSala('Sala', 100, cargo_limpieza=20), 2)
        reserva.confirmar()
        self.assertEqual(reserva.procesar(.19, .10), 235.62)
        self.assertEqual(reserva.estado, 'procesada')


class EquipoEspecializadoTests(unittest.TestCase):
    def test_seguro_proporcional_a_las_horas(self):
        equipo = AlquilerEquipo('Equipo', 100, tasa_seguro=.05)
        self.assertEqual(equipo.calcular_costo(2), 210)
        self.assertEqual(equipo.calcular_costo(4), 420)
        self.assertIn('Tasa de seguro: 0.05', equipo.describir())

    def test_seguro_con_impuesto_y_descuento(self):
        equipo = AlquilerEquipo('Equipo', 100, tasa_seguro=.05)
        self.assertEqual(equipo.calcular_costo(2, .19, .10), 224.91)
        self.assertEqual(equipo.calcular_costo(2, descuento=1), 0)
        self.assertEqual(AlquilerEquipo('Equipo', 100, tasa_seguro=1).calcular_costo(2), 400)

    def test_seguro_invalido(self):
        for tasa in (-1, 1.01, True, '0.05', None, math.nan, math.inf, Decimal('sNaN')):
            with self.subTest(tasa=tasa):
                with self.assertRaises(ServicioInvalidoError):
                    AlquilerEquipo('Equipo', 100, tasa_seguro=tasa)

    def test_seguro_es_de_solo_lectura(self):
        equipo = AlquilerEquipo('Equipo', 100, tasa_seguro=.05)
        with self.assertRaises(AttributeError):
            equipo.tasa_seguro = .10

    def test_reserva_real_incluye_seguro(self):
        cliente = Cliente('Ana Gomez', '123456', 'ana@example.com')
        reserva = Reserva(cliente, AlquilerEquipo('Equipo', 100, tasa_seguro=.05), 2)
        reserva.confirmar()
        self.assertEqual(reserva.procesar(.19, .10), 224.91)
        self.assertEqual(reserva.estado, 'procesada')
