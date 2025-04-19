from flask import Flask, request, jsonify
app = Flask(__name__)

usuarios = []

@app.route("/info", methods=["GET"])
def info():
    mensaje = (
        "Servidor Sencillo con JSON"
        "Maneja la solicitud de devolver los usuarios almacenados en el sistema "
        "y permite la creación de un nuevo usuario validando estos campos."
        "Cuenta con tres rutas principales:"
        "  - 'GET' /info"
        "  - 'GET' /usuarios"
        "  - 'POST' /crear_usuario"
    )

    return jsonify({"mensaje": mensaje})



@app.route("/crear_usuario", methods=["POST"])
def create_usuario():
    data = request.json

    nombre = data.get("nombre")
    correo = data.get("correo")

    if not nombre or not correo:
        return jsonify({"error": "Se requieren los campos 'nombre' y 'correo'"}), 400

    nuevo_usuario = {"nombre": nombre, "correo": correo}
    usuarios.append(nuevo_usuario)

    return jsonify({"mensaje": "Usuario creado exitosamente", "usuario": nuevo_usuario}), 201


@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return jsonify({"usuarios": usuarios})
if __name__ == "__main__":
    app.run(debug=True)