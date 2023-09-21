from flask import Flask, request, redirect, jsonify,send_file
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import io
import parser_1
import base64
from pymongo import MongoClient

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

client = MongoClient("mongodb+srv://chetan_325:chetan_325@cluster0.aopmq.mongodb.net/?retryWrites=true&w=majority")
db = client["raser"] 
collection = db["resumes"] 

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']

    if file:
        filename = file.filename
        binary_data = base64.b64encode(file.read())

        file_details = {
            'filename': filename,
            'data': binary_data.decode('utf-8')
        }

        collection.insert_one(file_details)

        return jsonify({'message': 'File uploaded and saved to database.'}), 200
    else:
        return jsonify({'message': 'No file uploaded.'}), 400

# Route to serve the PDF file
@app.route('/file/<filename>', methods=['GET'])
def get_file(filename):
    file = collection.find_one({'filename': filename})
    if file:
        binary_data = base64.b64decode(file['data'])
        return send_file(io.BytesIO(binary_data), mimetype='application/pdf')
    else:
        return jsonify({'message': 'File not found.'}), 404


class Test(Resource):
    def get(self):
        return 'Welcome to, Test App API!'

    def post(self):
        try:
            value = request.get_json()
            if(value):
                return {'Post Values': value}, 201

            return {"error":"Invalid format."}

        except Exception as error:
            return {'error': error}

class GetParsedOutput(Resource):
    def get(self):
        return {"error": "Invalid Method."}

    def post(self):
        try:
            if 'file' not in request.files:
                return {"error": "No file received."}

            file = request.files['file']

            if file and file.filename.endswith('.pdf'):
                uploaded_file_path = os.path.join("uploads", file.filename)
                file.save(uploaded_file_path)

                output = parser_1.nlpParser(uploaded_file_path)
                return {"Output": output}, 201

            return {"error": "Invalid file format. Please upload a PDF file."}

        except FileNotFoundError as error:
            return {'error': f'File not found: {error.filename}'}, 404  

        except Exception as error:
            return {'error': str(error)}, 500  

api.add_resource(Test,'/')
api.add_resource(GetParsedOutput,'/getOutput')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)