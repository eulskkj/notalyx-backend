# NotalyX — Backend

API REST para o **NotalyX**, sistema de controle de notas acadêmicas. Permite ao usuário criar conta, cadastrar matérias, lançar notas por unidade e acompanhar a meta de aprovação configurável.

🔗 Frontend em produção: [notalyx.vercel.app](https://notalyx.vercel.app/)
🔗 API em produção: [notalyx-backend.onrender.com](https://notalyx-backend.onrender.com)
🔗 Repositório do frontend: [notalyx-frontend](https://github.com/eulskkj/notalyx-frontend)

## Stack

- **Python 3** + **Flask**: API REST
- **MySQL** (Aiven, via `mysql-connector-python`): persistência de dados
- **Werkzeug**: hash de senha (`generate_password_hash` / `check_password_hash`)
- **Flask-CORS**: comunicação com o frontend
- **Gunicorn**: servidor WSGI de produção
- **Render**: hospedagem da API

## Funcionalidades

- Cadastro e login de usuário, com senha armazenada como hash (nunca em texto puro)
- CRUD de matérias por usuário
- Lançamento de notas por unidade, armazenadas como JSON
- Configuração personalizada: número de unidades, nota máxima e meta de média
- Rota de saúde (`/api/health`) que testa a conexão com o banco

## Estrutura da API

| Método | Rota                       | Descrição                            |
|--------|----------------------------|--------------------------------------|
| GET    | `/api/health`              | Verifica se a API e o banco respondem |
| POST   | `/api/registrar`           | Cria uma nova conta                  |
| POST   | `/api/login`               | Autentica o usuário                  |
| GET    | `/api/materias/<username>` | Lista as matérias do usuário         |
| POST   | `/api/materias`            | Cria uma nova matéria                |
| PUT    | `/api/materias/<id>`       | Atualiza as notas de uma matéria     |
| DELETE | `/api/materias/<id>`       | Remove uma matéria                   |
| GET    | `/api/config/<username>`   | Retorna as configurações do usuário  |
| PUT    | `/api/config/<username>`   | Salva as configurações do usuário    |

## Como rodar localmente

```bash
# 1. Clone o repositório
git clone https://github.com/eulskkj/notalyx-backend.git
cd notalyx-backend/BACKEND

# 2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Defina as variáveis de ambiente (veja abaixo) apontando para o seu MySQL

# 5. Rode o servidor
python app.py
```

O servidor sobe em `http://localhost:5000`.

### Variáveis de ambiente

| Variável      | Descrição                          | Padrão          |
|---------------|------------------------------------|-----------------|
| `DB_HOST`     | Host do MySQL                      | `127.0.0.1`     |
| `DB_PORT`     | Porta do MySQL                     | `3306`          |
| `DB_USER`     | Usuário do banco                   | `root`          |
| `DB_PASSWORD` | Senha do banco (obrigatória)       | —               |
| `DB_NAME`     | Nome do banco                      | `site_notas_db` |

## Banco de dados

O projeto usa MySQL com as tabelas `usuarios`, `materias` e `configuracoes`. As notas de cada matéria ficam em uma coluna JSON.

## Deploy

- API no **Render** (plano free), com o `Procfile` da pasta `BACKEND`
- Banco no **Aiven** (MySQL, plano free)
- As variáveis de ambiente acima são configuradas no painel do Render

### Mantendo tudo acordado

Nos planos gratuitos, o Render e o banco da Aiven são desligados por inatividade. Para evitar isso, um monitor (UptimeRobot) chama `GET /api/health` a cada 5 minutos. Essa rota faz um `SELECT 1` no banco, então gera atividade nos dois serviços. Se o banco estiver fora do ar, a rota responde 500 com o motivo do erro.

## Segurança

- Senhas de usuário são armazenadas com hash (`werkzeug.security`), nunca em texto puro
- Credenciais do banco ficam em variáveis de ambiente, fora do código-fonte

## Autor

Desenvolvido por [Luis](https://github.com/eulskkj), estudante de Desenvolvimento de Sistemas, focado em back-end.
