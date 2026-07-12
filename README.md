# NotalyX — Backend

API REST para o **NotalyX**, sistema de controle de notas acadêmicas. Permite ao usuário criar conta, cadastrar matérias, lançar notas por unidade e acompanhar a meta de aprovação configurável.

🔗 Frontend em produção: [notalyx.vercel.app](https://notalyx.vercel.app/)
🔗 API em produção: [notalyx-backend.onrender.com](https://notalyx-backend.onrender.com)
🔗 Repositório do frontend: [notalyx-frontend](https://github.com/eulskkj/notalyx-frontend)

## Stack

- **Python 3** + **Flask** — API REST
- **MySQL** (Aiven, via `mysql-connector-python`) — persistência de dados
- **Werkzeug** — hash de senha (`generate_password_hash` / `check_password_hash`)
- **Flask-CORS** — comunicação com o frontend
- **Gunicorn** — servidor WSGI de produção
- **Render** — hospedagem da API

## Funcionalidades

- Cadastro e login de usuário, com senha armazenada como hash (nunca em texto puro)
- CRUD de matérias por usuário
- Lançamento de notas por unidade, armazenadas como JSON
- Configuração personalizada: número de unidades, nota máxima e meta de média

## Estrutura da API

| Método | Rota                          | Descrição                          |
|--------|-------------------------------|-------------------------------------|
| POST   | `/api/registrar`              | Cria uma nova conta                 |
| POST   | `/api/login`                  | Autentica o usuário                 |
| GET    | `/api/materias/<username>`    | Lista as matérias do usuário        |
| POST   | `/api/materias`               | Cria uma nova matéria               |
| PUT    | `/api/materias/<id>`          | Atualiza as notas de uma matéria    |
| DELETE | `/api/materias/<id>`          | Remove uma matéria                  |
| GET    | `/api/config/<username>`      | Retorna as configurações do usuário |
| PUT    | `/api/config/<username>`      | Salva as configurações do usuário   |

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/eulskkj/notalyx-backend.git
cd notalyx-backend

# 2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# edite o .env com os dados do seu banco MySQL (host, porta, usuário, senha, nome do banco
# e o caminho do certificado SSL, obrigatório na Aiven)

# 5. Rode o servidor
python app.py
```

O servidor sobe em `http://localhost:5000`.

## Banco de dados

O projeto usa MySQL com as tabelas `usuarios`, `materias` e `configuracoes`. O script de criação está em [`schema.sql`](./schema.sql).

## Deploy

A API está hospedada no **Render** (plano free) e o banco no **Aiven** (plano free, MySQL). Variáveis de ambiente necessárias: `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_SSL_CA`.

## Segurança

- Senhas de usuário são armazenadas com hash (`werkzeug.security`), nunca em texto puro.
- Credenciais do banco ficam em variáveis de ambiente, fora do código-fonte.

## Autor

Desenvolvido por [Luis](https://github.com/eulskkj) — estudante de Desenvolvimento de Sistemas, focado em back-end.
