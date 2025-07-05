
from flask import Flask, render_template, request, redirect, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

ARCHIVO_COMPRAS = "compras.json"
ARCHIVO_HISTORIAL = "historial.json"
ARCHIVO_MOTOS_ROBADAS = "motos_robadas.json"
ARCHIVO_CONFIG = "config.json"

def cargar_o_crear(ruta, valor_defecto):
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            return json.load(f)
    with open(ruta, "w") as f:
        json.dump(valor_defecto, f)
    return valor_defecto

compras = cargar_o_crear(ARCHIVO_COMPRAS, [])
historial = cargar_o_crear(ARCHIVO_HISTORIAL, [])
motos_robadas = cargar_o_crear(ARCHIVO_MOTOS_ROBADAS, [])
config = cargar_o_crear(ARCHIVO_CONFIG, {"litros_moto": 5, "litros_auto": 10})

@app.route('/')
def index():
    return render_template("index.html", compras=compras)

@app.route('/registrar', methods=["POST"])
def registrar():
    carnet = request.form["carnet"]
    nombre = request.form["nombre"]
    chasis = request.form["chasis"]
    tipo = request.form["tipo"]

    for c in compras:
        if carnet == c["carnet"] and tipo == c["tipo"]:
            return "RECHAZADO: Ya compró para este tipo.", 400
        if nombre == c["nombre"] or chasis == c["chasis"]:
            return "RECHAZADO: Datos ya usados.", 400

    if any(chasis.endswith(r[-3:]) for r in motos_robadas):
        return "ALERTA: Moto con denuncia de robo.", 400

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = {"carnet": carnet, "nombre": nombre, "chasis": chasis, "tipo": tipo, "fecha": fecha}
    compras.append(registro)
    historial.append(registro)

    with open(ARCHIVO_COMPRAS, "w") as f:
        json.dump(compras, f)
    with open(ARCHIVO_HISTORIAL, "w") as f:
        json.dump(historial, f)

    return redirect("/")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
