from flask import Flask, request, redirect
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import parser_1

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

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