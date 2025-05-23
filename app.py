from flask import Flask, render_template, request, Blueprint


from src.controller.ControladorDeclaraciones import ControladorDeclaraciones



app = Flask(__name__)


blueprint = Blueprint('declaracion_renta', __name__, template_folder='templates')
@blueprint.route('/')
def index():
    return render_template('index.html')

@blueprint.route('/buscar')
def buscar():
    controlador = ControladorDeclaraciones()
    query = request.args.get('q', '')
    resultado = controlador.BuscarPorId(query)
    if resultado is None:
        declaraciones = []
    elif isinstance(resultado, list):
        declaraciones = resultado
    else:
        declaraciones = [resultado]
    return render_template('resultados.html', declaraciones=declaraciones)

# To run the app
if __name__ == '__main__':
    app.register_blueprint(blueprint)
    app.run(debug=True)
