# Importação do Banco de Dados SQLite3
import sqlite3

# criando conexao
try:
    con = sqlite3.connect('Cadastro_clinica.db')
    print('Conexao com o banco de dados realizada com sucesso!')
except sqlite3.Error as e:
    print("Error ao conectar com banco de dados:", e)





# CRIANDO CRUD


# Tabela de Medicos -----------------------------------------------------------------------------

# Criar Medicos ( Inserir C )
def criar_medico(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO medicos (nome, crm, especialidade) VALUES (?,?,?)"
        cur.execute(query,i)

# criar_medico(['Pedro Gabriel Magalhães', '7952','Dermatologista',])


# Ver todos os medicos (Selecionar R)
def ver_medicos():
    lista = []
    with con:
        cur = con.cursor()
        cur.execute('SELECT * FROM medicos')
        linha = cur.fetchall()
        for i in linha:
            lista.append(i)
    return lista

# print(ver_medicos())


def ver_medico_id(nome_medico):
    with con:
        cur = con.cursor()
        cur.execute("SELECT id FROM medicos WHERE nome=?", (nome_medico,))
        resultado = cur.fetchall()
        return resultado[0] if resultado else None
        
        

# Atualizar a tabela de Medicos ( Update U )
def atualizar_medico(i):
    with con:
        cur = con.cursor()
        query = "UPDATE medicos SET nome=?, crm=?,especialidade=? WHERE id=?"
        cur.execute(query,i)


# Deletar a tabela Medicos ( Delete D )
def deletar_medico(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM medicos WHERE id=?"
        cur.execute(query,i)

# deletar_medico([1])


# Tabela de Consultas -----------------------------------------------------------------------------

# Criar consultas ( Inserir C )
def criar_consulta(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO consultas (nome_consulta, paciente_id, medico_id, data_atendimento, valor_consulta) VALUES (?,?,?,?,?)"
        cur.execute(query,i)


# Ver todos as consultas (Selecionar R)
def ver_consultas():
    # Retorna o nome do médico em vez do ID para a Treeview
    lista = []
    with con:
        cur = con.cursor()
        # JOIN para mostrar o nome do médico
        cur.execute("""
            SELECT 
                c.id, c.nome_consulta, m.nome, c.data_atendimento, c.valor_consulta, c.paciente_id 
            FROM consultas c
            JOIN medicos m ON c.medico_id = m.id
            ORDER BY c.id
        """)
        linha = cur.fetchall()
        for i in linha:
            lista.append(i)
    return lista

# Atualizar consultas ( Update U )
def atualizar_consulta(i):
    with con:
        cur = con.cursor()
        query = "UPDATE consultas SET nome_consulta=?, paciente_id=?, medico_id=?, data_atendimento=?, valor_consulta=? WHERE id=?"
        cur.execute(query,i)


# Deletar consultas ( Delete D )
def deletar_consulta(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM consultas WHERE id=?"
        cur.execute(query,i)


# Tabela de Pacientes -----------------------------------------------------------------------------

def buscar_paciente_por_nome(nome_busca):
    # O '%' é o curinga do SQL, permitindo buscar por parte do nome
    # Converte o termo de busca para ser case-insensitive
    nome_busca_formatada = '%' + nome_busca + '%' 
    
    query = """
        SELECT * FROM pacientes 
        WHERE nome LIKE ?
    """
    with con: 
        cur = con.cursor()
        cur.execute(query, (nome_busca_formatada,)) 
        
        return cur.fetchall() # Retorna a lista de pacientes encontrado


# Criar Pacientes ( Inserir C )
def criar_pacientes(i):
    with con:
        cur = con.cursor()
        query = "INSERT INTO pacientes (nome, email, sexo, imagem, cpf, data_nascimento, telefone, consulta) VALUES (?,?,?,?,?,?,?,?)"
        cur.execute(query,i)


# Ver todos as pacientes (Selecionar R)
def ver_pacientes():
    lista = []
    with con:
        cur = con.cursor()

        query = """
        SELECT 
            p.id, 
            p.nome, 
            p.email, 
            p.sexo, 
            p.imagem, 
            p.cpf, 
            p.data_nascimento, 
            p.telefone,

            (
                SELECT c.nome_consulta 
                FROM consultas c 
                WHERE c.paciente_id = p.id
                ORDER BY c.data_atendimento DESC 
                LIMIT 1
            ) AS Ultima_Consulta 
            
        FROM pacientes p 
        ORDER BY p.id
        """

        cur.execute(query)
        linha = cur.fetchall()
        for i in linha:
            lista.append(i)
    return lista


# Atualizar pacientes ( Update U )
def atualizar_paciente(i):
    with con:
        cur = con.cursor()
        query = "UPDATE pacientes SET nome=?, email=?, sexo=?, imagem=?, cpf=?, data_nascimento=?, telefone=?, consulta=? WHERE id=?"
        cur.execute(query,i)


# Deletar pacientes ( Delete D )
def deletar_paciente(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM pacientes WHERE id=?"
        cur.execute(query,i)

