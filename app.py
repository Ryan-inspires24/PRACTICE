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
    
@app.route('/api/modify/<profession>', methods=['PUT'])
def modify_field(profession):
    required_data = request.get_json()
    updated_info = required_data.get('profession')
    
    file_path = f'static/testapi.json'
    try:
        with open(file_path, 'r') as file:
            original_data = json.load(file)
        if  not profession in original_data:
            return jsonify({
                'message' : f'Key : {profession} not found'
            }), 404
    except FileNotFoundError:
            return jsonify({
                'error' : 'File not Found'
            }), 500
    original_data['profession'] = updated_info
    
    with open(file_path, 'w') as update:
        json.dump(original_data, update, indent=4)
    return jsonify({
        'message' : f'Field with key: {profession} updated with success!'
    }), 200
        
@app.route('/api/patch/<data>/<admins>', methods=['PATCH'])
def patch_data(data, admins):
    patched_data = request.get_json()
    new_info = patched_data.get('clubId')
    
    file_path = f'static/testapi.json'
    try:    

        with open(file_path, 'r') as file:
            main_data = json.load(file)
    except FileNotFoundError :
        return jsonify({
            'error' : "File Not Found Error"
        }), 500
        
    try:
        main_data[data][admins][0]['clubId'] = new_info
    except (KeyError, IndexError):
        return jsonify({
            'Admins list or club Id jey not found'
        }),404
    with open(file_path, 'w') as file:
        json.dump(main_data, file, indent=4)
    return jsonify({
        'message':'Successful Patching of admins Data'
    })
        
if __name__== '__main__':
    app.run(debug = True)
    
