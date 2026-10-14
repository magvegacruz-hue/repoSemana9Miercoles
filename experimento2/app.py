import os

from flask import Flask, jsonify, render_template, request, send_from_directory

from modelo.foto import GestorFotos
from modelo.pila import Pila

app = Flask(__name__)

CARPETA_FOTOS = os.path.join(os.getcwd(), "uploads")

gestor_fotos = GestorFotos(CARPETA_FOTOS)
pila: Pila | None = None


def pila_no_creada():
    return jsonify({
        "exito": False,
        "mensaje": "Primero debes crear la pila."
    }), 400


def respuesta_pila(resultado: dict, incluir_elemento: bool = False):
    datos = {
        **resultado,
        "elementos": pila.mostrar(),
        "cantidad": len(pila.elementos),
        "capacidad": pila.capacidad
    }

    if incluir_elemento and "elemento" in resultado:
        datos["url"] = f"/foto/{resultado['elemento']}"

    return jsonify(datos)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/crear", methods=["POST"])
def crear_pila():
    global pila

    datos = request.get_json(silent=True) or {}

    try:
        capacidad = int(datos.get("capacidad", 0))
        pila = Pila(capacidad)

        return respuesta_pila({
            "exito": True,
            "mensaje": f"Pila creada con capacidad para {capacidad} fotos."
        })

    except (TypeError, ValueError):
        return jsonify({
            "exito": False,
            "mensaje": "Ingresa una capacidad válida mayor que cero."
        }), 400


@app.route("/api/capturar", methods=["POST"])
def capturar_foto():
    global pila

    if pila is None:
        return pila_no_creada()

    datos = request.get_json(silent=True) or {}
    imagen = datos.get("imagen", "")

    resultado_archivo = gestor_fotos.guardar_base64(imagen)

    if not resultado_archivo["exito"]:
        return jsonify(resultado_archivo), 400

    nombre = resultado_archivo["nombre"]
    resultado_pila = pila.apilar(nombre)

    if not resultado_pila["exito"]:
        gestor_fotos.eliminar(nombre)

        return jsonify({
            **resultado_pila,
            "elementos": pila.mostrar(),
            "cantidad": len(pila.elementos),
            "capacidad": pila.capacidad
        }), 400

    return respuesta_pila({
        **resultado_pila,
        "elemento": nombre
    }, incluir_elemento=True)


@app.route("/api/desapilar", methods=["POST"])
def desapilar_foto():
    global pila

    if pila is None:
        return pila_no_creada()

    resultado = pila.desapilar()

    if resultado["exito"]:
        gestor_fotos.eliminar(resultado["elemento"])

    return respuesta_pila(resultado, incluir_elemento=True)


@app.route("/api/tope", methods=["GET"])
def ver_tope():
    if pila is None:
        return pila_no_creada()

    resultado = pila.ver_tope()

    return respuesta_pila(resultado, incluir_elemento=True)


@app.route("/api/estado", methods=["GET"])
def estado():
    if pila is None:
        return jsonify({
            "exito": False,
            "mensaje": "No hay pila creada.",
            "elementos": [],
            "cantidad": 0,
            "capacidad": 0
        })

    return respuesta_pila({
        "exito": True,
        "mensaje": "Estado actualizado."
    })


@app.route("/foto/<nombre>")
def ver_foto(nombre):
    return send_from_directory(CARPETA_FOTOS, nombre)


if __name__ == "__main__":
    app.run(debug=True)