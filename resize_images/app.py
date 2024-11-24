from flask import Flask, request, send_file
import logging
from PIL import Image
import io

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename='resize_images.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif'}

@app.route('/', methods=['POST'])
def resize_image():
    try:
        file = request.files['file']
        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            logging.error(f"Invalid file format: {file.filename}")
            return "Invalid file format. Please upload a valid image file.", 400

        # Obtém dimensões desejadas
        width = int(request.form.get('width', 800))
        height = int(request.form.get('height', 600))

        # Abre e redimensiona a imagem
        image = Image.open(file)
        resized_image = image.resize((width, height), Image.Resampling.LANCZOS)

        # Salva a imagem em memória
        img_byte_arr = io.BytesIO()
        format_name = image.format if image.format else 'PNG'
        resized_image.save(img_byte_arr, format=format_name)
        img_byte_arr.seek(0)

        logging.info(f"Successfully resized {file.filename} to {width}x{height}")
        return send_file(
            img_byte_arr,
            mimetype=f'image/{format_name.lower()}',
            as_attachment=True,
            download_name=f"resized_{file.filename}"
        )

    except Exception as e:
        logging.error(f"Error resizing image: {str(e)}")
        return f"Error processing image: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003) 