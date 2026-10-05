"""
Controle de movimentações de estoque.

Permite lançar entradas e saídas de produtos no depósito. Cada movimentação
recebe um ID único e sequencial e uma descrição, e o programa informa o
estoque final do produto após o lançamento.

Os dados (estoque e histórico) são salvos em "dados_estoque.json", para que
os IDs continuem únicos entre uma execução e outra.

Uso:
  python estoque.py
"""

import json
import os
from datetime import datetime

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados_estoque.json")

ESTOQUE_INICIAL = {
    "estoque": [
        {"codigoProduto": 101, "descricaoProduto": "Caneta Azul", "estoque": 150},
        {"codigoProduto": 102, "descricaoProduto": "Caderno Universitário", "estoque": 75},
        {"codigoProduto": 103, "descricaoProduto": "Borracha Branca", "estoque": 200},
        {"codigoProduto": 104, "descricaoProduto": "Lápis Preto HB", "estoque": 320},
        {"codigoProduto": 105, "descricaoProduto": "Marcador de Texto Amarelo", "estoque": 90},
    ]
}

ENTRADA = "ENTRADA"
SAIDA = "SAIDA"


class ErroMovimentacao(Exception):
    """Erro de regra de negócio ao movimentar o estoque."""


class ControleEstoque:
    def __init__(self, arquivo=ARQUIVO_DADOS):
        self.arquivo = arquivo
        self.produtos = {}
        self.movimentacoes = []
        self._carregar()

    # ---------- persistência ----------
    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, encoding="utf-8") as f:
                dados = json.load(f)
            self.movimentacoes = dados.get("movimentacoes", [])
        else:
            dados = ESTOQUE_INICIAL
        self.produtos = {p["codigoProduto"]: dict(p) for p in dados["estoque"]}

    def _salvar(self):
        dados = {"estoque": list(self.produtos.values()), "movimentacoes": self.movimentacoes}
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def _proximo_id(self):
        return max((m["id"] for m in self.movimentacoes), default=0) + 1

    # ---------- regra de negócio ----------
    def movimentar(self, codigo, tipo, quantidade, descricao):
        """Lança uma movimentação e retorna (movimentacao, estoque_final)."""
        produto = self.produtos.get(codigo)
        if produto is None:
            raise ErroMovimentacao(f"Produto {codigo} não encontrado.")
        if tipo not in (ENTRADA, SAIDA):
            raise ErroMovimentacao("Tipo deve ser ENTRADA ou SAIDA.")
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ErroMovimentacao("A quantidade deve ser um número inteiro maior que zero.")
        if not descricao or not descricao.strip():
            raise ErroMovimentacao("Informe uma descrição para a movimentação.")
        if tipo == SAIDA and quantidade > produto["estoque"]:
            raise ErroMovimentacao(
                f"Estoque insuficiente: há {produto['estoque']} unidade(s) de "
                f"{produto['descricaoProduto']}."
            )

        estoque_anterior = produto["estoque"]
        produto["estoque"] += quantidade if tipo == ENTRADA else -quantidade

        movimentacao = {
            "id": self._proximo_id(),
            "dataHora": datetime.now().isoformat(timespec="seconds"),
            "codigoProduto": codigo,
            "tipo": tipo,
            "descricao": descricao.strip(),
            "quantidade": quantidade,
            "estoqueAnterior": estoque_anterior,
            "estoqueFinal": produto["estoque"],
        }
        self.movimentacoes.append(movimentacao)
        self._salvar()
        return movimentacao, produto["estoque"]


# ---------- interface de terminal ----------
def ler_inteiro(mensagem):
    while True:
        try:
            return int(input(mensagem).strip())
        except ValueError:
            print("  Digite um número inteiro válido.")


def listar_estoque(controle):
    print(f"\n{'Código':<8}{'Produto':<30}{'Estoque':>8}")
    print("-" * 46)
    for p in controle.produtos.values():
        print(f"{p['codigoProduto']:<8}{p['descricaoProduto']:<30}{p['estoque']:>8}")


def listar_movimentacoes(controle):
    if not controle.movimentacoes:
        print("\nNenhuma movimentação lançada.")
        return
    print(f"\n{'ID':<5}{'Data/hora':<21}{'Prod.':<7}{'Tipo':<9}{'Qtde':>6}{'Final':>7}  Descrição")
    print("-" * 80)
    for m in controle.movimentacoes:
        print(
            f"{m['id']:<5}{m['dataHora'].replace('T', ' '):<21}{m['codigoProduto']:<7}"
            f"{m['tipo']:<9}{m['quantidade']:>6}{m['estoqueFinal']:>7}  {m['descricao']}"
        )


def lancar_movimentacao(controle):
    listar_estoque(controle)
    codigo = ler_inteiro("\nCódigo do produto: ")
    opcao = input("Tipo (E = entrada, S = saída): ").strip().upper()
    tipo = {"E": ENTRADA, "S": SAIDA}.get(opcao)
    if tipo is None:
        print("  Tipo inválido.")
        return
    quantidade = ler_inteiro("Quantidade: ")
    descricao = input("Descrição (ex.: Compra de fornecedor, Venda, Devolução): ")

    try:
        mov, estoque_final = controle.movimentar(codigo, tipo, quantidade, descricao)
    except ErroMovimentacao as erro:
        print(f"\n  ✖ {erro}")
        return

    nome = controle.produtos[codigo]["descricaoProduto"]
    print(f"\n  ✔ Movimentação #{mov['id']} registrada ({mov['tipo']} de {quantidade} un.).")
    print(f"  Estoque final de {nome}: {estoque_final} unidade(s).")


def main():
    controle = ControleEstoque()
    opcoes = {
        "1": ("Lançar movimentação", lancar_movimentacao),
        "2": ("Consultar estoque", listar_estoque),
        "3": ("Histórico de movimentações", listar_movimentacoes),
    }
    while True:
        print("\n=== CONTROLE DE ESTOQUE ===")
        for chave, (texto, _) in opcoes.items():
            print(f"{chave} - {texto}")
        print("0 - Sair")
        escolha = input("Opção: ").strip()
        if escolha == "0":
            break
        if escolha in opcoes:
            opcoes[escolha][1](controle)
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()