# Fluxograma - Academic API

Este fluxograma mostra de forma resumida como funciona a API e quais operações podem ser realizadas.

flowchart TD
    A[Início] --> B[Usuário acessa a API pelo Swagger]
    B --> C{Qual operação será realizada?}

    C --> D[Gerenciar alunos]
    C --> E[Gerenciar disciplinas]
    C --> F[Gerenciar turmas]
    C --> G[Realizar matrícula]
    C --> H[Lançar ou corrigir nota]
    C --> I[Consultar boletim]
    C --> J[Verificar status da API]

    D --> K[Executar cadastro, consulta, alteração ou exclusão]
    E --> K
    F --> K

    G --> L{Aluno e turma existem?}
    L -- Não --> M[Retornar erro]
    L -- Sim --> N{Existe vaga e a matrícula não está duplicada?}
    N -- Não --> M
    N -- Sim --> O[Criar matrícula]

    H --> P{Matrícula válida?}
    P -- Não --> M
    P -- Sim --> Q[Salvar ou corrigir nota]

    I --> R[Buscar disciplinas e notas do aluno]
    R --> S[Calcular média]
    S --> T[Exibir boletim]

    J --> U[Testar conexão com o banco]

    K --> V[(Banco de dados)]
    O --> V
    Q --> V
    R --> V
    U --> V

    V --> W[Fim]
    M --> W
    T --> W

