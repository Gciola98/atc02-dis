from flask import Flask, request, send_file
import logging
from PIL import Image
import io
import os

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename='convert_images.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif'}
FORMAT_MIME_TYPES = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'tiff': 'image/tiff'
}

@app.route('/', methods=['POST'])
def convert_image():
    try:
        file = request.files['file']
        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            logging.error(f"Invalid file format: {file.filename}")
            return "Invalid file format. Please upload a valid image file.", 400

        # Obtém formato de destino
        target_format = request.form.get('format', 'png').lower()
        if target_format not in ['png', 'jpg', 'tiff']:
            return "Invalid target format. Use 'png', 'jpg', or 'tiff'", 400

        # Abre a imagem
        image = Image.open(file)

        # Converte para RGB se necessário (para JPG)
        if target_format == 'jpg' and image.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background

        # Salva a imagem convertida em memória
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=target_format.upper())
        img_byte_arr.seek(0)

        # Define o novo nome do arquivo
        filename_without_ext = os.path.splitext(file.filename)[0]
        new_filename = f"{filename_without_ext}.{target_format}"

        logging.info(f"Successfully converted {file.filename} to {target_format}")
        return send_file(
            img_byte_arr,
            mimetype=FORMAT_MIME_TYPES[target_format],
            as_attachment=True,
            download_name=new_filename
        )

    except Exception as e:
        logging.error(f"Error converting image: {str(e)}")
        return f"Error converting image: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004) 