from flask import Flask, request, send_file
import logging
import os
from PIL import Image
import io
import fitz  # PyMuPDF

app = Flask(__name__)

# Configuração do logging
logging.basicConfig(
    filename='reduce_resolution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def reduce_pdf_resolution(pdf_file, dpi):
    # Abre o PDF
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    output = fitz.open()

    for page in pdf_document:
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Converte a imagem de volta para PDF
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PDF')
        img_byte_arr.seek(0)
        
        # Adiciona a página ao novo PDF
        output.insert_pdf(fitz.open("pdf", img_byte_arr))

    # Salva o PDF em memória
    pdf_bytes = io.BytesIO()
    output.save(pdf_bytes)
    pdf_bytes.seek(0)
    
    return pdf_bytes

@app.route('/', methods=['POST'])
def reduce_resolution():
    try:
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            logging.error(f"Invalid file format: {file.filename}")
            return "Invalid file format. Please upload a PDF file.", 400

        dpi = int(request.form.get('dpi', 150))
        
        # Reduz a resolução do PDF
        output_pdf = reduce_pdf_resolution(file, dpi)
        
        logging.info(f"Successfully reduced resolution of {file.filename}")
        return send_file(
            output_pdf,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"reduced_{file.filename}"
        )

    except Exception as e:
        logging.error(f"Error reducing PDF resolution: {str(e)}")
        return f"Error processing PDF: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002) 