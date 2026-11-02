"""Pruebas de regresión con los resultados de las ocho hojas del Taller 3."""
import unittest
from fastapi.testclient import TestClient
from main import app

CASOS = [
    (1, dict(capital=110000, interes=39875, anios=2, meses=5), '15 % anual'),
    (2, dict(capital=85000, interes=35700, tasa_anual=21), '2,0000 años'),
    (3, dict(monto_futuro=1500, tasa_anual=6, meses=9), '$1.435,41'),
    (4, dict(tasa_anual=5.1, base_dias=360, monto_1=7000, dias_1=83,
             monto_2=15500, dias_2=125, monto_3=10000, dias_3=311), '$31.726,96'),
    (5, dict(tasa_anual=12.48, base_dias=360, deposito_1=15000, dias_1=145,
             deposito_2=10000, dias_2=59, retiro=9500, dias_retiro=101), '$16.125,90'),
    (6, dict(prestamo_1=1000, tasa_prestamo=4, plazo_contrato_anios=1.5,
             deuda_2=2500, tasa_equivalencia=5, pago_hoy=2000,
             vencimiento_1_meses=6, vencimiento_2_meses=9, focal_meses=12), '$1.517,75'),
    (7, dict(nominal=30000, tasa_descuento=35, meses=8), '$23.000,00'),
    (8, dict(nominal=30000, recibido=23000, meses=8, tasa_descuento=35), '45,6522 % anual'),
]

class PruebasCalculadoras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_ocho_resultados_del_excel(self):
        for numero, datos, esperado in CASOS:
            with self.subTest(ejercicio=numero):
                respuesta = self.client.post(f'/api/ejercicios/{numero}', json=datos)
                self.assertEqual(respuesta.status_code, 200, respuesta.text)
                self.assertEqual(respuesta.json()['resultado'], esperado)
                self.assertGreaterEqual(len(respuesta.json()['pasos']), 3)

    def test_capital_negativo_no_se_acepta(self):
        self.assertEqual(self.client.post('/api/ejercicios/1', json={**CASOS[0][1], 'capital': -10}).status_code, 422)

    def test_tiempo_cero_no_se_acepta(self):
        self.assertEqual(self.client.post('/api/ejercicios/1', json={**CASOS[0][1], 'anios': 0, 'meses': 0}).status_code, 422)

    def test_descuento_superior_al_nominal_no_se_acepta(self):
        self.assertEqual(self.client.post('/api/ejercicios/7', json={'nominal': 30000, 'tasa_descuento': 300, 'meses': 8}).status_code, 422)

    def test_fecha_focal_anterior_al_vencimiento_no_se_acepta(self):
        self.assertEqual(self.client.post('/api/ejercicios/6', json={**CASOS[5][1], 'focal_meses': 4}).status_code, 422)

    def test_inconsistencia_de_tasas_del_8_se_advierte(self):
        resp=self.client.post('/api/ejercicios/8', json={**CASOS[7][1], 'tasa_descuento': 30})
        self.assertEqual(resp.status_code, 200)
        self.assertIn('no son coherentes', resp.json()['nota'])

    def test_web_y_archivos(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertIn('Ingeniería Económica', self.client.get('/').text)
        self.assertEqual(self.client.get('/static/script.js').status_code, 200)
        self.assertEqual(self.client.get('/static/style.css').status_code, 200)
        self.assertEqual(self.client.get('/static/img/agraria-banner.png').status_code, 200)
        self.assertEqual(self.client.get('/static/archivos/Taller_3_Grupo13.xlsx').status_code, 200)
        self.assertEqual(self.client.get('/health').json()['ejercicios'], 8)

if __name__ == '__main__': unittest.main()
