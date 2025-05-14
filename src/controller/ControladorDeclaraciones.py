import sys
sys.path.append("src")

import psycopg2
from model.declaraciones import Declaracion
import SecretConfig 

class ControladorDeclaraciones:

    @staticmethod
    def CrearTabla():
        """ Crea la tabla de declaraciones en la BD """
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS declaraciones_renta (
                id SERIAL PRIMARY KEY,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ingresos_brutos_anuales NUMERIC(15, 2) NOT NULL,
                aportes_salud_pension NUMERIC(15, 2) NOT NULL,
                numero_dependientes INTEGER NOT NULL,
                intereses_credito_hipotecario NUMERIC(15, 2) NOT NULL,
                base_gravable NUMERIC(15, 2),
                base_gravable_uvt INTEGER,
                impuesto_renta NUMERIC(15, 2),
                mensaje_error TEXT
            );
        """)
        cursor.connection.commit()

    @staticmethod
    def EliminarTabla():
        """ Elimina la tabla de declaraciones """
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("DROP TABLE IF EXISTS declaraciones_renta")
        cursor.connection.commit()

    @staticmethod
    def InsertarDeclaracion(declaracion: Declaracion):
        """ Inserta una declaración de renta en la tabla """
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("""
            INSERT INTO declaraciones_renta (
                ingresos_brutos_anuales, 
                aportes_salud_pension, 
                numero_dependientes,
                intereses_credito_hipotecario,
                base_gravable,
                base_gravable_uvt,
                impuesto_renta,
                mensaje_error
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            declaracion.ingresos_brutos_anuales,
            declaracion.aportes_salud_pension,
            declaracion.numero_dependientes,
            declaracion.intereses_credito_hipotecario,
            declaracion.base_gravable,
            declaracion.base_gravable_uvt,
            declaracion.impuesto_renta,
            declaracion.mensaje_error
        ))
        id_insertado = cursor.fetchone()[0]
        cursor.connection.commit()
        return id_insertado

    @staticmethod
    def BuscarPorId(id):
        """ Busca una declaración por ID y retorna un objeto Declaracion """
        cursor = ControladorDeclaraciones.ObtenerCursor()
        cursor.execute("""
            SELECT id, fecha, ingresos_brutos_anuales, aportes_salud_pension,
                   numero_dependientes, intereses_credito_hipotecario,
                   base_gravable, base_gravable_uvt, impuesto_renta, mensaje_error
            FROM declaraciones_renta
            WHERE id = %s
        """, (id,))
        fila = cursor.fetchone()
        if fila:
            return Declaracion(
                id=fila[0], fecha=fila[1],
                ingresos_brutos_anuales=fila[2], aportes_salud_pension=fila[3],
                numero_dependientes=fila[4], intereses_credito_hipotecario=fila[5],
                base_gravable=fila[6], base_gravable_uvt=fila[7],
                impuesto_renta=fila[8], mensaje_error=fila[9]
            )
        return None

    @staticmethod
    def ObtenerCursor():
        """ Crea la conexión a la base de datos y retorna un cursor """
        connection = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT
        )
        return connection.cursor()
