from flask import Flask, request, send_file
import subprocess
import os
import logging

app = Flask(__name__)

logging.basicConfig(
    filename='reduce_resolution.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@app.route('/', methods=['POST'])
def reduce_resolution():
    try:
        file = request.files['file']
        if not file.filename.endswith('.pdf'):
            return "Invalid file format. Please upload a PDF file.", 400

        # Obtém o DPI desejado (padrão: 150)
        dpi = request.form.get('dpi', '150')

        # Cria diretório temporário se não existir
        if not os.path.exists('/tmp/conversions'):
            os.makedirs('/tmp/conversions')

        input_path = f"/tmp/conversions/{file.filename}"
        output_path = f"/tmp/conversions/reduced_{file.filename}"
        
        # Salva o arquivo temporariamente
        file.save(input_path)

        # Usa ghostscript para reduzir a resolução
        gs_command = [
            'gs',
            '-sDEVICE=pdfwrite',
            '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS=/ebook',  # Configuração de qualidade
            f'-dDownsampleColorImages=true',
            f'-dColorImageResolution={dpi}',
            f'-dDownsampleGrayImages=true',
            f'-dGrayImageResolution={dpi}',
            f'-dDownsampleMonoImages=true',
            f'-dMonoImageResolution={dpi}',
            '-dNOPAUSE',
            '-dBATCH',
            '-dQUIET',
            f'-sOutputFile={output_path}',
            input_path
        ]
        
        subprocess.run(gs_command, check=True)

        return send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=os.path.basename(output_path)
        )

    except Exception as e:
        logging.error(f"Error reducing PDF resolution: {str(e)}")
        return f"Error reducing PDF resolution: {str(e)}", 500
    finally:
        # Limpa os arquivos temporários
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)