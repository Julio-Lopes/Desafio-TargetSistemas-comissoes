"""
Cálculo de juros por atraso.

A partir de um valor e de uma data de vencimento, calcula os juros devidos
na data de hoje, considerando 2,5% ao dia (juros simples) sobre o valor
original, para cada dia de atraso.

Uso:
  python juros.py                         # modo interativo
  python juros.py 1500,00 10/09/2026      # valor e vencimento por argumento
"""

import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

TAXA_DIARIA = Decimal("0.025")  # 2,5% ao dia
CENTAVOS = Decimal("0.01")


def calcular_juros(valor, vencimento, hoje=None):
    """Retorna (dias_atraso, juros, total) na data 'hoje'."""
    hoje = hoje or date.today()
    dias_atraso = max((hoje - vencimento).days, 0)
    juros = (valor * TAXA_DIARIA * dias_atraso).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    return dias_atraso, juros, valor + juros


def converter_valor(texto):
    """Aceita '1500', '1500.50', '1500,50' ou '1.500,50'."""
    texto = texto.strip().replace("R$", "").replace(" ", "")
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    try:
        valor = Decimal(texto)
    except InvalidOperation:
        raise ValueError("Valor inválido. Use, por exemplo, 1500,00.")
    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def converter_data(texto):
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError:
        raise ValueError("Data inválida. Use o formato dd/mm/aaaa.")


def formatar_reais(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def ler(mensagem, conversor):
    while True:
        try:
            return conversor(input(mensagem))
        except ValueError as erro:
            print(f"  {erro}")


def main():
    if len(sys.argv) == 3:
        try:
            valor = converter_valor(sys.argv[1])
            vencimento = converter_data(sys.argv[2])
        except ValueError as erro:
            sys.exit(str(erro))
    else:
        valor = ler("Valor (R$): ", converter_valor)
        vencimento = ler("Data de vencimento (dd/mm/aaaa): ", converter_data)

    hoje = date.today()
    dias, juros, total = calcular_juros(valor, vencimento, hoje)

    print()
    print(f"Valor original:   {formatar_reais(valor)}")
    print(f"Vencimento:       {vencimento:%d/%m/%Y}")
    print(f"Data de hoje:     {hoje:%d/%m/%Y}")
    print(f"Dias de atraso:   {dias}")
    print(f"Taxa:             2,5% ao dia")
    print(f"Juros:            {formatar_reais(juros)}")
    print(f"Total a pagar:    {formatar_reais(total)}")
    if dias == 0:
        print("\nTítulo em dia: não há juros a cobrar.")


if __name__ == "__main__":
    main()
