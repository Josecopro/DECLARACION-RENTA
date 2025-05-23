from flask import Flask, render_template, request, redirect, url_for
# To run the app

from src.view.web.blueprint import DeclaracionRentaApp

app = Flask(__name__)

# Initialize the blueprint
declaracion_renta_app = DeclaracionRentaApp()
app.register_blueprint(declaracion_renta_app.blueprint)


if __name__ == '__main__':
    app.run()
