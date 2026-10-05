# Teste 3 – Cálculo de Juros por Atraso

Programa em Python que recebe um valor e uma data de vencimento e calcula os juros devidos na data de hoje. A taxa considerada é de **2,5% ao dia** de atraso.

## Regra de cálculo

```
dias de atraso = hoje − vencimento   (mínimo 0)
juros          = valor × 2,5% × dias de atraso
total          = valor + juros
```

Os juros são **simples**: os 2,5% incidem sempre sobre o valor original, e não sobre o valor já acrescido de juros. Se o vencimento for hoje ou uma data futura, não há juros.

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa

## Como executar

No modo interativo, o programa pede os dados:

```bash
python juros.py
```

Também é possível passar os dados por argumento:

```bash
python juros.py 1500,00 25/09/2026
```

O valor pode ser digitado como `1500`, `1500.50`, `1500,50` ou `1.500,50`. A data deve estar no formato `dd/mm/aaaa`.

## Exemplo

Executado em 05/10/2026:

```
Valor original:   R$ 1.500,00
Vencimento:       25/09/2026
Data de hoje:     05/10/2026
Dias de atraso:   10
Taxa:             2,5% ao dia
Juros:            R$ 375,00
Total a pagar:    R$ 1.875,00
```

## Decisões de implementação

- **Juros simples:** o enunciado fala em 2,5% ao dia sem citar capitalização. Por isso, adotei juros simples, que é o padrão mais comum em cobranças por atraso. Para usar juros compostos, basta trocar a fórmula em `calcular_juros()` por `valor * ((1 + TAXA_DIARIA) ** dias_atraso - 1)`.
- **Dias corridos:** o atraso é contado em dias corridos, sem desconsiderar fins de semana ou feriados.
- **Precisão monetária:** os cálculos usam `Decimal`, com arredondamento para 2 casas decimais (meio para cima).
- **Validações:** o programa recusa valores inválidos ou menores ou iguais a zero e datas inexistentes (ex.: 31/02).
- **Função testável:** `calcular_juros(valor, vencimento, hoje)` aceita a data de "hoje" como parâmetro, o que permite testar o cálculo com datas fixas.