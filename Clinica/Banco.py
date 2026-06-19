
# Importação do Banco de Dados SQLite3
import sqlite3

# Criando conexao com o BD
try:
    con = sqlite3.connect('Cadastro_clinica.db')
    print('Conexao com o banco de dados realizada com sucesso!')
except sqlite3.Error as e:
    print("Error ao conectar com banco de dados:", e)


def adicionar_coluna_consulta():
    try:
        cur = con.cursor()
        # Comando para adicionar a coluna, se ela ainda não existir
        query = "ALTER TABLE pacientes ADD COLUMN consulta TEXT;"
        cur.execute(query)
        con.commit()
        print("✅ Coluna 'consulta' adicionada com sucesso.")
        
    except Exception as e:
        if "duplicate column name" in str(e).lower():
            print("Coluna 'consulta' já existe. Nenhuma alteração necessária.")
        else:
            print(f"Erro inesperado ao alterar a tabela: {e}")

adicionar_coluna_consulta()


# Criando tabela pacientes
try:
    with con:
        cur = con.cursor()                                                                                
        cur.execute(""" CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            email TEXT,
            sexo TEXT,  
            imagem TEXT,      
            cpf TEXT UNIQUE NOT NULL,  
            data_nascimento DATE,
            telefone TEXT,
            nome_consulta TEXT,
            consulta TEXT
        )""")
        print("Tabela pacientes criada com sucesso!")
       
except sqlite3.Error as e:
    print("Error ao criar a tabela pacientes:", e)



# Criando tabela medicos
try:
    with con:
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS medicos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            crm TEXT UNIQUE, 
            especialidade TEXT                      
        )""")

        print("Tabela medicos criada com sucesso!")
       
except sqlite3.Error as e:
    print("Error ao criar a tabela medicos:", e)



# Criando tabela consultas
try:
    with con:
        cur = con.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY,
            nome_consulta TEXT,
            paciente_id INTEGER NOT NULL,
            medico_id TEXT NOT NULL,
            data_atendimento DATE,  
            valor_consulta REAL,
            FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
            FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE CASCADE                         
        )""")




        print("Tabela consultas criada com sucesso!")

except sqlite3.Error as e:
    print("Error ao criar a tabela consultas:", e)
 



  
  # Fechando conexão com o BD

#if con:
    #con.close()
    #print("Conexão com o banco de dados fechada com sucesso.")