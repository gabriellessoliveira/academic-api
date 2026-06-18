# ⭐ Academic API

Este projeto consiste em uma API REST para gerenciamento acadêmico. A ideia foi criar um sistema capaz de organizar alunos, professores, disciplinas, turmas, matrículas e notas, aplicando conceitos de desenvolvimento de APIs, banco de dados e organização de código em camadas.

Durante o desenvolvimento, utilizei o SQLite para realizar os primeiros testes de forma local. Depois, configurei o projeto com Docker e PostgreSQL para que a API e o banco de dados possam ser iniciados juntos.

## 📌 Funcionalidades

A API possui as seguintes funcionalidades:

* cadastro, consulta, atualização e exclusão de alunos;
* cadastro, consulta, atualização e exclusão de disciplinas;
* cadastro, consulta, atualização e exclusão de turmas;
* criação e cancelamento de matrículas;
* lançamento e correção de notas;
* consulta das notas de uma matrícula;
* geração do boletim do aluno;
* cálculo da média por disciplina;
* verificação do funcionamento da API e da conexão com o banco.

Os professores são cadastrados inicialmente pelo arquivo de seed e utilizados como responsáveis pelas disciplinas.

## ✅ Regras implementadas

Além das operações básicas, algumas validações foram adicionadas ao sistema:

* não é permitido cadastrar alunos com e-mail ou número de matrícula repetidos;
* uma disciplina não pode ser cadastrada com um código já existente;
* toda disciplina precisa estar ligada a um professor existente;
* uma turma deve estar relacionada a uma disciplina cadastrada;
* um aluno não pode se matricular duas vezes na mesma turma;
* a matrícula só é criada quando ainda existem vagas;
* não é possível lançar notas em uma matrícula cancelada;
* as notas devem ter valor entre 0 e 10;
* não é permitido cadastrar duas notas do mesmo tipo para a mesma matrícula.

## 🛠️ Tecnologias utilizadas

* Python;
* FastAPI;
* SQLAlchemy;
* Pydantic;
* SQLite;
* PostgreSQL;
* Docker;
* Docker Compose;
* Swagger.

O SQLite é utilizado durante a execução local. Quando o projeto é iniciado com Docker, o banco utilizado é o PostgreSQL.

## 📂 Organização do projeto

O código foi separado em camadas para facilitar a organização e a manutenção:

* `domain/models`: contém as entidades e tabelas do banco;
* `domain/schemas`: define os dados de entrada e saída da API;
* `services`: contém as regras e a lógica do sistema;
* `routes/v1`: contém os endpoints;
* `database`: possui a conexão, a configuração e o seed do banco;
* `core`: contém as configurações gerais da aplicação.

Estrutura resumida:

```text
academic-api/
├── app/
│   ├── core/
│   ├── database/
│   ├── domain/
│   │   ├── models/
│   │   └── schemas/
│   ├── routes/
│   │   └── v1/
│   ├── services/
│   └── main.py
├── docs/
│   └── fluxograma.md
├── .dockerignore
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## 🐳 Executando com Docker

Para executar o projeto dessa forma, é necessário ter o Docker Desktop instalado e aberto.

Dentro da pasta principal do projeto, execute:

```bash
docker compose up --build
```

Esse comando irá:

1. baixar e iniciar o PostgreSQL;
2. construir a imagem da API;
3. instalar as dependências;
4. criar as tabelas;
5. executar o seed;
6. iniciar o servidor da aplicação.

Depois que os serviços iniciarem, a documentação poderá ser acessada em:

```text
http://127.0.0.1:8000/docs
```

O endpoint de verificação da API está disponível em:

```text
http://127.0.0.1:8000/v1/health
```

Para encerrar os serviços, pressione `Ctrl + C` e execute:

```bash
docker compose down
```

Os dados do PostgreSQL permanecem armazenados no volume do Docker.

Para remover também o volume e começar com um banco vazio, utilize:

```bash
docker compose down -v
```

## 💻 Executando localmente

Para executar sem Docker, crie o ambiente virtual:

```bash
python -m venv .venv
```

No CMD do Windows, ative com:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Crie um arquivo chamado `.env` na pasta principal do projeto com o seguinte conteúdo:

```env
DATABASE_URL=sqlite:///./academic.db
```

Execute o seed:

```bash
python -m app.database.seed
```

Inicie a API:

```bash
uvicorn app.main:app --reload
```

A documentação estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## 🔗 Endpoints principais

### Alunos

```text
POST   /v1/alunos
GET    /v1/alunos
GET    /v1/alunos/{aluno_id}
PUT    /v1/alunos/{aluno_id}
DELETE /v1/alunos/{aluno_id}
```

### Disciplinas

```text
POST   /v1/disciplinas
GET    /v1/disciplinas
GET    /v1/disciplinas/{disciplina_id}
PUT    /v1/disciplinas/{disciplina_id}
DELETE /v1/disciplinas/{disciplina_id}
```

### Turmas

```text
POST   /v1/turmas
GET    /v1/turmas
GET    /v1/turmas/{turma_id}
PUT    /v1/turmas/{turma_id}
DELETE /v1/turmas/{turma_id}
```

### Matrículas

```text
POST  /v1/matriculas
GET   /v1/matriculas
GET   /v1/matriculas/{matricula_id}
PATCH /v1/matriculas/{matricula_id}/cancelar
```

### Notas

```text
POST  /v1/notas
GET   /v1/notas
GET   /v1/notas/{nota_id}
PATCH /v1/notas/{nota_id}
```

A listagem de notas também pode ser filtrada pela matrícula:

```text
GET /v1/notas?matricula_id=1
```

### Relatórios

```text
GET /v1/relatorios/alunos/{aluno_id}/boletim
```

O boletim retorna os dados do aluno, as disciplinas em que ele está matriculado, as notas e a média calculada para cada disciplina.

### Status

```text
GET /v1/health
```

Esse endpoint verifica se a API está funcionando e realiza uma consulta simples para testar a conexão com o banco.

## 🌱 Dados iniciais

O arquivo `app/database/seed.py` adiciona dados iniciais para permitir que o projeto seja testado logo após sua execução.

São cadastrados:

* 5 alunos;
* 3 professores;
* 4 disciplinas;
* 4 turmas;
* matrículas para todos os alunos;
* notas para cada matrícula.

O seed verifica os registros antes de cadastrar, permitindo que ele seja executado novamente sem duplicar os principais dados.

## 📊 Fluxograma

O fluxograma apresenta de forma resumida o funcionamento da API, incluindo os cadastros, as validações de matrícula, o lançamento de notas e a consulta do boletim.

Ele está disponível em:

```text
docs/fluxograma.md
```
