from flask import Flask, render_template, request, jsonify


from src.controller.ControladorDeclaraciones import ControladorDeclaraciones

class DeclaracionRentaApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.controlador = ControladorDeclaraciones()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/declaraciones')
        def get_declaraciones():
            declaraciones = self.controlador.TodasDeclaraciones()
            return render_template('declaraciones.html', declaraciones=declaraciones)

        @self.app.route('/declaracion/<int:id>')
        def get_declaracion(id):
            declaracion = self.controlador.get_declaracion_by_id(id)
            if not declaracion:
                return "Declaración no encontrada", 404
            return render_template('declaracion_detalle.html', declaracion=declaracion)

        @self.app.route('/api/declaraciones')
        def api_declaraciones():
            declaraciones = []
            current_id = 1
            while True:
                declaracion = self.controlador.BuscarPorId(str(current_id))
                if not declaracion:
                    break
                if isinstance(declaracion, list):
                    declaraciones.extend(declaracion)
                else:
                    declaraciones.append(declaracion)
                current_id += 1
            return jsonify([d.to_dict() if hasattr(d, 'to_dict') else d for d in declaraciones])

        @self.app.route('/buscar')
        def buscar():
            query = request.args.get('q', '')
            resultado = self.controlador.BuscarPorId(query)
            if resultado is None:
                declaraciones = []
            elif isinstance(resultado, list):
                declaraciones = resultado
            else:
                declaraciones = [resultado]
            return render_template('resultados.html', declaraciones=declaraciones)

    def run(self, **kwargs):
        self.app.run(**kwargs)

# To run the app
if __name__ == '__main__':
    app_instance = DeclaracionRentaApp()
    app_instance.run(debug=True)
