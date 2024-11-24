from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename='main_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Configuração dos serviços
SERVICES = {
    "pdf2txt": "http://pdf2txt:5001/",
    "reduce_resolution": "http://reduce_resolution:5002/",
    "resize_images": "http://resize_images:5003/",
    "convert_images": "http://convert_images:5004/"
}

@app.route('/pdf2txt', methods=['POST'])
def pdf2txt_route():
    try:
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            logging.error(f"Invalid file format: {file.filename}")
            return jsonify({"error": "Invalid file format. Please upload a PDF file."}), 400
            
        files = {'file': file}
        response = requests.post(SERVICES["pdf2txt"], files=files)
        logging.info(f"PDF to TXT conversion requested for file: {file.filename}")
        return response.content, response.status_code
    except Exception as e:
        logging.error(f"Error in PDF to TXT conversion: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/reduce-resolution', methods=['POST'])
def reduce_resolution_route():
    try:
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            logging.error(f"Invalid file format: {file.filename}")
            return jsonify({"error": "Invalid file format. Please upload a PDF file."}), 400
            
        files = {'file': file}
        dpi = request.form.get('dpi', 150)  # DPI padrão de 150
        data = {'dpi': dpi}
        
        response = requests.post(SERVICES["reduce_resolution"], files=files, data=data)
        logging.info(f"PDF resolution reduction requested for file: {file.filename}")
        return response.content, response.status_code
    except Exception as e:
        logging.error(f"Error in PDF resolution reduction: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/resize-image', methods=['POST'])
def resize_image_route():
    try:
        file = request.files['file']
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif')):
            logging.error(f"Invalid file format: {file.filename}")
            return jsonify({"error": "Invalid file format. Please upload an image file."}), 400
            
        files = {'file': file}
        width = request.form.get('width')
        height = request.form.get('height')
        data = {'width': width, 'height': height}
        
        response = requests.post(SERVICES["resize_images"], files=files, data=data)
        logging.info(f"Image resize requested for file: {file.filename}")
        return response.content, response.status_code
    except Exception as e:
        logging.error(f"Error in image resize: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/convert-image', methods=['POST'])
def convert_image_route():
    try:
        file = request.files['file']
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.tif')):
            logging.error(f"Invalid file format: {file.filename}")
            return jsonify({"error": "Invalid file format. Please upload an image file."}), 400
            
        files = {'file': file}
        target_format = request.form.get('format', 'png').lower()
        if target_format not in ['png', 'jpg', 'tiff']:
            return jsonify({"error": "Invalid target format. Use 'png', 'jpg', or 'tiff'"}), 400
            
        data = {'format': target_format}
        
        response = requests.post(SERVICES["convert_images"], files=files, data=data)
        logging.info(f"Image conversion requested for file: {file.filename}")
        return response.content, response.status_code
    except Exception as e:
        logging.error(f"Error in image conversion: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/healthcheck')
def health_check():
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 