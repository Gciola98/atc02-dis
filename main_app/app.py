from flask import Flask, request, jsonify
import requests
import logging
import os

app = Flask(__name__)

logging.basicConfig(
    filename='main_app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URLs dos serviços
SERVICES = {
    'pdf2txt': 'http://pdf2txt:5001',
    'reduce_resolution': 'http://reduce_resolution:5002',
    'resize_images': 'http://resize_images:5003',
    'convert_images': 'http://convert_images:5004'
}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/convert/pdf2txt', methods=['POST'])
def convert_pdf_to_txt():
    try:
        if 'file' not in request.files:
            return "No file provided", 400
        
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return "Invalid file format. Please upload a PDF file.", 400

        response = requests.post(
            SERVICES['pdf2txt'],
            files={'file': (file.filename, file.stream, file.content_type)}
        )
        
        return response.content, response.status_code, response.headers.items()

    except Exception as e:
        logging.error(f"Error in pdf2txt conversion: {str(e)}")
        return f"Error in conversion: {str(e)}", 500

@app.route('/convert/reduce_resolution', methods=['POST'])
def reduce_pdf_resolution():
    try:
        if 'file' not in request.files:
            return "No file provided", 400
        
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return "Invalid file format. Please upload a PDF file.", 400

        # Obtém o DPI dos parâmetros do formulário
        dpi = request.form.get('dpi', '150')
        
        response = requests.post(
            SERVICES['reduce_resolution'],
            files={'file': (file.filename, file.stream, file.content_type)},
            data={'dpi': dpi}
        )
        
        return response.content, response.status_code, response.headers.items()

    except Exception as e:
        logging.error(f"Error in PDF resolution reduction: {str(e)}")
        return f"Error in conversion: {str(e)}", 500

@app.route('/convert/resize_image', methods=['POST'])
def resize_image():
    try:
        if 'file' not in request.files:
            return "No file provided", 400

        file = request.files['file']
        width = request.form.get('width', '800')
        height = request.form.get('height', '600')

        response = requests.post(
            SERVICES['resize_images'],
            files={'file': (file.filename, file.stream, file.content_type)},
            data={'width': width, 'height': height}
        )
        
        return response.content, response.status_code, response.headers.items()

    except Exception as e:
        logging.error(f"Error in image resizing: {str(e)}")
        return f"Error in conversion: {str(e)}", 500

@app.route('/convert/image_format', methods=['POST'])
def convert_image_format():
    try:
        if 'file' not in request.files:
            return "No file provided", 400

        file = request.files['file']
        target_format = request.form.get('format', 'jpg')

        response = requests.post(
            SERVICES['convert_images'],
            files={'file': (file.filename, file.stream, file.content_type)},
            data={'format': target_format}
        )
        
        return response.content, response.status_code, response.headers.items()

    except Exception as e:
        logging.error(f"Error in image format conversion: {str(e)}")
        return f"Error in conversion: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)