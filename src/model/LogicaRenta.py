VALOR_UVT: int = 49_799  # Unidad de valor tributario
VALOR_MINIMO_UVT: int = 1400
VALOR_MINIMO_IMPUESTO: int = VALOR_MINIMO_UVT * VALOR_UVT


class IngresosNegativosError(Exception):
    """Excepción para cuando los ingresos brutos anuales son negativos (Caso 7)."""
    pass

class DependientesExcedidoError(Exception):
    """Excepción para cuando el número de dependientes excede el límite (Caso 8)."""
    pass

class AportesSaludExcedidoError(Exception):
    """Excepción para cuando los aportes a salud y pensión superan el límite (Caso 9)."""
    pass

class IngresosInferioresAlMinimoError(Exception):
    """Excepción para cuando los ingresos brutos anuales son inferiores al mínimo para declarar (Caso 10)."""
    pass

"""Base gravable a partir de datos de entrada"""
def obtener_base_gravable(ingresos_brutos_anuales, aportes_salud_pension, numero_dependientes,
                          intereses_credito_hipotecario):
    if ingresos_brutos_anuales < 0:
        raise IngresosNegativosError("Los ingresos brutos anuales no pueden ser negativos.")

    if numero_dependientes > 4:
        raise DependientesExcedidoError("El número de dependientes excede el límite permitido de 4.")

    if aportes_salud_pension > ingresos_brutos_anuales * 0.04:  # 4% de los ingresos brutos
        raise AportesSaludExcedidoError(
            "Los aportes a salud y pensión superan el 4% de los ingresos brutos anuales.")

    if ingresos_brutos_anuales < VALOR_MINIMO_IMPUESTO:  # Validación para el Caso 10
        raise IngresosInferioresAlMinimoError(
            f"Los ingresos brutos anuales deben ser superiores a 1.400 UVT, lo que equivale a ${VALOR_MINIMO_IMPUESTO} pesos colombianos.")

    base_gravable = ingresos_brutos_anuales - (aportes_salud_pension + intereses_credito_hipotecario)
    return base_gravable

"""Conversor del valor base gravable a unidad de valor tributario (UVT)"""
def obtener_base_gravable_en_uvt(base_gravable):
    base_gravable_en_uvt = base_gravable / VALOR_UVT

    return round(base_gravable_en_uvt)

"""Cálculo del impuesto según fórmulas en README.md, Procesos y Operaciones"""
def obtener_impuesto(base_gravable_en_uvt):

    if base_gravable_en_uvt >= 1090 and base_gravable_en_uvt <= 1700:
        impuesto: float = ((base_gravable_en_uvt - 1_090) * 0.19) * VALOR_UVT

    elif base_gravable_en_uvt > 1700 and base_gravable_en_uvt <= 4100:
        impuesto: float = ((base_gravable_en_uvt - 1_700) * 0.28 + 116) * VALOR_UVT

    elif base_gravable_en_uvt > 4100 and base_gravable_en_uvt <= 8670:
        impuesto: float = ((base_gravable_en_uvt - 4100) * 0.33 + 788) * VALOR_UVT

    elif base_gravable_en_uvt > 8670 and base_gravable_en_uvt <= 18970:
        impuesto: float = ((base_gravable_en_uvt - 8670) * 0.35 + 2296) * VALOR_UVT

    elif base_gravable_en_uvt > 18970 and base_gravable_en_uvt <= 31000:
        impuesto: float = ((base_gravable_en_uvt - 18970) * 0.37 + 5901) * VALOR_UVT

    elif base_gravable_en_uvt > 31000:
        impuesto: float = ((base_gravable_en_uvt - 31000) * 0.39 + 10352) * VALOR_UVT

    return round(impuesto)
