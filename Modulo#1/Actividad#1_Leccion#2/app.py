from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/info", methods=["GET"])
def info():
    mensaje = """Servidor sencillo con JSON
    Demuestra la integración y manejo de datos en formato JSON.
    
    Cuenta con dos rutas principales:
            - 'GET' /info
            - 'POST' /mensaje"""
    
    return f"<pre>{mensaje}</pre>"

@app.route("/mensaje", methods=["POST"])
def saludo():
    data = request.json
    
    if not data or "usuario" not in data:
        return jsonify({"error": "El campo 'usuario' es requerido"}), 400

    usuario = data["usuario"]
    return jsonify({"mensaje": f"Hola, {usuario}!"})

if __name__ == "__main__":
    app.run(debug=True)