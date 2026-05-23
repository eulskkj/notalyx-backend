from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import json
import os

app = Flask(__name__)
CORS(app)

# ── CONEXÃO usa variáveis de ambiente do Railway ──────────────
# Localmente continua funcionando com os valores padrão
def get_db_connection():
    return mysql.connector.connect(
        host     = os.environ.get('DB_HOST',     '127.0.0.1'),
        port     = int(os.environ.get('DB_PORT', 3306)),
        user     = os.environ.get('DB_USER',     'root'),
        password = os.environ.get('DB_PASSWORD', 'Pikaflamejante1!'),
        database = os.environ.get('DB_NAME',     'site_notas_db'),
    )


# ── LOGIN ─────────────────────────────────────────────────────
@app.route('/api/login', methods=['POST'])
def login():
    data     = request.get_json()
    username = data.get('username')
    senha    = data.get('senha')
    try:
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT username, nome_exibicao FROM usuarios WHERE username = %s AND senha = %s",
            (username, senha)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return jsonify({"success": True, "user": user}), 200
        else:
            return jsonify({"success": False, "error": "Usuário ou senha incorretos."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── REGISTRAR NOVO USUÁRIO ────────────────────────────────────
@app.route('/api/registrar', methods=['POST'])
def registrar():
    data          = request.get_json()
    username      = data.get('username', '').strip()
    senha         = data.get('senha', '').strip()
    nome_exibicao = data.get('nome_exibicao', '').strip()

    if not username or not senha or not nome_exibicao:
        return jsonify({"error": "Preencha todos os campos."}), 400
    if len(senha) < 4:
        return jsonify({"error": "A senha deve ter pelo menos 4 caracteres."}), 400

    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close(); conn.close()
            return jsonify({"error": "Esse usuário já existe. Escolha outro."}), 409
        cursor.execute(
            "INSERT INTO usuarios (username, senha, nome_exibicao) VALUES (%s, %s, %s)",
            (username, senha, nome_exibicao)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "Conta criada com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── LISTAR MATÉRIAS ───────────────────────────────────────────
@app.route('/api/materias/<username>', methods=['GET'])
def carregar_materias(username):
    try:
        conn   = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nome AS name, unidades_notas AS grades FROM materias WHERE userId = %s ORDER BY createdAt ASC",
            (username,)
        )
        rows = cursor.fetchall()
        for row in rows:
            row['grades'] = json.loads(row['grades'])
        cursor.close()
        conn.close()
        return jsonify(rows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── CRIAR MATÉRIA ─────────────────────────────────────────────
@app.route('/api/materias', methods=['POST'])
def salvar_materia():
    data    = request.get_json()
    nome    = data.get('name')
    grades  = data.get('grades')
    user_id = data.get('userId')
    try:
        conn        = get_db_connection()
        cursor      = conn.cursor()
        grades_json = json.dumps(grades)
        cursor.execute(
            "INSERT INTO materias (nome, unidades_notas, userId) VALUES (%s, %s, %s)",
            (nome, grades_json, user_id)
        )
        conn.commit()
        novo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"id": novo_id, "name": nome, "grades": grades}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── ATUALIZAR NOTAS ───────────────────────────────────────────
@app.route('/api/materias/<int:materia_id>', methods=['PUT'])
def atualizar_materia(materia_id):
    data    = request.get_json()
    grades  = data.get('grades')
    user_id = data.get('userId')
    try:
        conn        = get_db_connection()
        cursor      = conn.cursor()
        grades_json = json.dumps(grades)
        cursor.execute(
            "UPDATE materias SET unidades_notas = %s WHERE id = %s AND userId = %s",
            (grades_json, materia_id, user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close(); conn.close()
            return jsonify({"error": "Matéria não encontrada."}), 404
        cursor.close()
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── DELETAR MATÉRIA ───────────────────────────────────────────
@app.route('/api/materias/<int:materia_id>', methods=['DELETE'])
def deletar_materia(materia_id):
    data    = request.get_json()
    user_id = data.get('userId')
    try:
        conn   = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM materias WHERE id = %s AND userId = %s",
            (materia_id, user_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            cursor.close(); conn.close()
            return jsonify({"error": "Matéria não encontrada."}), 404
        cursor.close()
        conn.close()
        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)