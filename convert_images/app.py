from flask import Flask, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='convert_images.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.tif'}
ALLOWED_FORMATS = {'png', 'jpg', 'jpeg', 'tiff', 'tif'}
FORMAT_MIME_TYPES = {
    'png': 'image/png',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'tiff': 'image/tiff',
    'tif': 'image/tiff'
}

@app.route('/', methods=['POST'])
def convert_image():
    try:
        file = request.files['file']
        if not any(file.filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            return "Invalid file format. Please upload a valid image file.", 400

        # Obtém o formato de destino
        target_format = request.form.get('format', 'jpg').lower()
        if target_format not in ALLOWED_FORMATS:
            return f"Invalid target format. Allowed formats: {', '.join(ALLOWED_FORMATS)}", 400

        # Cria diretório temporário se não existir
        if not os.path.exists('/tmp/conversions'):
            os.makedirs('/tmp/conversions')

        input_path = f"/tmp/conversions/{file.filename}"
        filename_without_ext = os.path.splitext(file.filename)[0]
        output_path = f"/tmp/conversions/{filename_without_ext}.{target_format}"
        
        # Salva o arquivo temporariamente
        file.save(input_path)

        # Configurações específicas para cada formato
        convert_command = ['convert', input_path]
        
        if target_format in ['jpg', 'jpeg']:
            # Para JPG, converte para RGB e define qualidade
            convert_command.extend([
                '-background', 'white',
                '-flatten',  # Achata camadas e remove transparência
                '-quality', '90'
            ])
        elif target_format == 'png':
            # Para PNG, preserva transparência
            convert_command.extend([
                '-define', 'png:compression-level=9'  # Máxima compressão
            ])
        elif target_format in ['tiff', 'tif']:
            # Para TIFF, usa compressão LZW
            convert_command.extend([
                '-compress', 'lzw'
            ])

        # Adiciona o arquivo de saída ao comando
        convert_command.append(output_path)
        
        # Executa a conversão
        subprocess.run(convert_command, check=True)

        return send_file(
            output_path,
            mimetype=FORMAT_MIME_TYPES.get(target_format, 'application/octet-stream'),
            as_attachment=True,
            download_name=os.path.basename(output_path)
        )

    except Exception as e:
        logging.error(f"Error converting image: {str(e)}")
        return f"Error converting image: {str(e)}", 500
    finally:
        # Limpa os arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)