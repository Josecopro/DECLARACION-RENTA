import unittest
import sys
import os
sys.path.append("src")
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.controller.ControladorDeclaraciones import ControladorDeclaraciones
from src.model.declaraciones import Declaracion
from datetime import datetime

class DeclaracionesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ControladorDeclaraciones.EliminarTabla()
        ControladorDeclaraciones.CrearTabla()
    
        cls.ids = []
        for i, declaracion in enumerate([
            Declaracion(None, None, 100000000, 4000000, 2, 3000000, 93000000, 1867, 5500000, None),
            Declaracion(None, None, 85000000, 3500000, 1, 1000000, 80500000, 1617, 4200000, None),
            Declaracion(None, None, 60000000, 2000000, 3, 1500000, 56500000, 1134, 2600000, None)
        ]):
            inserted_id = ControladorDeclaraciones.InsertarDeclaracion(declaracion)
            cls.ids.append(inserted_id)
            
    # -------------------- Pruebas de Inserción --------------------
    def test_insertar_declaracion_1(self):
        declaracion = Declaracion(
            id=None, fecha=None,
            ingresos_brutos_anuales=100000000,
            aportes_salud_pension=4000000,
            numero_dependientes=2,
            intereses_credito_hipotecario=3000000,
            base_gravable=93000000,
            base_gravable_uvt=1868,
            impuesto_renta=8119229,
            mensaje_error=None
        )
        ControladorDeclaraciones.InsertarDeclaracion(declaracion)

    def test_insertar_declaracion_2(self):
        declaracion = Declaracion(
            id=None, fecha=None,
            ingresos_brutos_anuales=85000000,
            aportes_salud_pension=3500000,
            numero_dependientes=1,
            intereses_credito_hipotecario=1000000,
            base_gravable=None,
            base_gravable_uvt=None,
            impuesto_renta=None,
            mensaje_error= "Los aportes a salud y pensión superan el 4% de los ingresos brutos anuales (Caso 9)."
        )
        ControladorDeclaraciones.InsertarDeclaracion(declaracion)

    def test_insertar_declaracion_3(self):
        declaracion = Declaracion(
            id=None, fecha=None,
            ingresos_brutos_anuales=74000000,
            aportes_salud_pension=2000000,
            numero_dependientes=3,
            intereses_credito_hipotecario=1500000,
            base_gravable=70500000,
            base_gravable_uvt=1416,
            impuesto_renta=3084550,
            mensaje_error=None
        )
        ControladorDeclaraciones.InsertarDeclaracion(declaracion)

    # -------------------- Pruebas de Búsqueda --------------------
    def test_buscar_declaracion_1(self):
        buscado = ControladorDeclaraciones.BuscarPorId(self.ids[0])
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.base_gravable_uvt, 1867)
    
    def test_buscar_declaracion_2(self):
        buscado = ControladorDeclaraciones.BuscarPorId(self.ids[1])
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.numero_dependientes, 1)
    
    def test_buscar_declaracion_3(self):
        buscado = ControladorDeclaraciones.BuscarPorId(self.ids[2])
        self.assertIsNotNone(buscado)
        self.assertEqual(buscado.impuesto_renta, 2600000)
    

    # -------------------- Pruebas de Modificación (simulada como inserción directa SQL) --------------------
    def test_modificar_declaracion_1(self):
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("UPDATE declaraciones_renta SET numero_dependientes = 4 WHERE id = 1")
        cursor.connection.commit()
        buscado = ControladorDeclaraciones.BuscarPorId(1)
        self.assertEqual(buscado.numero_dependientes, 4)

    def test_modificar_declaracion_2(self):
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("UPDATE declaraciones_renta SET impuesto_renta = 999999 WHERE id = 2")
        cursor.connection.commit()
        buscado = ControladorDeclaraciones.BuscarPorId(2)
        self.assertEqual(buscado.impuesto_renta, 999999)

    def test_modificar_declaracion_3(self):
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("UPDATE declaraciones_renta SET mensaje_error = 'Modificado' WHERE id = 3")
        cursor.connection.commit()
        buscado = ControladorDeclaraciones.BuscarPorId(3)
        self.assertEqual(buscado.mensaje_error, 'Modificado')


if __name__ == '__main__':
    unittest.main()
