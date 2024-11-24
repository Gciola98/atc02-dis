from flask import Flask, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

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
            return "Invalid file format. Please upload a valid image file.", 400

        # Obtém dimensões desejadas
        width = request.form.get('width', '800')
        height = request.form.get('height', '600')

        # Cria diretório temporário se não existir
        if not os.path.exists('/tmp/conversions'):
            os.makedirs('/tmp/conversions')

        input_path = f"/tmp/conversions/{file.filename}"
        output_path = f"/tmp/conversions/resized_{file.filename}"
        
        # Salva o arquivo temporariamente
        file.save(input_path)

        # Usa ImageMagick (convert) para redimensionar
        convert_command = [
            'convert',
            input_path,
            '-resize',
            f'{width}x{height}',
            '-quality', '90',  # Qualidade da imagem (para JPG)
            output_path
        ]
        
        subprocess.run(convert_command, check=True)

        # Determina o tipo MIME baseado na extensão
        extension = os.path.splitext(file.filename)[1].lower()
        mime_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.tiff': 'image/tiff',
            '.tif': 'image/tiff'
        }
        mime_type = mime_types.get(extension, 'application/octet-stream')

        return send_file(
            output_path,
            mimetype=mime_type,
            as_attachment=True,
            download_name=os.path.basename(output_path)
        )

    except Exception as e:
        logging.error(f"Error resizing image: {str(e)}")
        return f"Error resizing image: {str(e)}", 500
    finally:
        # Limpa os arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)