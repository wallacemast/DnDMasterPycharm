from tkinter import *
from tkinter import messagebox
import sqlite3
from reportlab.pdfgen import canvas
from PIL import ImageTk,Image


con = sqlite3.connect("Personagens.db")
cur = con.cursor()

# ------------------------------- CRIA TABELA HEROIS SE NÃO EXISTIR -------------------------------------#
cur.execute('''
CREATE TABLE if not exists herois (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    status TEXT NOT NULL,
    ca INTEGER NOT NULL,
    pv INTEGER NOT NULL,
    pvmax INTEGER NOT NULL,
    fort INTEGER NOT NULL,
    von INTEGER NOT NULL,
    ref INTEGER NOT NULL);
''')


class FirstWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        self.title('Cadastro de Personagem')
        self.iconbitmap('imagens\\dnd.ico')
        self.configure(background='green')
        self.configure(relief=GROOVE)
        self.configure(borderwidth="2")
        Label(self, text='CADASTRAR NOVO HERÓI', font=('Ariel', '30'), bg='green').place(relx=0.3, rely=0.01)

        # ----------------------------------------CAMPO NOME ----------------------------------------------------#
        Label(self, text='NOME', font=('Arial', '12'), bg='green').place(relx=0.02, rely=0.10)
        self.nome = Entry(self, font=('Arial', '20'))
        self.nome.place(relx=0.02, rely=0.14)

        # -------------------------------------- CAMPO STATUS ---------------------------------------------------#
        Label(self, text='STATUS', font=('Arial', '12'), bg='green').place(relx=0.25, rely=0.10)
        self.status = Spinbox(self, values=("vivo", "inconsciente", "morto"), font=('Ariel', '20'), width=11)
        self.status.place(relx=0.25, rely=0.14)

        # -------------------------------------- CAMPO CA -------------------------------   -----------------------#
        Label(self, text='CA', font=('Arial', '12'), bg='green').place(relx=0.39, rely=0.10)
        self.ca = Entry(self, font=('Arial', '20'), width=2)
        self.ca.place(relx=0.39, rely=0.14)

        # ----------------------------------------CAMPO PV ------------------------------------------------------#
        Label(self, text='PV', font=('Arial', '12'), bg='green').place(relx=0.42, rely=0.10)
        self.pv = Entry(self, font=('Arial', '20'), width=2)
        self.pv.place(relx=0.42, rely=0.14)

        # ----------------------------------------CAMPO PVMAX ------------------------------------------------------#
        Label(self, text='PX', font=('Ariel', '12'), bg='green').place(relx=0.45, rely=0.10)
        self.pvmax = Entry(self, font=('Ariel', '20'), width=3)
        self.pvmax.place(relx=0.45, rely=0.14)

        # ----------------------------------------CAMPO FORT -----------------------------------------------------#
        Label(self, text='FORT', font=('Arial', '12'), bg='green').place(relx=0.02, rely=0.60)
        self.fort = Entry(self, font=('Arial', '20'), width=3)
        self.fort.place(relx=0.02, rely=0.64)

        # ----------------------------------------CAMPO VON -----------------------------------------------------#
        Label(self, text='VON', font=('Arial', '12'), bg='green').place(relx=0.02, rely=0.70)
        self.von = Entry(self, font=('Arial', '20'), width=3)
        self.von.place(relx=0.02, rely=0.74)

        # ----------------------------------------CAMPO REF -----------------------------------------------------#
        Label(self, text='REF', font=('Arial', '12'), bg='green').place(relx=0.02, rely=0.80)
        self.ref = Entry(self, font=('Arial', '20'), width=3)
        self.ref.place(relx=0.02, rely=0.84)

        # ----------------------------- INSERÇÃO DE CADASTRO NA BASE DE DADOS ------------------------------------#

        def cadastraheroi():
            heroi = []
            nome_ = pegainfo(self.nome)
            heroi.append(nome_)
            status_ = pegainfo(self.status)
            heroi.append(status_)
            pv_ = pegainfo(self.pv)
            heroi.append(pv_)
            pvmax_ = pegainfo(self.pvmax)
            heroi.append(pvmax_)
            ca_ = pegainfo(self.ca)
            heroi.append(ca_)
            fort_ = pegainfo(self.fort)
            heroi.append(fort_)
            von_ = pegainfo(self.von)
            heroi.append(von_)
            ref_ = pegainfo(self.ref)
            heroi.append(ref_)
            try:
                cur.execute('''
                        INSERT INTO herois (nome,status,ca,pv,pvmax,fort,von,ref)
                        VALUES (?,?,?,?,?,?,?,?)''', heroi)
            except ValueError:
                messagebox.showerror('Aviso!', 'Erro ao inserir dados no banco!')
            con.commit()

            # ---------------------------- MOSTRA ID NA TELA AO SALVAR CADASTRO -------------------------------------#
            def mostraid(x):
                cur.execute("SELECT * FROM herois WHERE nome = '%s'" % x)
                for i in cur.fetchall():
                    return i[0]

            idhe = mostraid(heroi[0])
            messagebox.showinfo('Anote sua id!', '      %s     ' % idhe)
            lista = (self.nome, self.status, self.pv, self.pvmax, self.ca, self.fort, self.von, self.ref)
            for f in lista:
                f.delete(0, END)

        # -------------------------------------BOTAO SALVAR --------------------------------------------------#

        self.botaocadastra = Button(self, text='Salvar', font=('Ariel', '20'), fg='green', command=cadastraheroi)
        self.botaocadastra.place(relx=0.32, rely=0.85, relwidth=0.28)

        def limpaclientes():
            lista = (self.nome, self.status, self.pv, self.pvmax, self.ca, self.fort, self.von, self.ref)
            for f in lista:
                f.delete(0, END)

        # ------------------------------------ BOTAO CANCELAR ---------------------------------------------------#

        self.botaocancela = Button(self, text='Novo/Cancelar', font=('Ariel', '20'), fg='red', command=limpaclientes)
        self.botaocancela.place(relx=0.62, rely=0.85, relwidth=0.28)
        # resolução
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()

        self.geometry("%dx%d+0+0" % (largura_screen, altura_screen))

        self.resizable(0, 0)


class SecondWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        # Configuração da janela principal
        self.title('Segunda Janela')
        self.iconbitmap('imagens\\dnd.ico')
        self.configure(background='darkgray')

        frame2 = Frame(self, bg='sky blue')
        frame2.configure(relief=SOLID)
        frame2.configure(borderwidth="2")
        frame2.place(relx=0.51, rely=0.0, relheight=0.28, relwidth=0.49)

        def verifica_status():
            cur.execute("SELECT pv FROM herois WHERE id = '%s'" % idh.get())
            pv_atual = cur.fetchall()
            pv_novo = 0
            for i in pv_atual:
                pv_novo = "{}".format(i[0])
            pv_novo = int(pv_novo)
            return pv_novo

        def atualiza_status():
            pv_novo = verifica_status()
            if pv_novo >= 1:
                cur.execute("UPDATE herois SET status= 'bom' WHERE id= %s" % idh.get())
            if pv_novo <= 0:
                cur.execute("UPDATE herois SET status='inconsiente' WHERE id= %s" % idh.get())
            if pv_novo <= -10:
                cur.execute("UPDATE herois SET status='morto' WHERE id= %s" % idh.get())
            con.commit()

        # ------------------------------------  FUNCAO CURAR  ---------------------------------------------------#

        def curarherois():
            cur.execute("SELECT nome FROM herois WHERE id = '%s'" % idh.get())
            heroi = cur.fetchall()
            for h in heroi:
                heroi = "{}".format(h[0])
            status = verifica_status()
            if status <= -10:
                messagebox.showwarning("%s" % heroi, "O Personagem esta morto e não pode ser curado!")
            else:
                cur.execute("SELECT pv FROM herois WHERE id = '%s'" % idh.get())
                pv_atual = cur.fetchall()
                pv_novo = 0
                for i in pv_atual:
                    pv_novo = "{}".format(i[0])
                pv_atual = int(pv_novo) + int(campo_cura.get())
                cur.execute('''UPDATE herois SET pv= %s WHERE id = %s ''' % (pv_atual, idh.get()))
                con.commit()
                messagebox.showinfo("%s" % heroi, "Foi curado em: %s pontos de vida!" % (campo_cura.get()))

            campo_cura.delete(0, END)
            mostraheroisid()

        # --------------------------------------- CAMPO CURA ----------------------------------------------------#

        campo_cura = Entry(frame2)
        campo_cura.place(relx=0.08, rely=0.10)
        # --------------------------------------- BOTAO CURA ----------------------------------------------------#

        botaocura = Button(frame2, text='CURAR', font=('Arial', '20', 'bold'), fg='dark orange', command=curarherois)
        botaocura.place(relx=0.08, rely=0.20)

        # ------------------------------------  FUNCAO DANOS  ---------------------------------------------------#

        def danoherois():
            cur.execute("SELECT pv FROM herois WHERE id = '%s'" % idh.get())
            pv_atual = cur.fetchall()
            pv_novo = 0
            for i in pv_atual:
                pv_novo = "{}".format(i[0])
            pv_atual = int(pv_novo) - int(campo_dano.get())
            cur.execute('''UPDATE herois SET pv= %s WHERE id = %s ''' % (pv_atual, idh.get()))
            cur.execute("SELECT nome FROM herois WHERE id = '%s'" % idh.get())
            heroi = cur.fetchall()
            for h in heroi:
                heroi = "{}".format(h[0])
            con.commit()
            messagebox.showinfo("%s" % heroi, "Recebeu %s pontos de dano!" % (campo_dano.get()))
            atualiza_status()
            campo_dano.delete(0, END)
            mostraheroisid()

        # --------------------------------------- CAMPO DANO ----------------------------------------------------#

        campo_dano = Entry(frame2)
        campo_dano.place(relx=0.38, rely=0.10)
        # --------------------------------------- BOTAO DANO ----------------------------------------------------#

        botaodano = Button(frame2, text=' DANO ', font=('Arial', '20', 'bold'), fg='firebrick2', command=danoherois)
        botaodano.place(relx=0.38, rely=0.20)

        # --------------------------- FUNÇÃO MOSTRAR DADOS NA FRAME 3 -------------------------------------------#

        def mostraheroisid():
            mostra1.delete(0.0, END)
            campos = [campo_cura, campo_dano]
            apagacampos(campos)
            id_ = idh.get()
            cur.execute("SELECT * FROM herois WHERE id = '%s'" % id_)
            consulta = cur.fetchall()
            for i in consulta:
                mostra1.insert(END, '''ID:{}
        Nome:{}
        status:{}
        CA:{}
        PV:{}
        PVMAX: {}
        FORT:{}
        VON:{}
        REF:{}'''.format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))

        # --------------------------------------- BOTAO BUSCAR ID ----------------------------------------------#

        botaook2 = Button(frame2, text='Buscar', font=('Ariel', '12'), fg='green', command=mostraheroisid)
        botaook2.place(relx=0.37, rely=0.62)

        # ----------------------------------- ENTRY PESQUISAR POR ID -------------------------------------------#

        Label(frame2, text='PESQUISAR HEROI POR ID:', font=('Ariel', '9', 'bold'), bg='sky blue').place(relx=0.02,
                                                                                                        rely=0.55)
        idh = Entry(frame2, font=('Ariel', '13'))
        idh.place(relx=0.02, rely=0.64)

        # --------------------------------------- BOTAO LIMPAR ID ----------------------------------------------#

        def limpa_idh():
            idh.delete(0, END)
            mostra1.delete(0.0, END)

        botaolimpar = Button(frame2, text='limpar', font=('Ariel', '12'), fg='gray', command=limpa_idh)
        botaolimpar.place(relx=0.52, rely=0.62)

        # ----------------------------------------- FRAME 3 -----------------------------------------------------#
        frame3 = Frame(self)
        frame3.configure(relief=SOLID)
        frame3.configure(borderwidth="2")
        frame3.place(relx=0.0, rely=0.0, relheight=0.58, relwidth=0.49)

        # ------------------------------------- CAIXA DE TEXTO 1 ------------------------------------------------#

        mostra1 = Text(frame3, bg='azure', font=('Courier', '15', 'bold'), fg='blue')
        mostra1.place(relx=0.0, rely=0.0, relheight=0.5, relwidth=1.0)

        lb_nome_ficha = Label(frame3, text="NOME DO ARQUIVO")
        lb_nome_ficha.place(relx=0.015, rely=0.499, relheight=0.05, relwidth=0.19)
        campo_ficha = Entry(frame3, width=10)
        campo_ficha.place(relx=0.015, rely=0.555, relheight=0.05, relwidth=0.19)
        btn3 = Button(frame3, text='Exportar Ficha', command=lambda: generatePDF(campo_ficha.get()))
        btn3.place(relx=0.024, rely=0.61, relheight=0.07, relwidth=0.17)

        def generatePDF(nome_pdf):
            con = sqlite3.connect("Personagens.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            query = "SELECT * FROM herois WHERE id={}".format(pegainfo(idh))
            cur.execute(query)

            result = [dict(row) for row in cur.fetchall()]
            for row in result:
                result = row
            try:
                pdf = canvas.Canvas('{}.pdf'.format(nome_pdf))
                x = 720
                pdf.setTitle(nome_pdf)
                pdf.setFont("Times-Bold", 20)
                pdf.drawString(200, 750, 'Ficha de Personagem')
                pdf.setFont("Helvetica-Bold", 12)
                pdf.drawString(200, 728, 'ID: {}'.format(result.get('id')))
                pdf.drawString(200, 716, 'Nome: {}'.format(result.get('nome')))
                pdf.drawString(200, 704, 'Status: {}'.format(result.get('status')))
                pdf.drawString(200, 692, 'CA: {}'.format(result.get('ca')))
                pdf.drawString(200, 680, 'PV: {}'.format(result.get('pv')))
                pdf.drawString(200, 668, 'PV Maximo: {}'.format(result.get('pvmax')))
                pdf.drawString(200, 656, 'FORT: {}'.format(result.get('fort')))
                pdf.drawString(200, 644, 'VON: {}'.format(result.get('von')))
                pdf.drawString(200, 632, 'REF: {}'.format(result.get('ref')))
                pdf.save()
                messagebox.showinfo("Exportando Ficha",'{}.pdf criado com sucesso!'.format(nome_pdf))
            except:
                messagebox.showerror('Erro ao gerar {}.pdf'.format(nome_pdf))

        # resolução
        largura_screen = self.winfo_screenwidth()
        altura_screen = self.winfo_screenheight()

        self.geometry("%dx%d+0+0" % (largura_screen, altura_screen))

        self.resizable(0, 1)


'''class ThirdWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        # Configuração da janela principal
        self.title('Terceira Janela')
        self.configure(background='yellow')
        self.geometry('480x240')
'''


class MainWindow(Frame):
    def __init__(self):
        Frame.__init__(self, master=None)
        bgImage = PhotoImage(file=r"imagens/DND-FUNDO.png")
        self.lbl = Label(self, image=bgImage).place(relwidth=1, relheight=1)
        # Configuração da janela principal
        self.master.title("DnD Master")
        self.master.iconbitmap('imagens\\dnd.ico')
        largura_screen = self.master.winfo_screenwidth()
        altura_screen = self.master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (largura_screen, altura_screen))
        self.configure(borderwidth=4)
        self.configure(background='white')
        self.master.resizable(False, True)  # tamanho ajustável (True ou False)
        self.button1 = Button(self, text="Cadastrar", command=FirstWindow)
        self.button1.pack(side='left', fill='x', expand=True)
        self.button2 = Button(self, text="Gerenciar", command=SecondWindow)
        self.button2.pack(side='left', fill='x', expand=True)
        # Empacotamos o frame principal
        self.pack(fill='both', expand=True)



def apagacampos(campos):
    for campo in campos:
        campo.delete(0, END)


def pegainfo(campo):
    a = campo.get()
    a = a.lower()
    return a


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.mainloop()
