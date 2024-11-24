from flask import Flask, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='pdf2txt.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/', methods=['POST'])
def convert_pdf_to_txt():
    try:
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return "Invalid file format. Please upload a PDF file.", 400

        # Cria diretório temporário se não existir
        if not os.path.exists('/tmp/conversions'):
            os.makedirs('/tmp/conversions')

        input_path = f"/tmp/conversions/{file.filename}"
        output_path = f"/tmp/conversions/{os.path.splitext(file.filename)[0]}.txt"
        
        # Salva o arquivo temporariamente
        file.save(input_path)

        # Usa pdftotext (do poppler-utils) para converter
        subprocess.run(['pdftotext', input_path, output_path], check=True)

        return send_file(
            output_path,
            mimetype='text/plain',
            as_attachment=True,
            download_name=os.path.basename(output_path)
        )

    except Exception as e:
        logging.error(f"Error converting PDF to text: {str(e)}")
        return f"Error converting PDF: {str(e)}", 500
    finally:
        # Limpa os arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)