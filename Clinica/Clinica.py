# Importações:

import site
from tkinter.ttk import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd

# Importando pillow
from PIL import ImageTk, Image

from View import criar_medico, ver_medicos, atualizar_medico, deletar_medico, criar_consulta, ver_consultas, atualizar_consulta, deletar_consulta, buscar_paciente_por_nome, criar_pacientes, ver_pacientes, atualizar_paciente, deletar_paciente, ver_medico_id

# tk calendario
from tkcalendar import Calendar, DateEntry
from datetime import datetime, date


# Cores utilizadas


co0 = "#2e2d2b" # Cor Preta
co1 = "#feffff" # Cor Branca
co2 = "#FEC20C" # Cor amarela
co3 = "#00a095" # Cor Verde
co4 = "#906EB6" # Cor Lilás
co5 = "#003452" # Cor azul forte
co6 = "#FF0095" # Cor rosa
co7 = "#ef5350" # Cor vermelha

co8 = "#033cfc" # Cor Azul
co9 = "#263238" # Cor Verde +
co10 = "#e9edf5" # Cor Cinza




# Criando janela
janela = Tk()
janela.title("")
janela.geometry('945x620')
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)

Style = Style(janela)
Style.theme_use("clam")



# CRIAÇÃO DE FRAMES


# Frame Logo:

frame_logo = Frame(janela, width = 850, height = 52, bg = co1)
frame_logo.grid(row = 0, column = 0, pady =0, padx = 0,  sticky = NSEW)

ttk.Separator(janela, orient = HORIZONTAL).grid(row=1, columnspan=1, ipadx=680)

# Frame Dados:

frame_informações = Frame(janela, width = 850, height = 65, bg = co1)
frame_informações.grid(row = 2, column = 0, pady =0, padx = 0,  sticky = NSEW)

ttk.Separator(janela, orient = HORIZONTAL).grid(row=3, columnspan=1, ipadx=680)

# Frame Detalhes:

frame_detalhes = Frame(janela, width = 850, height = 200, bg = co1)
frame_detalhes.grid(row = 4, column = 0, pady =0, padx = 10,  sticky = NSEW)

# Frame Tabela:

frame_tabela = Frame(janela, width = 850, height = 200, bg = co1)
frame_tabela.grid(row = 5, column = 0, pady =0, padx = 10,  sticky = NSEW)



# Trabalhando com frame Logo ------------------------------------------------------------- 
global logo_photo_img

logo_img_pil = Image.open('Logo.png')
logo_img_pil  = logo_img_pil .resize((50,50))

logo_photo_img = ImageTk.PhotoImage(logo_img_pil)

logo_label = Label(frame_logo, image= logo_photo_img , text="Cadastro de Pacientes", width= 960, compound = LEFT, relief = RAISED, anchor=NW, font=('Ivy 15 bold'), bg=co7, fg=co1)
logo_label.place(x=0, y=0)







# FUNCAO PARA CADASTRAR PACIENTES:

