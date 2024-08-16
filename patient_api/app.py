from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# In-memory "database"
patients = {}


# POST /patients - Add a new patient record
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    if not data.get('name') or not isinstance(data.get('age'), int) or not data.get('gender'):
        return jsonify({"error": "Invalid data"}), 400

    patient_id = str(len(patients) + 1)
    patients[patient_id] = {
        "id": patient_id,
        "name": data['name'],
        "age": data['age'],
        "gender": data['gender'],
        "diagnosis": data.get('diagnosis', '')
    }
    return jsonify(patients[patient_id]), 201


# GET /patients/{id} - Retrieve patient details by ID
@app.route('/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    if patient_id not in patients:
        abort(404)
    return jsonify(patients[patient_id]), 200


# PUT /patients/{id} - Update patient information
@app.route('/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    if patient_id not in patients:
        abort(404)

    data = request.json
    if data.get('name'):
        patients[patient_id]['name'] = data['name']
    if data.get('age') and isinstance(data.get('age'), int):
        patients[patient_id]['age'] = data['age']
    if data.get('gender'):
        patients[patient_id]['gender'] = data['gender']
    if data.get('diagnosis'):
        patients[patient_id]['diagnosis'] = data['diagnosis']

    return jsonify(patients[patient_id]), 200


# DELETE /patients/{id} - Remove a patient record
@app.route('/patients/<patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    if patient_id not in patients:
        abort(404)
    del patients[patient_id]
    return '', 204


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
