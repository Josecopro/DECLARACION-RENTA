# DECLARACION DE RENTA

## ¿Quién hizo esto?
- Miguel Martinez Tamayo
- Juan Esteban Vallejo


## Editado por:
- Samuel Uribe
- Santiago Martinez

## ¿Qué es y para qué es?
Programa que permite calcular si un usuario debe declarar renta, proporcionando valores como el impuesto a pagar y su vase gravable en Unidad de Valor Tributario (UVT) y en pesos colombianos (COP)

## Arquitectura del proyecto:

```
DECLARACION_RENTA/
├──.vscode/
|   └──settings.json
├──sql/
|   └──crear_declaraciones.sql
├──src/
|   ├──controller/
|   |    └──contolador_declaraciones.py
|   ├──model/
|   |    ├──__init__.py
|   |    ├──declaraciones.py
|   |    └──LogicaRenta.py
|   └──view/
|        ├──__init__.py
|        ├──consola_renta.py
|        └──InterfazRenta.py
|
├──tests/
|   ├──Tests_Renta1.py
|   └──tests_declaraiones.py
|
├──.gitignore
├──README.md
├──SecretConfig-sample.py
└──requirements.txt
```

## ¿Como ejecuto la GUI?

La aplicación cuenta con una interfaz gráfica construida con **Kivy** para calcular el impuesto sobre la renta en Colombia.  

### ✅ Requisitos previos

Asegúrate de tener instaladas las dependencias:

```bash
pip install -r requirements.txt
```

> Si no tienes un archivo `requirements.txt`, puedes instalar Kivy directamente con:

```bash
pip install kivy
```

---

### ▶️ Ejecutar la GUI

Desde la raíz del proyecto (donde está la carpeta `src`), usa el siguiente comando:

```bash
python -m src.view.console.InterfazRenta
```

Esto garantizará que los módulos se importen correctamente y la aplicación se ejecute sin errores.

---

### ▶️ Ejecutar interfaz de consola
- Inicializar la consola de sus sistema operativo, y, a demás, buscar allí la ruta del archivo del programa (DECLARACION-RENTA).
- En la consola, ubicados en la carpeta raíz del proyecto, utilice el siguiente comando:

  ```
  py src/view/console/ConsolaRenta.py
  ```
---

## ¿Cómo inicializo una base de datos para el proyecto?

La aplicación cuenta con un acceso a una base de datos PostgreSQL guardada en la nube.

### Crear columnas de base de datos
- en su servidor en la nube (recomendablemente use el servicio online de *Neon.tech*) deberá crear un nuevo proyecto en el cual debe pegar el código que se encuentra en el archivo crear_declaraciones.sql la carpeta llamada sql/
```
DECLARACION_RENTA/
├──sql/
|   └──crear_declaraciones.sql
```
-una vez pegado y ejecutado el código se creara una tabla en su base de datos

---

### Acceso a su base de datos desde el proyecto
- En la carpeta raíz del proecto encontrará un proyecto con el nombre de *SecretConfig-sample.py*, allí encontrará una guia de como debe ingresar las credenciales de su base de datos, que encontrará en el servicio Neon o cualquiera que utilice.
- Una vez reemplazados los strings en el archivo *SecretConfig-sample.py*, puede renombrar el archivo simplemente como *SecretConfig.py* (o simplemente duplicarlo con ese nombre), esto hará que el programa pueda acceeder a su base de datos.
    *IMPORTANTE*: Recuerde no exponer sus credenciales en el navegador, el puerto de conexión con la base de datos, si está utilizando PostgreSQl siempre será el                   mismo "5432"
---

### Inicializar base de datos:
- Luego de hacer los pasos anteriores, para inicializar la base de datos y asegurarse de que esta funcione correctamente, deberá ejecutar las pruebas unitarias del proyecto que se encuentran en la carpeta tests/.

```
DECLARACION_RENTA/
├──.vscode/
|   └──settings.json
|
├──tests/
    ├──Tests_Renta1.py
    └──tests_declaraiones.py
```
---
### Guardar calculos del programa en base de datos
- Una vez inicializada la base de datos con los pasos anteriores, todo cálculo que genere la aplicación principal (ejecutada desde la interfaz gráfica InterfazRenta.py) se guardará automaticamente en su base de datos.
---

## ✅ ¿Cómo ejecuto las pruebas unitarias?

- El proyecto utiliza el framework *Unittest* de python para correr pruebas.
- Si está utilizando VSCode, el proyecto cuenta con un archivo settings.json que ya tiene un pre-ajuste del explorador de pruebas.
- Asegurese de que el explorador compile todas las pruebas del proyecto antes de ejecutar.

