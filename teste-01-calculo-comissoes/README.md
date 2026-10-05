# Teste 1 – Cálculo de Comissões

Programa em Python que lê os registros de vendas de um time comercial (em JSON) e calcula a comissão de cada vendedor.

## Regras de comissão

A comissão é calculada **por venda**, de acordo com o valor:

| Valor da venda | Comissão |
|---|---|
| Abaixo de R$ 100,00 | 0% |
| De R$ 100,00 até R$ 499,99 | 1% |
| A partir de R$ 500,00 | 5% |

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Como executar

Com os dados embutidos no script:

```bash
python comissoes.py
```

Com um arquivo JSON externo:

```bash
python comissoes.py vendas.json
```

O arquivo deve seguir este formato:

```json
{
  "vendas": [
    { "vendedor": "João Silva", "valor": 1200.50 },
    { "vendedor": "Maria Souza", "valor": 90.75 }
  ]
}
```

## Resultado esperado

```
Vendedor           Vendas     Total vendido      Comissão
---------------------------------------------------------
João Silva             10      R$ 10.754,70     R$ 495,69
Maria Souza             9       R$ 9.874,30     R$ 465,96
Carlos Oliveira         8       R$ 7.928,35     R$ 379,38
Ana Lima                9       R$ 8.763,95     R$ 404,99
---------------------------------------------------------
Total de comissões                            R$ 1.746,02
```

## Decisões de implementação

- **Precisão monetária:** os valores são tratados com `Decimal` em vez de `float`. Isso evita erros de arredondamento nos centavos.
- **Arredondamento:** a comissão de cada venda é arredondada para 2 casas decimais (meio para cima) antes de ser somada ao total do vendedor.
- **Limite de R$ 500,00:** uma venda de exatamente R$ 500,00 entra na faixa de 5%, conforme a regra "a partir de".