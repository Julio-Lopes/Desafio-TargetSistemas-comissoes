# Teste 2 – Movimentação de Estoque

Programa em Python, executado no terminal, para lançar entradas e saídas de mercadorias no depósito. Depois de cada lançamento, ele informa a quantidade final em estoque do produto movimentado.

## Funcionalidades

- **Lançar movimentação** de entrada ou saída de um produto.
- **Consultar o estoque** atual de todos os produtos.
- **Ver o histórico** das movimentações lançadas.

Cada movimentação registra:

| Campo | Descrição |
|---|---|
| `id` | Número identificador único e sequencial |
| `descricao` | Texto que identifica o tipo da movimentação (ex.: "Compra de fornecedor", "Venda", "Devolução") |
| `tipo` | `ENTRADA` ou `SAIDA` |
| `quantidade` | Quantidade movimentada |
| `codigoProduto` | Produto movimentado |
| `estoqueAnterior` / `estoqueFinal` | Saldo antes e depois da movimentação |
| `dataHora` | Data e hora do lançamento |

## Validações

- O produto precisa existir.
- A quantidade deve ser um número inteiro maior que zero.
- A descrição é obrigatória.
- Uma saída não pode deixar o estoque negativo.

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Como executar

```bash
python estoque.py
```

Exemplo de uso:

```
=== CONTROLE DE ESTOQUE ===
1 - Lançar movimentação
2 - Consultar estoque
3 - Histórico de movimentações
0 - Sair
Opção: 1

Código do produto: 101
Tipo (E = entrada, S = saída): E
Quantidade: 50
Descrição (ex.: Compra de fornecedor, Venda, Devolução): Compra de fornecedor

  ✔ Movimentação #1 registrada (ENTRADA de 50 un.).
  Estoque final de Caneta Azul: 200 unidade(s).
```

## Persistência

O estoque e o histórico ficam salvos no arquivo `dados_estoque.json`, criado na primeira movimentação. Assim, os IDs continuam únicos entre execuções. Para voltar ao estoque inicial do enunciado, basta apagar esse arquivo.

## Decisões de implementação

- **ID sequencial:** o próximo ID é sempre o maior ID existente mais 1. Isso garante que não haja repetição e que os números sejam fáceis de ler.
- **Regra separada da interface:** a lógica fica no método `ControleEstoque.movimentar()`, que retorna a movimentação e o estoque final. Ele pode ser reaproveitado ou testado sem o menu do terminal.