---

### Ejecución general en explorador
- Corra las pruebas desde el explorador de VSCode y espere a que estas se completen (31 pruebas en total)

---
### Pruebas de funcionalidad
- El archivo Test_Renta1.py prueba que la funcionalidad principal del proyecto cumpla correctamente con todas las expectativas, siguiendo con una serie de casos de prueba que encontrará en un enlace mas adelante en este documento.
- puede ejecutarlas directamente con el archivo abierto en el editor, presionando el botón de "Run". O, también puede ejecutar el siguiente comando en consola.

```bash
python -m tests.Test_Renta1
```
---

### Pruebas de base de datos
- El archivo tests_declaraciones.py prueba que las funcionalidades del programa de insertar, buscar y modificar datos o filas en la base de datos se ejecuten correctamente, y los podrá observar en su base de datos una vez ejecute las pruebas.  
- puede ejecutarlas directamente con el archivo abierto en el editor, presionando el botón de "Run". O, también puede ejecutar el siguiente comando en consola.

```bash
python -m tests.tests_declaraciones
```

---

### 🐞 ¿Errores comunes?

- Si ves `ModuleNotFoundError: No module named 'src'`, asegúrate de estar ejecutando el comando **desde la raíz del proyecto** y no desde dentro de `src`.

Puedes confirmar que estás en la raíz si ves una estructura como esta:

```
📁 tu_proyecto/
├── src/
|   ├── controller/
│   ├── model/
│   └── view/
└── README.md
```


## 🤓 ¿Cómo está hecho?
link de excel para la declaracion de impuestos de un asalariado (CASOS DE PRUEBA)
https://docs.google.com/spreadsheets/d/1IwasnT6Vj87bwmWxKCBOTA8iFx_RkNW8GP2FXW7QbEE/edit?usp=sharing

**Variables de entrada:**
Criterios a tener en cuenta para el proceso de declaración de impuestos, ya que si la persona supera uno o más, deberá cumplir con la declaración de sus ingresos para evitar sanciones:

    1. Ingresos brutos anuales.
    2. Aportes a salud y pensión.
    3. Número de dependientes.
    4. Intereses de crédito hipotecario.
    5. Consumos con tarjeta de crédito.
    6. Consignaciones/depósitos bancarios.
    7. Patrimonio bruto.
    8. Retenciones en la fuente.
    9. Tipo de cambio (si hay ingresos en USD).

**Variables de salida:**
Esto se obtiene al calcular la declaración de renta de la persona.

    1. Base gravable.
    2. Base gravable en uvt.
    3. Impuesto(menos retenciones, solo si aplica).

**Procesos y operaciones:**
Las formulas del impuesto se obtuvieron en base al artículo 241 del Estatuto Tributario Nacional:

![image](https://github.com/user-attachments/assets/1bb101d8-3c00-4e88-be18-5a97614735ff)

El valor de la Unidad de Valor Tributario (UVT) para el año 2025 es de $49.799 pesos colombianos.
Este valor se utiliza como referencia para diversas obligaciones tributarias y sanciones en Colombia. Para declarar la renta, los ingresos brutos mínimos para declarar renta son 1.400 UVT, lo que equivale a $69.718.600 pesos colombianos.

**Reglas generales para la declaración obligatoria de renta**

Los contribuyentes asalariados en Colombia están obligados a presentar una declaración de renta si cumplen con alguna de las siguientes condiciones:

    1.El valor de los activos poseídos al 31 de diciembre supera las 4,500 Unidades Tributarias (UVT), lo que equivale aproximadamente a COP 224.095.5000 
    
    2.Los cargos a tarjetas de crédito durante el año fiscal superan las 1,400 UVT (aproximadamente COP 69.718.600) 
    
    3.El valor total de las compras en efectivo supera las 1,400 UVT (COP 69.718.600) 
    
    4.El valor total de los depósitos bancarios y otras inversiones supera las 1,400 UVT (COP 69.718.600) 
    
    5.Los ingresos durante el año fiscal superan las 1,400 UVT (COP 69.718.600) 
    
**URL de la aplicación:**

https://declaracion-renta-1.onrender.com


**¿Comó correr la aplicación WEB?**

> Utiliza una base de datos en donde tengas los datos, como neon, despues de tenerla, con el archivo de SecretConfig.py creado con la previa explicacion, puedes correr app.py con f5 o desde la carpeta raiz ejecutar el comando `python3 app.py`
 




