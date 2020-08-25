from reportlab.pdfgen import canvas
import sqlite3


def generatePDF():
    global nome_pdf
    con = sqlite3.connect("Personagens.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    query = "SELECT * FROM herois WHERE id = {}".format(1)
    cur.execute(query)

    result = [dict(row) for row in cur.fetchall()]
    for row in result:
        result = row
    try:
        nome_pdf = input("digite o nome do arquivo:")
        pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
        x = 720
        pdf.setTitle(nome_pdf)
        pdf.setFont("Times-Bold", 20)
        pdf.drawString(200,750, 'Ficha de Personagem')
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(200,728, 'ID: {}'.format(result.get('id')))
        pdf.drawString(200, 716, 'Nome: {}'.format(result.get('nome')))
        pdf.drawString(200, 704, 'Status: {}'.format(result.get('status')))
        pdf.drawString(200, 692, 'CA: {}'.format(result.get('ca')))
        pdf.drawString(200, 680, 'PV: {}'.format(result.get('pv')))
        pdf.drawString(200, 668, 'PV Maximo: {}'.format(result.get('pvmax')))
        pdf.drawString(200, 656, 'FORT: {}'.format(result.get('fort')))
        pdf.drawString(200, 644, 'VON: {}'.format(result.get('von')))
        pdf.drawString(200, 632, 'REF: {}'.format(result.get('ref')))
        pdf.save()
        print('{}.pdf criado com sucesso!'.format(nome_pdf))
    except:
        print('Erro ao gerar {}.pdf'.format(nome_pdf))


