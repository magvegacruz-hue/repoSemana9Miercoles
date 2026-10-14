from flask import Flask, render_template, request, jsonify

from modelo.pila import Pila

app = Flask(__name__)

pilas: dict[str, Pila] = {}


def obtener_pila() -> Pila:
    capacidad = request.session.get("capacidad") if hasattr(request, "session") else None
    return pilas.get("actual")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/crear", methods=["POST"])
def crear_pila():
    datos = request.get_json(silent=True) or {}
    try:
        capacidad = int(datos.get("capacidad", 0))
        pila = Pila(capacidad)
        pilas["actual"] = pila
        return jsonify({
            "exito": True,
            "mensaje": f"Pila creada con capacidad {capacidad}.",
            "elementos": pila.mostrar(),
            "cantidad": len(pila.elementos),
            "capacidad": pila.capacidad
        })
    except (TypeError, ValueError):
        return jsonify({
            "exito": False,
            "mensaje": "Ingresa una capacidad válida mayor que cero."
        }), 400


def pila_no_creada():
    return jsonify({
        "exito": False,
        "mensaje": "Primero debes crear la pila."
    }), 400


@app.route("/api/apilar", methods=["POST"])
def apilar():
    pila = pilas.get("actual")
    if pila is None:
        return pila_no_creada()

    datos = request.get_json(silent=True) or {}
    item = str(datos.get("item", "")).strip()

    if not item:
        return jsonify({
            "exito": False,
            "mensaje": "Escribe un valor para apilar."
        }), 400

    resultado = pila.apilar(item)
    return jsonify({
        **resultado,
        "elementos": pila.mostrar(),
        "cantidad": len(pila.elementos),
        "capacidad": pila.capacidad
    })


@app.route("/api/desapilar", methods=["POST"])
def desapilar():
    pila = pilas.get("actual")
    if pila is None:
        return pila_no_creada()

    resultado = pila.desapilar()
    return jsonify({
        **resultado,
        "elementos": pila.mostrar(),
        "cantidad": len(pila.elementos),
        "capacidad": pila.capacidad
    })


@app.route("/api/tope", methods=["GET"])
def ver_tope():
    pila = pilas.get("actual")
    if pila is None:
        return pila_no_creada()

    resultado = pila.ver_tope()
    return jsonify({
        **resultado,
        "elementos": pila.mostrar(),
        "cantidad": len(pila.elementos),
        "capacidad": pila.capacidad
    })


@app.route("/api/estado", methods=["GET"])
def estado():
    pila = pilas.get("actual")
    if pila is None:
        return jsonify({
            "exito": False,
            "mensaje": "No hay pila creada.",
            "elementos": [],
            "cantidad": 0,
            "capacidad": 0
        })

    return jsonify({
        "exito": True,
        "elementos": pila.mostrar(),
        "cantidad": len(pila.elementos),
        "capacidad": pila.capacidad,
        "vacia": pila.esta_vacia(),
        "llena": pila.esta_llena()
    })


if __name__ == "__main__":
    app.run(debug=True)