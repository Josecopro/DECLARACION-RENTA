from datetime import datetime

class Declaracion:

    def __init__(self, id, fecha, ingresos_brutos_anuales, aportes_salud_pension,
                 numero_dependientes, intereses_credito_hipotecario, base_gravable,
                 base_gravable_uvt, impuesto_renta, mensaje_error):
        self.id = id
        self.fecha = fecha
        self.ingresos_brutos_anuales = ingresos_brutos_anuales
        self.aportes_salud_pension = aportes_salud_pension
        self.numero_dependientes = numero_dependientes
        self.intereses_credito_hipotecario = intereses_credito_hipotecario
        self.base_gravable = base_gravable
        self.base_gravable_uvt = base_gravable_uvt
        self.impuesto_renta = impuesto_renta
        self.mensaje_error = mensaje_error

    def esIgual(self, comparar_con):
        
        assert self.id == comparar_con.id
        assert self.fecha == comparar_con.fecha
        assert self.ingresos_brutos_anuales == comparar_con.ingresos_brutos_anuales
        assert self.aportes_salud_pension == comparar_con.aportes_salud_pension
        assert self.numero_dependientes == comparar_con.numero_dependientes
        assert self.intereses_credito_hipotecario == comparar_con.intereses_credito_hipotecario
        assert self.base_gravable == comparar_con.base_gravable
        assert self.base_gravable_uvt == comparar_con.base_gravable_uvt
        assert self.impuesto_renta == comparar_con.impuesto_renta
        assert self.mensaje_error == comparar_con.mensaje_error