from flask import Flask, jsonify, request, render_template, url_for

app = Flask(__name__)

next_day_id = 2
data = {
    "days": [
        {
            "id": 1,
            "date": "Viernes, 9 de mayo de 2025",
            "costs": [
                {"name": "Gasolina", "cost": 30.0},
                {"name": "Almuerzo", "cost": 12.75}
            ]
        }
    ]
}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", data=data, message=None)

@app.route("/day", methods=["GET", "POST"])
def dayForm():
    global next_day_id
    if request.method == "POST":
        json_data = request.get_json()
        date = json_data.get("day")

        if not date:
            return jsonify({"error": "Date is required"}), 400

        
        new_day = {
            "id": next_day_id,
            "date": date,
            "costs": []
        }
        data["days"].append(new_day)
        next_day_id += 1

        return jsonify({"redirectUrl": url_for("displayDay", day_id=new_day["id"])})

    return render_template("newDay.html", data='', message=None)


@app.route("/day/<int:day_id>", methods=["GET"])
def displayDay(day_id):
    selectedDay = next((day for day in data["days"] if day["id"] == day_id), None)
    print(f"Dia seleccionado, {selectedDay}")
    if not selectedDay:
        return "Día no encontrado", 404
    return render_template("dayCost.html", data=selectedDay, message=None)

@app.route("/day/<int:day_id>/cost", methods=["POST"])
def addCost(day_id):
    selectedDay = next((day for day in data["days"] if day["id"] == day_id), None)
    print(f"Día seleccionado: {selectedDay}")

    if not selectedDay:
        return jsonify({"error": "Día no encontrado"}), 404

    request_data = request.json
    cost = request_data.get('cost')
    costName = request_data.get('costName')

    if costName is None or cost is None:
        return jsonify({"error": "Nombre y valor del costo son requeridos"}), 400

    newCost = {
        "name": costName,
        "cost": float(cost)
    }

    selectedDay["costs"].append(newCost)

    return jsonify({
        "message": "Costo agregado exitosamente",
        "day": selectedDay
    }), 201

@app.route("/day/<int:day_id>/cost", methods=["DELETE"])
def deleteCost(day_id):
    selectedDay = next((day for day in data["days"] if day["id"] == day_id), None)
    print(f"Día seleccionado: {selectedDay}")

    if not selectedDay:
        return jsonify({"error": "Día no encontrado"}), 404

    request_data = request.json
    costName = request_data.get("costName")

    if not costName:
        return jsonify({"error": "Nombre del costo requerido"}), 400

    original_length = len(selectedDay["costs"])
    selectedDay["costs"] = [
        cost for cost in selectedDay["costs"] if cost["name"] != costName
    ]

    if len(selectedDay["costs"]) == original_length:
        return jsonify({"error": "Costo no encontrado"}), 404

    return jsonify({
        "message": "Costo eliminado exitosamente",
        "day": selectedDay
    }), 200

    
if __name__ == "__main__":
    app.run(debug=True)