from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)
@app.route('/')
def index():
    return render_template('index.html')

#Route to store json request from the request body, and update information in the static json file by overwrittng the existing infromation with the updated version
#Post route.
@app.route('/api/test', methods=['POST'])
def api_test():
    required_data = request.get_json()
    filename = required_data.get('filename')
    new_info = required_data.get('fellow_data')
    if not filename or not new_info:
        return jsonify({
            'error' : 'Missing Data or File'
        }) 
    filePath = f'static/{filename}'
    try:
        with open(filePath, 'r') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        current_data = {}
    current_data['fellow_data'] = new_info
    
    with open(filePath, 'w') as file:
        json.dump(current_data, file, indent=4)
        
    return jsonify({
        'message': f" Information saved to {filename} successfully "
    })    
           
#Route to Delete an entity in a json object
@app.route('/api/delete/<Name>', methods=['DELETE'])
def delete_field(Name):
    file_path = f'static/testapi.json'
    with open(file_path, 'r') as file:
        new_data = json.load(file)
        
    if Name in new_data:
        del new_data[Name]        
    else:
        return jsonify({
            'message' : f'Key : {Name} not found'
            
        }), 200
    with open(file_path, 'w') as file:
        json.dump(new_data, file, indent=4)
    return jsonify({
        'message': f'Deletion of object with key : {Name} successful!'
    }),200
if __name__== '__main__':
    app.run(debug = True)
    
    