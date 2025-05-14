CREATE TABLE declaraciones_renta (
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