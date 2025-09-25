from flasgger import Swagger
from Projeto import create_app
from flask import request, render_template, flash

# Cria o app
app = create_app()

# executar: flask --app app run
# abrir no navegador: http://127.0.0.1:5000/apidocs

if __name__ == "__main__":
    app.run(debug=True)

