from flask import Flask, render_template, request, jsonify

from src.controller.ControladorDeclaraciones import ControladorDeclaraciones

app = Flask(__name__)
controlador = ControladorDeclaraciones()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/declaraciones')
def get_declaraciones():
    declaraciones = controlador.TodasDeclaraciones()
    return render_template('declaraciones.html', declaraciones=declaraciones)

@app.route('/declaracion/<int:id>')
def get_declaracion(id):
    declaracion = controlador.get_declaracion_by_id(id)
    if not declaracion:
        return "Declaración no encontrada", 404
    return render_template('declaracion_detalle.html', declaracion=declaracion)

@app.route('/api/declaraciones')
def api_declaraciones():
    declaraciones = []
    current_id = 1
    while True:
        declaracion = controlador.BuscarPorId(str(current_id))
        if not declaracion:
            break
        if isinstance(declaracion, list):
            declaraciones.extend(declaracion)
        else:
            declaraciones.append(declaracion)
        current_id += 1
    return jsonify([d.to_dict() if hasattr(d, 'to_dict') else d for d in declaraciones])

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    resultado = controlador.BuscarPorId(query)
    if resultado is None:
        declaraciones = []
    elif isinstance(resultado, list):
        declaraciones = resultado
    else:
        declaraciones = [resultado]
    return render_template('resultados.html', declaraciones=declaraciones)

if __name__ == '__main__':
    app.run()
