from flask import Flask
# To run the app

from src.view.web.blueprint import declaracion_renta_bp

app = Flask(__name__)

app.secret_key = "ñamñamñam" 

# Initialize the blueprint
app.register_blueprint(declaracion_renta_bp)


if __name__ == '__main__':
    app.run()
