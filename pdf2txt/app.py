from flask import Flask, request, send_file
import os
import logging
from PyPDF2 import PdfReader
import io

app = Flask(__name__)

# Configuração do logging
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
            logging.error(f"Invalid file format: {file.filename}")
            return "Invalid file format. Please upload a PDF file.", 400

        # Lê o PDF e extrai o texto
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        # Cria um arquivo de texto em memória
        text_io = io.StringIO(text)
        
        logging.info(f"Successfully converted {file.filename} to text")
        return send_file(
            io.BytesIO(text.encode()),
            mimetype='text/plain',
            as_attachment=True,
            download_name=f"{os.path.splitext(file.filename)[0]}.txt"
        )

    except Exception as e:
        logging.error(f"Error converting PDF to text: {str(e)}")
        return f"Error converting PDF: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) 