import psycopg2
import time
from flask import Flask
from flask_restx import Api, Resource # type: ignore

app = Flask(__name__)
api = Api(app, version='1.0', title='Conecta Postgres API', description='API para conectar ao PostgreSQL', doc='/swagger')

ns = api.namespace('alunos', description='Operações de conexão com o PostgreSQL')

def connect_to_postgres():
    conn = psycopg2.connect(
         host="db",
         dbname="postgres",
         user="postgres",
         password="123456"
    )
    return conn

@ns.route('/')
class AlunosList(Resource): 
    def get(self):
        time.sleep(5)
        conn = connect_to_postgres()
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS alunos (id SERIAL PRIMARY KEY, nome VARCHAR(100), idade INT)")
        conn.commit()
        cursor.execute("INSERT INTO alunos (nome, idade) VALUES (%s, %s)", ('João', 20))
        conn.commit()
        cursor.execute("SELECT * FROM alunos")
        alunos = cursor.fetchall()
        cursor.close()
        conn.close()
        return {'alunos': [{'id': aluno[0], 'nome': aluno[1], 'idade': aluno[2]} for aluno in alunos]}