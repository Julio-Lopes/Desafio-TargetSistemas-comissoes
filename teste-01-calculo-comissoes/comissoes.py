"""
Cálculo de comissão por vendedor.

Regras (aplicadas a cada venda individualmente):
  - Venda abaixo de R$ 100,00  -> sem comissão
  - Venda abaixo de R$ 500,00  -> 1% de comissão
  - A partir de R$ 500,00      -> 5% de comissão

Uso:
  python comissoes.py              # usa os dados embutidos abaixo
  python comissoes.py vendas.json  # lê os dados de um arquivo JSON
"""

import json
import sys
from collections import OrderedDict
from decimal import Decimal, ROUND_HALF_UP

DADOS_JSON = """
{
  "vendas": [
    {"vendedor": "João Silva", "valor": 1200.50},
    {"vendedor": "João Silva", "valor": 950.75},
    {"vendedor": "João Silva", "valor": 1800.00},
    {"vendedor": "João Silva", "valor": 1400.30},
    {"vendedor": "João Silva", "valor": 1100.90},
    {"vendedor": "João Silva", "valor": 1550.00},
    {"vendedor": "João Silva", "valor": 1700.80},
    {"vendedor": "João Silva", "valor": 250.30},
    {"vendedor": "João Silva", "valor": 480.75},
    {"vendedor": "João Silva", "valor": 320.40},

    {"vendedor": "Maria Souza", "valor": 2100.40},
    {"vendedor": "Maria Souza", "valor": 1350.60},
    {"vendedor": "Maria Souza", "valor": 950.20},
    {"vendedor": "Maria Souza", "valor": 1600.75},
    {"vendedor": "Maria Souza", "valor": 1750.00},
    {"vendedor": "Maria Souza", "valor": 1450.90},
    {"vendedor": "Maria Souza", "valor": 400.50},
    {"vendedor": "Maria Souza", "valor": 180.20},
    {"vendedor": "Maria Souza", "valor": 90.75},

    {"vendedor": "Carlos Oliveira", "valor": 800.50},
    {"vendedor": "Carlos Oliveira", "valor": 1200.00},
    {"vendedor": "Carlos Oliveira", "valor": 1950.30},
    {"vendedor": "Carlos Oliveira", "valor": 1750.80},
    {"vendedor": "Carlos Oliveira", "valor": 1300.60},
    {"vendedor": "Carlos Oliveira", "valor": 300.40},
    {"vendedor": "Carlos Oliveira", "valor": 500.00},
    {"vendedor": "Carlos Oliveira", "valor": 125.75},

    {"vendedor": "Ana Lima", "valor": 1000.00},
    {"vendedor": "Ana Lima", "valor": 1100.50},
    {"vendedor": "Ana Lima", "valor": 1250.75},
    {"vendedor": "Ana Lima", "valor": 1400.20},
    {"vendedor": "Ana Lima", "valor": 1550.90},
    {"vendedor": "Ana Lima", "valor": 1650.00},
    {"vendedor": "Ana Lima", "valor": 75.30},
    {"vendedor": "Ana Lima", "valor": 420.90},
    {"vendedor": "Ana Lima", "valor": 315.40}
  ]
}
"""

CENTAVOS = Decimal("0.01")


def calcular_comissao(valor: Decimal) -> Decimal:
    """Retorna a comissão de uma única venda."""
    if valor < Decimal("100"):
        taxa = Decimal("0")
    elif valor < Decimal("500"):
        taxa = Decimal("0.01")
    else:
        taxa = Decimal("0.05")
    return (valor * taxa).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def carregar_vendas() -> list:
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            dados = json.load(f, parse_float=Decimal)
    else:
        dados = json.loads(DADOS_JSON, parse_float=Decimal)
    return dados["vendas"]


def formatar_reais(valor: Decimal) -> str:
    texto = f"{valor:,.2f}"  # ex.: 1,234.56
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    vendas = carregar_vendas()

    resumo = OrderedDict()
    for venda in vendas:
        nome = venda["vendedor"]
        valor = Decimal(str(venda["valor"]))
        item = resumo.setdefault(
            nome, {"qtd": 0, "total_vendido": Decimal("0"), "comissao": Decimal("0")}
        )
        item["qtd"] += 1
        item["total_vendido"] += valor
        item["comissao"] += calcular_comissao(valor)

    print(f"{'Vendedor':<18}{'Vendas':>7}{'Total vendido':>18}{'Comissão':>14}")
    print("-" * 57)
    total_geral = Decimal("0")
    for nome, item in resumo.items():
        total_geral += item["comissao"]
        print(
            f"{nome:<18}{item['qtd']:>7}"
            f"{formatar_reais(item['total_vendido']):>18}"
            f"{formatar_reais(item['comissao']):>14}"
        )
    print("-" * 57)
    print(f"{'Total de comissões':<43}{formatar_reais(total_geral):>14}")


if __name__ == "__main__":
    main()
