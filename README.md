# Testes Técnicos – Python

Repositório com a resolução de três testes técnicos em Python. Cada teste fica em sua própria pasta, com o código-fonte e um README explicando as regras, o modo de execução e as decisões tomadas.

## Testes

| # | Pasta | Descrição |
|---|---|---|
| 1 | [`teste-01-calculo-comissoes`](teste-01-calculo-comissoes/) | Lê os registros de vendas de um time comercial e calcula a comissão de cada vendedor por faixa de valor (0%, 1% ou 5%). |
| 2 | [`teste-02-movimentacao-estoque`](teste-02-movimentacao-estoque/) | Lança entradas e saídas de produtos no depósito. Cada movimentação tem ID único e descrição, e o programa informa o estoque final do produto. |
| 3 | [`teste-03-calculo-juros`](teste-03-calculo-juros/) | Calcula os juros de um título vencido até a data de hoje, à taxa de 2,5% ao dia. |

## Estrutura

```
.
├── README.md
├── teste-01-calculo-comissoes/
│   ├── README.md
│   └── comissoes.py
├── teste-02-movimentacao-estoque/
│   ├── README.md
│   └── estoque.py
└── teste-03-calculo-juros/
    ├── README.md
    └── juros.py
```

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa: todos os testes usam apenas a biblioteca padrão

## Como executar

Clone o repositório e entre na pasta do teste desejado:

```bash
cd teste-01-calculo-comissoes
python comissoes.py
```

```bash
cd teste-02-movimentacao-estoque
python estoque.py
```

```bash
cd teste-03-calculo-juros
python juros.py
```

Os detalhes de cada programa (parâmetros, exemplos de saída e validações) estão no README da respectiva pasta.

## Decisões gerais

- **Precisão monetária:** os cálculos com dinheiro (testes 1 e 3) usam `Decimal` em vez de `float`, para evitar erros de arredondamento nos centavos.
- **Regra separada da interface:** a lógica de negócio fica em funções ou métodos próprios (`calcular_comissao`, `ControleEstoque.movimentar`, `calcular_juros`), separados da leitura e exibição no terminal. Isso facilita reaproveitar e testar o código.
- **Validação de entradas:** os programas tratam dados inválidos com mensagens claras, sem encerrar com erro.
- **Formato brasileiro:** valores em reais são exibidos como `R$ 1.234,56` e datas como `dd/mm/aaaa`.