def pacientes():
    
    # Variáveis globais necessárias (apenas caminhos de imagem/objetos Tkinter que precisam persistir no módulo)
    global imagem, imagem_string 
    imagem_string = ''
    
    # =========================================================
    # 1. DEFINIÇÃO DAS FUNÇÕES ANINHADAS (RESOLVENDO O ESCOPO)
    #    Todas as funções chamadas por botões ou binds devem estar definidas aqui.
    # =========================================================
    
    # Função obter o ID da Consulta (mantida como referência)
    def obter_consulta_id(nome_consulta):   
       try:
           # Assumindo que ver_consultas() retorna uma lista de tuplas (id, nome)
           for id_consulta, nome in ver_consultas(): 
                if nome == nome_consulta:
                    return id_consulta
           return None
       except NameError:
           return None
        
    # Tabela de pacientes:
    def mostrar_pacientes():
        app_nome = Label(frame_tabela, text="Tabela de Pacientes", height=1, pady=0, padx=0, relief='flat', anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co5)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        list_header = ['Id', 'Nome','Email', 'Sexo', 'Imagem', 'CPF', 'DATA', 'Telefone', 'Consulta']
        df_list = ver_pacientes() # Sua função que retorna todos os pacientes

        global tree_paciente
        # O widget tree_paciente é criado aqui
        tree_paciente = ttk.Treeview(frame_tabela, selectmode="extended", columns=list_header, show="headings")
        
        # vertical scrollbar e horizontal scrollbar
        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree_paciente.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=tree_paciente.xview)

        tree_paciente.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_paciente.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
        frame_tabela.grid_rowconfigure(0, weight=12)

        hd = ["nw", "nw", "nw", "center", "center", "center", "center","center", 'nw']
        h = [40,120,120,110,105,110,105,100,100]
        n = 0

        for col in list_header:
            tree_paciente.heading(col, text=col.title(), anchor=NW)
            tree_paciente.column(col, width=h[n], anchor=hd[n])
            n+=1

        for item in df_list:
            tree_paciente.insert('', 'end', values=item)

        # Re-atribui o bind após a criação da treeview
        tree_paciente.bind('<<TreeviewSelect>>', preencher_campos)


    # FUNCAO NOVO PACIENTE (SALVAR):
    def novo_paciente():
        global imagem, imagem_string
        
        # Não redefina l_imagem aqui. Ela já foi criada no corpo principal.

        nome = e_nome_paciente.get()
        email = e_email.get()
        telefone = e_tel.get()
        sexo = c_sexo.get()
        data = data_nascimento.get_date()  
        cpf = e_cpf.get()
        imagem = imagem_string

        nome_consulta_selecionada = c_consulta.get()

        lista = [nome, email, sexo, imagem, cpf, data, telefone, nome_consulta_selecionada]

        # verificando caso alguum campo esteja vazio:
        for i in lista:
            if i=='' or i == ' ':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
            
        # Inserindo os dados no banco de dados
        criar_pacientes(lista)

        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso!')

        # Limpando os campos de entrada:
        e_nome_paciente.delete(0, END)
        e_email.delete(0, END)
        e_tel.delete(0, END)
        c_sexo.set('') # CORRIGIDO: Usa .set('') para Combobox
        data_nascimento.set_date(datetime.today().date())
        e_cpf.delete(0,END)
        c_consulta.set('') # CORRIGIDO: Usa .set('') para Combobox
        
        # mostrando os valores da tabela:
        mostrar_pacientes()


    # FUNCAO UPDATE PACIENTE:
    def update_paciente():
        global imagem_string 

        try:
            tree_itens = tree_paciente.focus()
            tree_dicionario = tree_paciente.item(tree_itens)
            tree_lista = tree_dicionario['values']
            valor_id = tree_lista[0] 
        except IndexError:
            messagebox.showerror('Erro', 'Selecione um paciente na tabela para atualizar.')
            return

        nome = e_nome_paciente.get()
        email = e_email.get()
        telefone = e_tel.get()
        sexo = c_sexo.get()
        data = data_nascimento.get_date()  
        cpf = e_cpf.get() 
        consulta_selecionada = c_consulta.get()
        
        imagem = imagem_string if imagem_string else tree_lista[4]
        
        # [Nome, Email, Sexo, Imagem, CPF, Data, Telefone, Consulta, ID]
        lista_update = [nome, email, sexo, imagem, cpf, data, telefone, consulta_selecionada, valor_id]

        for i in lista_update[:-1]: 
            if i == '' or i == ' ':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

        atualizar_paciente(lista_update)

        messagebox.showinfo('Sucesso', 'Os dados foram atualizados com sucesso!')
        
        # Limpando os campos
        e_nome_paciente.delete(0, END)
        e_email.delete(0, END)
        e_tel.delete(0, END)
        c_sexo.set('') # CORRIGIDO
        data_nascimento.set_date(datetime.today().date()) 
        e_cpf.delete(0,END)
        c_consulta.set('') # CORRIGIDO

        # Retorna o botão Salvar ao seu estado original
        botao_salvar.config(command=novo_paciente, text="Salvar".upper())
        
        mostrar_pacientes()


    # FUNCAO DELETE PACIENTE:
    def delete_paciente():
        try:
            tree_itens = tree_paciente.focus()
            tree_dicionario = tree_paciente.item(tree_itens)
            tree_lista = tree_dicionario['values']
            
            valor_id = tree_lista[0] 
            
            deletar_paciente([valor_id]) 
            
            # Limpa os campos
            e_nome_paciente.delete(0, END)
            e_email.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.set('')
            data_nascimento.set_date(datetime.today().date())
            e_cpf.delete(0,END)
            c_consulta.set('')
            
            mostrar_pacientes()
            
            messagebox.showinfo('Sucesso', 'Paciente excluído com sucesso!')

        except IndexError:
            messagebox.showerror('Erro', 'Selecione um paciente na tabela para excluir.')
            return


    # FUNCAO PARA PREENCHER OS CAMPOS (Chamada pelo click na Treeview)
    def preencher_campos(event):
        global imagem_string
        
        try:
            tree_itens = tree_paciente.focus()
            tree_dicionario = tree_paciente.item(tree_itens)
            tree_lista = tree_dicionario['values']

            # Limpando os campos de entrada:
            e_nome_paciente.delete(0, END)
            e_email.delete(0, END)
            e_tel.delete(0, END)
            c_sexo.set('')
            e_cpf.delete(0,END)
            c_consulta.set('')

            # Inserindo os valores nos campos de entradas
            e_nome_paciente.insert(0, tree_lista[1])
            e_email.insert(0, tree_lista[2])
            e_tel.insert(0, tree_lista[7])
            c_sexo.set(tree_lista[3])
            e_cpf.insert(0, tree_lista[5])
            
            # Formatação da data:
            data_str = tree_lista[6] 
            if data_str:
                data_obj = datetime.strptime(data_str, '%Y-%m-%d').date() 
                data_nascimento.set_date(data_obj)

            # Insere o nome da Consulta
            c_consulta.set(tree_lista[8]) 

            # CARREGANDO A IMAGEM NA LABEL
            caminho_imagem = tree_lista[4]
            imagem_string = caminho_imagem # Define a global para que update_paciente a utilize
            if caminho_imagem:
                try:
                    imagem_carregada = Image.open(caminho_imagem)
                    imagem_carregada = imagem_carregada.resize((130,130))
                    imagem_tk = ImageTk.PhotoImage(imagem_carregada)

                    l_imagem.config(image=imagem_tk)
                    l_imagem.image = imagem_tk # Mantém a referência

                except FileNotFoundError:
                    l_imagem.config(image='')
                    l_imagem.image = None
                    messagebox.showwarning('Atenção', 'Arquivo de imagem não encontrado no caminho original.')
            
            # Reconfigura o botão SALVAR para chamar a função de ATUALIZAR
            botao_salvar.config(command=update_paciente, text="Salvar".upper())
            
        except IndexError:
            pass # Ignora se não houver item selecionado


    # FUNCAO PARA ESCOLHER IMAGEM: (ESTRUTURA CORRIGIDA)
    def escolher_imagem():
        global imagem, imagem_string # l_imagem é acessada via closure

        # Selecione o arquivo:
        caminho_arquivo = fd.askopenfilename(
            title ="Selecione a imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.gif")]
        )

        # Se o usuario cancelar a aplicação, Não continua
        if not caminho_arquivo:
            return

        imagem_string = caminho_arquivo # Salva o caminho para o banco de dados

        # Abrindo, redimensionando e atualizando o Label
        try:
            imagem_pil = Image.open(caminho_arquivo)
            imagem_pil = imagem_pil.resize((130,130))
            imagem_tk = ImageTk.PhotoImage(imagem_pil) 
            
            # O widget l_imagem é acessado do escopo pai (closure)
            l_imagem.config(image=imagem_tk)
            l_imagem.image = imagem_tk # CRÍTICO: Mantém a referência
            
            global imagem
            imagem = imagem_tk 

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir a imagem: {e}")
            return
        
        botao_carregar['text'] = 'Trocar de Foto'
    
    # FUNCAO PROCURAR PACIENTE:
    def procurar_paciente():
        # Pega o texto do campo de procurar (e_nome_procurar)
        nome_busca = e_nome_procurar.get()
        
        if not nome_busca:
            messagebox.showwarning('Aviso', 'Digite o nome ou parte do nome para buscar.')
            return

        # Chama a função de busca que está no View.py
        resultados = buscar_paciente_por_nome(nome_busca) 
        
        # 1. Limpa a Treeview
        for item in tree_paciente.get_children():
            tree_paciente.delete(item)
        
        # 2. Insere os novos resultados
        if resultados:
            for item in resultados:
                tree_paciente.insert('', 'end', values=item)

            messagebox.showinfo('Busca', f'{len(resultados)} paciente(s) encontrado(s).')
        else:
            messagebox.showinfo('Busca', f'Nenhum paciente encontrado com o nome "{nome_busca}".')
            # Se não houver resultados, recarrega a tabela completa
            mostrar_pacientes() # Chama a função que você já tem para recarregar a tabela






    # =========================================================
    # 2. CRIAÇÃO DOS WIDGETS E BOTÕES
    # =========================================================

    # Criando campos de entrada
    l_nome = Label(frame_detalhes, text="Nome *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_nome.place(x=10, y=10)
    e_nome_paciente = Entry(frame_detalhes, width=45, justify='left', relief='solid')
    e_nome_paciente.place(x=12, y=40)

    l_email = Label(frame_detalhes, text="Email *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_email.place(x=10, y=70)
    e_email = Entry(frame_detalhes, width=45, justify='left', relief='solid')
    e_email.place(x=12, y=100)

    l_tel= Label(frame_detalhes, text="Telefone *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_tel.place(x=10, y=130)
    e_tel = Entry(frame_detalhes, width=20, justify='left', relief='solid')
    e_tel.place(x=12, y=160)


    # SELECIONANDO O SEXO
    l_sexo= Label(frame_detalhes, text="Sexo *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_sexo.place(x=190, y=130)
    c_sexo = ttk.Combobox(frame_detalhes, width=12, font=('Ivy 8 bold'),)
    c_sexo['values'] = ('Masculino', 'Feminino')
    c_sexo.place(x=190, y=160)


    l_nascimento= Label(frame_detalhes, text="Data de Nascimento *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_nascimento.place(x=446, y=10)
    data_nascimento = DateEntry(frame_detalhes, width=18, background='darkblue', foreground='white', bordewith=2, year=2025)
    data_nascimento.place(x=450, y=40)


    l_cpf= Label(frame_detalhes, text="CPF *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_cpf.place(x=446, y=70)
    e_cpf = Entry(frame_detalhes, width=20, justify='left', relief='solid')
    e_cpf.place(x=450, y=100)


    # PEGANDO AS CONSULTAS:
    consultas_bd = ver_consultas()
    consulta_nomes = []

    for i in consultas_bd:
        consulta_nomes.append(i[1])

    l_consulta = Label(frame_detalhes, text="Consulta *", height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co0)
    l_consulta.place(x=446, y=130)
    c_consulta = ttk.Combobox(frame_detalhes, width=20, font=('Ivy 8 bold'),)
    c_consulta['values'] = (consulta_nomes)
    c_consulta.place(x=450, y=160)


    # Inicialização do Label da Imagem (CORRIGIDO: Sem 'image=imagem' inicial)
    l_imagem = Label(frame_detalhes, bg=co1, fg=co4)
    l_imagem.place(x=300, y=10)


    # BOTAO CARREGAR FOTO
    botao_carregar = Button(frame_detalhes, command = escolher_imagem, text="Carregar Foto".upper(), width= 20, compound = CENTER, anchor= CENTER, overrelief=RIDGE, font=('Ivy 8'), bg=co1, fg=co0)
    botao_carregar.place(x=300, y=160)

    # linha separatoria 
    l_linha = Label(frame_detalhes, relief=GROOVE, text='h', width=1, height=100, anchor=NW, font=('Ivy 1'), bg=co0, fg=co0)
    l_linha.place(x=610, y=10)
    l_linha = Label(frame_detalhes, relief=GROOVE, text='h', width=1, height=100, anchor=NW, font=('Ivy 1'), bg=co1, fg=co0)
    l_linha.place(x=608, y=10)

    # Procurar paciente
    l_nome = Label(frame_detalhes, text="Procurar paciente [Entra o nome]", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0)
    l_nome.place(x=627, y=10)
    e_nome_procurar = Entry(frame_detalhes, width=20, justify='center', relief='solid', font=('Ivy 10'))
    e_nome_procurar.place(x=630, y=35)

    botao_procurar = Button(frame_detalhes, command=procurar_paciente, anchor=CENTER, text="Procurar", width=12 , overrelief=RIDGE, font=('Ivy 7 bold'), bg=co1, fg=co0)
    botao_procurar.place(x=777, y=35)

    
   # Botões CRUD -------------------------------------------------------------------------------

    botao_salvar = Button(frame_detalhes, command= novo_paciente, anchor=CENTER, text="Salvar".upper(), width=9 , overrelief=RIDGE, font=('Ivy 7 bold'), bg=co3, fg=co0)
    botao_salvar.place(x=627, y=110)

    botao_atualizar = Button(frame_detalhes, command= update_paciente,anchor=CENTER, text='Atualizar'.upper(), width=9, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co5, fg=co1)
    botao_atualizar.place(x=627, y=135)

    botao_deletar = Button(frame_detalhes,command= delete_paciente ,anchor=CENTER, text='Deletar'.upper(), width=9, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co7, fg=co1)
    botao_deletar.place(x=627, y=160)

    botao_ver = Button(frame_detalhes, command= mostrar_pacientes, anchor=CENTER, text='Ver'.upper(), width=9, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co2, fg=co1)
    botao_ver.place(x=727, y=160)

    # =========================================================
    # 3. EXECUÇÃO INICIAL
    # =========================================================
    # Executa a função mostrar_pacientes para carregar a tabela ao iniciar.
    # O bind para preencher os campos já está dentro de mostrar_pacientes().
    mostrar_pacientes()





#  Função para adicionar médicos e consultas:
def adicionar():
    # Criando frames para tabelas ----------

    frame_tabela_medico = Frame(frame_tabela, width=300, height=200, bg=co1)
    frame_tabela_medico.grid(row=0, column=0, pady=0, padx=10, sticky=NSEW)

    frame_tabela_linha = Frame(frame_tabela, width=30, height=200, bg=co1)
    frame_tabela_linha.grid(row=0, column=1, pady=0, padx=10, sticky=NSEW)

    frame_tabela_consulta =  Frame(frame_tabela, width=300, height=200, bg=co1)
    frame_tabela_consulta.grid(row=0, column=2, pady=0, padx=10, sticky=NSEW)



    # DETALHES DO MEDICO -------------------------------------------------------------------------------------------------------

    # FUNCAO NOVO MEDICO:
    def novo_medico():
        nome = e_nome_medico.get()
        especialidade = e_especialidade.get()
        crm = e_crm.get()

        lista = [nome, especialidade, crm]

        # Verificando se tem valores vazios ou não:
        for i in lista:
            if i=="":
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return
            
        # Inserindo os dados
        criar_medico(lista)

        # mostrando mesagem de sucesso
        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

        e_nome_medico.delete(0,END)
        e_especialidade.delete(0,END)
        e_crm.delete(0,END)

        # mostrando os valores na tabela
        mostrar_medicos()



    # FUNCAO ATUALIZAR MEDICO:
    def update_medico():
            try:
                tree_itens = tree_medico.focus()
                tree_dicionario = tree_medico.item(tree_itens)
                tree_lista = tree_dicionario['values']

                valor_id = tree_lista[0]

                # Inserindo valore nas Entries:
                e_nome_medico.insert(0, tree_lista[1])
                e_especialidade.insert(0, tree_lista[2])
                e_crm.insert(0, tree_lista[3])

                # FUNCAO ATUALIZAR:
                def update():
                    
                    nome = e_nome_medico.get()
                    especialidade = e_especialidade.get()
                    crm = e_crm.get()

                    lista = [nome, especialidade, crm, valor_id]

                    # Verificando se tem valores vazios ou não:
                    for i in lista:
                        if i=="":
                            messagebox.showerror('Erro', 'Preencha todos os campos')
                            return
                            
                    # Inserindo os dados
                    atualizar_medico(lista)

                    # mostrando mesagem de sucesso
                    messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

                    e_nome_medico.delete(0,END)
                    e_especialidade.delete(0,END)
                    e_crm.delete(0,END)

                    # mostrando os valores na tabela
                    mostrar_medicos()        

                    # destruindo o botao salvar depois de salvar os dados:
                    botao_salvar.destroy()
                            
                botao_salvar = Button(frame_detalhes, command=update, anchor=CENTER, text='Salvar atualizacação'.upper(), overrelief=RIDGE, font=('Ivy 7 bold'), bg=co5, fg=co1)
                botao_salvar.place(x=227, y=130)

            except IndexError:
                messagebox.showerror('Error', 'Selecione um dos médicos na tabela')

        
    # FUNCAO DELETAR MEDICO:
    def delete_medico():
            try:
                tree_itens = tree_medico.focus()
                tree_dicionario = tree_medico.item(tree_itens)
                tree_lista = tree_dicionario['values']

                valor_id = tree_lista[0]

                # deletar os dados do BD:
                deletar_medico([valor_id])

                # mostrando mesagem de sucesso
                messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')
                
                # mostrando os valores na tabela
                mostrar_medicos() 

            except IndexError:
                messagebox.showerror('Error', 'Selecione um dos médicos na tabela')



    l_nome = Label(frame_detalhes, text="Nome do medico *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0 )
    l_nome.place(x=10, y=10)
    e_nome_medico = Entry(frame_detalhes, width=35, justify='left', relief='solid')
    e_nome_medico.place(x=12, y=40)

    l_especialidade = Label(frame_detalhes, text="Especialidade *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0 )
    l_especialidade.place(x=10, y=70)
    e_especialidade = Entry(frame_detalhes, width=20, justify='left', relief='solid')
    e_especialidade.place(x=12, y=100)

    l_crm = Label(frame_detalhes, text="Crm *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0 )
    l_crm.place(x=10, y=130)
    e_crm = Entry(frame_detalhes, width=10, justify='left', relief='solid')
    e_crm.place(x=12, y=160)

    # Botões:

    botao_carregar = Button(frame_detalhes, command=novo_medico, anchor=CENTER, text='Novo'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co3, fg=co1)
    botao_carregar.place(x=107, y=160)

    botao_atualizar = Button(frame_detalhes, command=update_medico, anchor=CENTER, text='Atualizar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co5, fg=co1)
    botao_atualizar.place(x=187, y=160)

    botao_deletar = Button(frame_detalhes, command=delete_medico, anchor=CENTER, text='Deletar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co7, fg=co1)
    botao_deletar.place(x=267, y=160)





    # Tabela de Médicos:

    def mostrar_medicos():
        app_nome = Label(frame_tabela_medico, text="Tabela de Médicos", height=1, pady=0, padx=0, relief='flat', anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co5)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        # Criando uma TreeView com duas barras de rolagem

        list_header = ['Id', 'Medico', 'Especialidade', 'Crm']

        df_list = ver_medicos()

        global tree_medico

        tree_medico = ttk.Treeview(frame_tabela_medico, selectmode="extended", columns=list_header, show="headings")
        
        # vertical scrollbar
        vsb = ttk.Scrollbar(frame_tabela_medico, orient="vertical", command=tree_medico.yview)

        # horizontal scrollbar
        hsb = ttk.Scrollbar(frame_tabela_medico, orient="horizontal", command=tree_medico.xview)

        tree_medico.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree_medico.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
        frame_tabela_medico.grid_rowconfigure(0, weight=12)

        hd = ["nw", "nw", "e", "e"]
        h = [30,150,80,60]
        n = 0

        for col in list_header:
            tree_medico.heading(col, text=col.title(), anchor=NW)
            # 
            tree_medico.column(col, width=h[n], anchor=hd[n])
            n+=1


        for item in df_list:
            tree_medico.insert('', 'end', values=item)

    mostrar_medicos()



    # linha separatoria ----------------------------------------------------------------------
  
    l_linha = Label(frame_detalhes, relief=GROOVE, text='h', width=1, height=100, anchor=NW, font=('Ivy 1'), bg=co0, fg=co0)
    l_linha.place(x=374, y=10)
    l_linha = Label(frame_detalhes, relief=GROOVE, text='h', width=1, height=100, anchor=NW, font=('Ivy 1'), bg=co1, fg=co0)
    l_linha.place(x=372, y=10)

    # linha separatoria tabela --------------------------------------------------------------

    l_linha = Label(frame_tabela_linha, relief=GROOVE, text='h', width=1, height=140, anchor=NW, font=('Ivy 1'), bg=co0, fg=co0)
    l_linha.place(x=6, y=10)
    l_linha = Label(frame_tabela_linha, relief=GROOVE, text='h', width=1, height=140, anchor=NW, font=('Ivy 1'), bg=co1, fg=co0)
    l_linha.place(x=4, y=10)




    # DETALHES DA CONSULTA------------------------------------------------  --------------------------------------------------------

     # FUNCAO NOVA CONSULTA:

    def nova_consulta():
        nome_consulta = e_nome_consulta.get().strip()
        medico_nome = m_medico.get().strip()
        data = data_atendimento.get_date()
        data_formatada = data.strftime('%Y-%m-%d')
        valor_str = valor_consulta.get().strip()

        
        resultado_medico = ver_medico_id(medico_nome) 
        if resultado_medico is None:
            messagebox.showerror("Erro", "Médico não encontrado.")
            return     
        # Se retornar tupla, como (3,)
        medico_id = resultado_medico[0] 

        # ----- PACIENTE -----
        resultado_paciente = 1
        if resultado_paciente is None:
            messagebox.showerror("Erro", "Paciente não encontrado.")
            return

        paciente_id = resultado_paciente

        # Validação de campos obrigatórios
        if not nome_consulta or not medico_id or not valor_str:
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

        # Validação do valor
        try:
            valor_limpo = valor_str.replace("R$", "").replace(",", ".").strip()
            valor_num = float(valor_limpo)
            if valor_num < 0:
                messagebox.showerror('Erro', 'O valor da consulta não pode ser negativo.')
                return
        except ValueError:
            messagebox.showerror('Erro', 'O valor da consulta deve ser um número válido')
            return

        # Inserir dados no banco
        lista = [nome_consulta, paciente_id, medico_id, data_formatada, valor_num]
        criar_consulta(lista)

        # Mensagem de sucesso
        messagebox.showinfo('Sucesso', 'Os dados foram inseridos com sucesso')

        # Limpar campos
        e_nome_consulta.delete(0, 'end')
        m_medico.set('')
        data_atendimento.set_date(date.today())
        valor_consulta.delete(0, 'end')

        # Atualizar tabela
        mostrar_consultas()


    # FUNCAO ATUALIZAR CONSULTA:
    
    def update_consulta():
        try:
            item_selecionado = tree_consulta.focus()
            print(f"Item selecionado: {item_selecionado}")
            if not item_selecionado:
                raise IndexError

            dados_item = tree_consulta.item(item_selecionado)['values']
            valor_id = dados_item[0]
            paciente_id_original = dados_item[5]

            # Preencher campos
            e_nome_consulta.delete(0, 'end')
            e_nome_consulta.insert(0, dados_item[1])

            m_medico.set(dados_item[2])

            try:
                data_str = dados_item[3]
                data_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
                data_atendimento.set_date(data_obj)
            except ValueError:
                messagebox.showerror('Erro de Dados', 
                f"O formato da data '{dados_item[3]}' no registro selecionado está inválido (esperado: YYYY-MM-DD).")

                return

            valor_consulta.delete(0, 'end')
            valor_consulta.insert(0, dados_item[4])

            # Função interna para salvar atualização
            def salvar_atualizacao():
                nome = e_nome_consulta.get().strip()
                medico_nome = m_medico.get().strip()
                data = data_atendimento.get_date()
                data_formatada = data.strftime('%Y-%m-%d')
                valor_str = valor_consulta.get().strip()

                # Obter ID do médico
                resultado_medico = ver_medico_id(medico_nome)

                if resultado_medico is None:
                    messagebox.showerror("Erro", "Médico não encontrado.")
                    return

                medico_id = resultado_medico[0]

                # Validação do valor
                try:
                    valor_limpo = valor_str.replace("R$", "").replace(",", ".").strip()
                    valor_num = float(valor_limpo)
                    if valor_num < 0:
                        messagebox.showerror('Erro', 'O valor da consulta não pode ser negativo.')
                        return
                except ValueError:
                    messagebox.showerror('Erro', 'O valor da consulta deve ser um número válido')
                    return

                # Atualizar dados
                lista = [nome, paciente_id_original, medico_id, data_formatada, valor_num, valor_id]
                atualizar_consulta(lista)

                messagebox.showinfo('Sucesso', 'Os dados foram atualizados com sucesso')

                # Limpar campos
                e_nome_consulta.delete(0, 'end')
                m_medico.set('')
                data_atendimento.set_date(date.today())
                valor_consulta.delete(0, 'end')

                # Atualizar tabela
                mostrar_consultas()

                # Destruir botão de salvar atualização
                botao_salvar.destroy()

            # Criar botão para salvar atualização
            global botao_salvar
            botao_salvar = Button(frame_detalhes, text='Salvar Atualização'.upper(),
                                command=salvar_atualizacao, anchor='center',
                                overrelief='ridge', font=('Ivy 7 bold'),
                                bg=co5, fg=co1, width = 20)
            botao_salvar.place(x=420, y=130)

        except IndexError:
            messagebox.showerror('Erro', 'Selecione uma consulta na tabela')


    # FUNCAO DELETAR Consulta:
    def delete_consulta():
            try:
                tree_itens = tree_consulta.focus()
                tree_dicionario = tree_consulta.item(tree_itens)
                tree_lista = tree_dicionario['values']

                valor_id = tree_lista[0]

                # deletar os dados do BD:
                deletar_consulta([valor_id])

                # mostrando mesagem de sucesso
                messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso')
                
                # mostrando os valores na tabela
                mostrar_consultas() 

            except IndexError:
                messagebox.showerror('Error', 'Selecione uma consulta na tabela')



    l_nome = Label(frame_detalhes, text="Nome da Consulta *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0)
    l_nome.place(x=420, y=10)
    e_nome_consulta = Entry(frame_detalhes, width=35, justify='left', relief="solid")
    e_nome_consulta.place(x=420, y=40)

    l_consulta = Label(frame_detalhes, text="Medico *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0)
    l_consulta.place(x=420, y=70)




    # SELECIONANDO OS MEDICOS:

    medicos = ver_medicos()
    medico = []

    for i in medicos:
        medico.append(i[1])


    m_medico = ttk.Combobox(frame_detalhes, width=20, font=('Ivy 8 bold'),)
    m_medico['values'] = (medico)
    m_medico.place(x=420, y=100)


    l_valor = Label(frame_detalhes, text="Valor da Consulta *",  height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0)
    l_valor.place(x=687, y=70)
    valor_consulta = Entry(frame_detalhes, width=15, justify='left', relief='solid')
    valor_consulta.place(x=690, y=100)
    


    l_data_atendimento = Label(frame_detalhes, text="Datas de Atendimento *", height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co0)
    l_data_atendimento.place(x=418, y=130)
    data_atendimento = DateEntry(frame_detalhes, width=10, background='darkblue', foreground='white', borderwidth=2, year=2025)
    data_atendimento.place(x=420, y=160)



    botao_carregar = Button(frame_detalhes, command= nova_consulta, anchor=CENTER, text='Salvar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co3, fg=co1)
    botao_carregar.place(x=537, y=160)

    botao_atualizar = Button(frame_detalhes, command= update_consulta, anchor=CENTER,  text='Atualizar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co5, fg=co1)
    botao_atualizar.place(x=617, y=160)

    botao_deletar = Button(frame_detalhes, command=delete_consulta ,anchor=CENTER, text='Deletar'.upper(), width=10, overrelief=RIDGE, font=('Ivy 7 bold'), bg=co7, fg=co1)
    botao_deletar.place(x=697, y=160)


    # Tabela de Consultas:

    def mostrar_consultas():
        app_nome = Label(frame_tabela_consulta, text="Tabela de Consultas", height=1, pady=0, padx=0, relief='flat', anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co5)
        app_nome.grid(row=0, column=0, padx=0, pady=10, sticky=NSEW)

        # Criando uma TreeView com duas barras de rolagem

        list_header = ['Id', 'Nome da Consulta', 'Medico', 'Data', 'Valor']

        df_list = ver_consultas()

        global tree_consulta
        tree_consulta = ttk.Treeview(
        frame_tabela_consulta, 
        selectmode="extended", 
        columns=list_header, 
        show="headings")
        
        # vertical scrollbar
        vsb = ttk.Scrollbar(frame_tabela_consulta, orient="vertical", command=tree_consulta.yview)

        # horizontal scrollbar
        hsb = ttk.Scrollbar(frame_tabela_consulta, orient="horizontal", command=tree_consulta.xview)

        tree_consulta.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)


        tree_consulta.grid(column=0, row=1, sticky='nsew')
        vsb.grid(column=1, row=1, sticky='ns')
        hsb.grid(column=0, row=2, sticky='ew')
        frame_tabela_consulta.grid_rowconfigure(0, weight=12)


        hd = ["nw", "nw", "nw", "center", "e"]
        h = [110,80,130,120,30]
        n = 0

        for col in list_header:
            tree_consulta.heading(col, text=col.title(), anchor=NW)
            tree_consulta.column(col, width=h[n], anchor=hd[n])
            n+=1


        for item in df_list:
            tree_consulta.insert('', 'end', values=item)

    mostrar_consultas()




# Função para salvar:
def salvar():
    print('Salvar')



# FUNCAO CONTROLE -----------------------------------------------------------------------

def control(i):
   # cadastro paciente  
    if i == 'cadastro':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()


        # Chamando a funcao paciente:
        pacientes()


    if i == 'adicionar':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()


        # Chamando a funcao adicionar:
        adicionar()


    if i == 'salvar':
        for widget in frame_detalhes.winfo_children():
            widget.destroy()

        for widget in frame_tabela.winfo_children():
            widget.destroy()


        # Chamando a funcao salvar:
        salvar()





# CRIANDO BOTOES PARA INTERFACE:

app_img_cadastro = Image.open('add.png')
app_img_cadastro = app_img_cadastro.resize((18,18))
app_img_cadastro = ImageTk.PhotoImage(app_img_cadastro)
app_cadastro = Button(frame_informações, command = lambda:control('cadastro'), image=app_img_cadastro, text="Cadastro", width= 100, compound = LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_cadastro.place(x=10, y=30)


app_img_adicionar = Image.open('add.png')
app_img_adicionar = app_img_adicionar.resize((18,18))
app_img_adicionar= ImageTk.PhotoImage(app_img_adicionar)
app_adicionar = Button(frame_informações, command = lambda:control('adicionar'), image=app_img_adicionar, text="Adicionar", width= 100, compound = LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_adicionar.place(x=123, y=30)


app_img_salvar = Image.open('Salvar.png')
app_img_salvar = app_img_salvar.resize((18,18))
app_img_salvar= ImageTk.PhotoImage(app_img_salvar)
app_salvar = Button(frame_informações, command = lambda:control('salvar'), image=app_img_salvar, text="Salvar", width= 100, compound = LEFT, overrelief=RIDGE, font=('Ivy 11'), bg=co1, fg=co0)
app_salvar.place(x=236, y=30)



 
# Executando janela

pacientes()


janela.mainloop()
