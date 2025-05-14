"""Importaciones de Kivy para crear la interfaz gráfica"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

"""Módulos estándar para manejar rutas y sistema"""
import sys
import os

"""Agrega la raíz del proyecto al sys.path si no está, para permitir imports relativos"""
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

"""Imprime las rutas actuales en sys.path para depuración"""
print("Rutas en sys.path:")
for path in sys.path:
    print(path)

"""Intenta importar una función desde el módulo del modelo de lógica de renta"""
try:
    from src.model.LogicaRenta import obtener_base_gravable
    print("✅ Import exitoso de LogicaRenta")
except ModuleNotFoundError as e:
    print("🚨 Error importando LogicaRenta:", e)

"""Importa todas las funciones y excepciones necesarias desde la lógica del modelo"""
from src.model.LogicaRenta import (
    obtener_base_gravable,
    obtener_base_gravable_en_uvt,
    obtener_impuesto,
    IngresosNegativosError,
    DependientesExcedidoError,
    AportesSaludExcedidoError,
    IngresosInferioresAlMinimoError,
    VALOR_UVT,
    VALOR_MINIMO_IMPUESTO
)

"""Importaciones de funcionalidad con base de datos"""
from src.model.declaraciones import Declaracion
from src.controller.ControladorDeclaraciones import ControladorDeclaraciones
from datetime import datetime

"""Clase principal de la aplicación"""
class RentaApp(App):
    
    def build(self):
        self.title = "Calculadora de Impuesto sobre la Renta (Colombia)"
        
        # Layout principal en forma vertical
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campos de entrada para que el usuario escriba sus datos
        self.ingresos_input = TextInput(hint_text="Ingrese ingresos brutos anuales", multiline=False)
        self.aportes_input = TextInput(hint_text="Ingrese aportes a salud y pensión", multiline=False)
        self.dependientes_input = TextInput(hint_text="Ingrese número de dependientes", multiline=False)
        self.intereses_input = TextInput(hint_text="Ingrese intereses crédito hipotecario", multiline=False)
        
        # Botón para ejecutar el cálculo del impuesto
        self.calculate_button = Button(text="Calcular Impuesto", on_press=self.calcular_impuesto)

        # Etiquetas para mostrar los resultados del cálculo
        self.result_label = Label(text="Resultados aparecerán aquí", size_hint_y=None, height=44)
        self.base_gravable_label = Label(text="Base gravable: ", size_hint_y=None, height=44)
        self.base_gravable_uvt_label = Label(text="Base gravable en UVT: ", size_hint_y=None, height=44)
        self.impuesto_label = Label(text="Impuesto de renta: ", size_hint_y=None, height=44)

        # Agrega los elementos al layout principal
        layout.add_widget(self.ingresos_input)
        layout.add_widget(self.aportes_input)
        layout.add_widget(self.dependientes_input)
        layout.add_widget(self.intereses_input)
        layout.add_widget(self.calculate_button)
        layout.add_widget(self.base_gravable_label)
        layout.add_widget(self.base_gravable_uvt_label)
        layout.add_widget(self.impuesto_label)
        
        # Retorna el layout para que se muestre en pantalla
        return layout


    def calcular_impuesto(self, instance):
        try:
            ingresos_brutos_anuales = float(self.ingresos_input.text)
            aportes_salud_pension = float(self.aportes_input.text)
            numero_dependientes = int(self.dependientes_input.text)
            intereses_credito_hipotecario = float(self.intereses_input.text)

            base_gravable = obtener_base_gravable(
                ingresos_brutos_anuales,
                aportes_salud_pension,
                numero_dependientes,
                intereses_credito_hipotecario
            )
            base_gravable_uvt = obtener_base_gravable_en_uvt(base_gravable)
            impuesto = obtener_impuesto(base_gravable_uvt)

            # Mostrar resultados
            self.base_gravable_label.text = f"Base gravable: ${base_gravable:,.2f}"
            self.base_gravable_uvt_label.text = f"Base gravable en UVT: {base_gravable_uvt} UVT"
            self.impuesto_label.text = f"Impuesto de renta: ${impuesto:,.2f}"

            # Guardar en base de datos
            declaracion = Declaracion(
                id=None,
                fecha=None,
                ingresos_brutos_anuales=ingresos_brutos_anuales,
                aportes_salud_pension=aportes_salud_pension,
                numero_dependientes=numero_dependientes,
                intereses_credito_hipotecario=intereses_credito_hipotecario,
                base_gravable=base_gravable,
                base_gravable_uvt=base_gravable_uvt,
                impuesto_renta=impuesto,
                mensaje_error=None
            )
            ControladorDeclaraciones.InsertarDeclaracion(declaracion)

        except (IngresosNegativosError, DependientesExcedidoError,
                AportesSaludExcedidoError, IngresosInferioresAlMinimoError) as e:

            self.mostrar_popup("Error", str(e))

            # Registrar en base de datos con mensaje de error
            try:
                declaracion = Declaracion(
                    id=None,
                    fecha=None,
                    ingresos_brutos_anuales=float(self.ingresos_input.text),
                    aportes_salud_pension=float(self.aportes_input.text),
                    numero_dependientes=int(self.dependientes_input.text),
                    intereses_credito_hipotecario=float(self.intereses_input.text),
                    base_gravable=None,
                    base_gravable_uvt=None,
                    impuesto_renta=None,
                    mensaje_error=str(e)
                )
                ControladorDeclaraciones.InsertarDeclaracion(declaracion)
            except:
                pass  # No registrar si fallan las conversiones

        except ValueError:
            self.mostrar_popup("Error", "Por favor, ingrese valores numéricos válidos.")
        except Exception as e:
            self.mostrar_popup("Error inesperado", str(e))


    # Muestra una ventana emergente con un mensaje de error o advertencia
    def mostrar_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Cerrar", on_press=lambda x: self.close_popup())
        content.add_widget(close_button)

        self.popup = Popup(title=title, content=content, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    # Cierra el popup
    def close_popup(self):
        self.popup.dismiss()

# Punto de entrada de la aplicación
if __name__ == "__main__":
    RentaApp().run()
