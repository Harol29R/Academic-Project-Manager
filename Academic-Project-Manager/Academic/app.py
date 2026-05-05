from flask import Flask, render_template, request, redirect, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import mysql.connector
import io
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'pdfs'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="trabajos_db"
)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/listar')
def listar():
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT id, titulo_trabajo, tipo_trabajo, autor, curso, especialidad 
        FROM trabajos
    """)
    
    trabajos = cursor.fetchall()
    
    return render_template('listar.html', trabajos=trabajos)

@app.route('/pdf/<int:id>')
def generar_pdf(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trabajos WHERE id=%s", (id,))
    trabajo = cursor.fetchone()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    contenido = []

    # Texto
    contenido.append(Paragraph(f"<b>Título:</b> {trabajo['titulo_trabajo']}", styles['Normal']))
    contenido.append(Paragraph(f"<b>Tipo:</b> {trabajo['tipo_trabajo']}", styles['Normal']))
    contenido.append(Paragraph(f"<b>Autor:</b> {trabajo['autor']}", styles['Normal']))
    contenido.append(Paragraph(f"<b>Curso:</b> {trabajo['curso']}", styles['Normal']))
    contenido.append(Paragraph(f"<b>Especialidad:</b> {trabajo['especialidad']}", styles['Normal']))
    contenido.append(Paragraph(f"<b>Ciudad:</b> {trabajo['ciudad']}", styles['Normal']))
    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph(f"<b>Resumen:</b> {trabajo['resumen']}", styles['Normal']))
    contenido.append(Spacer(1, 20))

    # Imagen desde BD
    if trabajo['imagen']:
        img_bytes = io.BytesIO(trabajo['imagen'])
        img = Image(img_bytes, width=200, height=150)
        contenido.append(img)

    doc.build(contenido)

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="trabajo.pdf", mimetype='application/pdf')

@app.route('/guardar', methods=['POST'])
def guardar():
    cursor = db.cursor()

    titulo = request.form['titulo']
    tipo = request.form['tipo']
    autor = request.form['autor']
    universidad = request.form['universidad']
    palabras = request.form['palabras']
    resumen = request.form['resumen']
    curso = request.form['curso']
    ciudad = request.form['ciudad']
    especialidad = request.form['especialidad']

    # Imagen (guardada en BD)
    imagen = request.files['imagen'].read()

    # PDF (guardado en carpeta)
    pdf = request.files['pdf']
    pdf_nombre = pdf.filename
    pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_nombre))
    

    sql = """INSERT INTO trabajos 
    (titulo_trabajo, tipo_trabajo, autor, universidad, palabras_claves, resumen, curso, imagen, pdf, ciudad, especialidad)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

    valores = (titulo, tipo, autor, universidad, palabras, resumen, curso, imagen, pdf_nombre, ciudad, especialidad)

    cursor.execute(sql, valores)
    db.commit()

    return "Guardado correctamente"

if __name__ == '__main__':
    app.run(debug=True)