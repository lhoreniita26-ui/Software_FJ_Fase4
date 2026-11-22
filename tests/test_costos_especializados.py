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


class AsesoriaEspecializadaTests(unittest.TestCase):
    def test_recargo_por_cada_nivel(self):
        for nivel, esperado in (('basico', 200), ('intermedio', 230), ('avanzado', 260)):
            with self.subTest(nivel=nivel):
                asesoria = Asesoria('Consulta', 100, nivel=nivel)
                self.assertEqual(asesoria.calcular_costo(2), esperado)
                self.assertIn(nivel, asesoria.describir())

    def test_normalizar_nivel(self):
        self.assertEqual(Asesoria('Consulta', 100, nivel=' BÁSICO ').nivel, 'basico')
        self.assertEqual(Asesoria('Consulta', 100, nivel=' AVANZADO ').calcular_costo(2), 260)

    def test_nivel_invalido(self):
        for nivel in (None, '', 'experto', 1, True, object()):
            with self.subTest(nivel=nivel):
                with self.assertRaises(ServicioInvalidoError):
                    Asesoria('Consulta', 100, nivel=nivel)

    def test_nivel_y_recargo_son_de_solo_lectura(self):
        asesoria = Asesoria('Consulta', 100, nivel='avanzado')
        with self.assertRaises(AttributeError):
            asesoria.nivel = 'basico'
        with self.assertRaises(AttributeError):
            asesoria.recargo_nivel = 0

    def test_recargo_con_impuesto_y_descuento(self):
        asesoria = Asesoria('Consulta', 100, nivel='avanzado')
        self.assertEqual(asesoria.calcular_costo(2, .19, .10), 278.46)
        self.assertEqual(asesoria.calcular_costo(2, descuento=1), 0)

    def test_reserva_real_incluye_recargo(self):
        cliente = Cliente('Ana Gomez', '123456', 'ana@example.com')
        reserva = Reserva(cliente, Asesoria('Consulta', 100, nivel='avanzado'), 2)
        reserva.confirmar()
        self.assertEqual(reserva.procesar(.19, .10), 278.46)
        self.assertEqual(reserva.estado, 'procesada')


class PolimorfismoTests(unittest.TestCase):
    def test_misma_llamada_despacha_tres_reglas_distintas(self):
        servicios = [
            ReservaSala('Sala', 100, cargo_limpieza=20),
            AlquilerEquipo('Equipo', 100, tasa_seguro=.05),
            Asesoria('Consulta', 100, nivel='avanzado'),
        ]
        self.assertEqual([s.calcular_costo(2, .19, .10) for s in servicios],
                         [235.62, 224.91, 278.46])
        self.assertTrue(all(s.validar_parametros(2, .19, .10) for s in servicios))
