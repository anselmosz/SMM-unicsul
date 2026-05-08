"""
Simulador de meio de pagamentos

UNICSUL - 2026 | Programaçao de Computadores

Desenvolvido por:
Matheus Souza Anselmo | Engenharia de Software
------
Aplicar conhecimentos de algoritmos matemáticos e pensamento computacional desenvolvendo um
simulador de meio de pagamento (SMM) em Python. Para as operações de debito será cobrado 1%
de MDR (valor_taxa da transaçao), e para cartao de credito e credito parcelado será cobrado 5% de MDR.
"""

# Implementar retorno de estrutura de recibo única onde cada modelo de pagamento apresenta seu conteúdo adicional

# Import da classe 'datetime' da biblioteca datetime
from datetime import datetime as dt, timedelta as td

# Import das bibliotecas 'os' e 're'
import os, re


# Ok
def ExibirMenu():
  print(f"""\nUNICSUL - Simulador de Meio de Pagamento - versão 2026 | {dt.now().strftime("%d/%m/%Y")}\n
Meios de pagamento disponiveis:
0 - Cartao de Débito
1 - Cartao de Crédito à Vista
2 - Cartao de Crédito Parcelado
9 - Sair\n""")

# Ok
def ValidarEntrada(opcoes):
  entrada = input("Digite uma opção: ")

  if entrada in (opcoes):
    return entrada
  else:
    print("\nOpção inválida, digite uma das opções do menu!")
    input("Pressione ENTER para limpar a tela e continuar...")
    os.system('cls' if os.name == 'nt' else 'clear')

def limparTela():
  os.system('cls' if os.name == 'nt' else 'clear')

# To do - Improve
def InserirValorDaCompra():
  question = True

  while question == True:
    valor = input("\nInforme o valor da compra: R$ ").strip().replace(',', '.')

    if valor == "" or float(valor) <= 0 :
      print("\nCampo vazio! É necessário informar um valor")
      input("Pressione ENTER para continuar...")
    elif re.fullmatch(r"\d+(\.\d{1,2})?", valor):
      valor_float = float(valor)
      question = False
      return valor_float
    else:
      print("\nFormato inválido! É necessário informar um valor numérico")
      input("Pressione ENTER para continuar...")

# Ok
def InserirParcelas():
  question = True

  while question == True:
    valor = input("\nQuantidade de parcelas (2 ou 3): ").strip()

    if valor == "":
      print("\nCampo vazio! É necessário informar uma quantidde de parcelas")
      input("Pressione ENTER para continuar...")
    elif re.fullmatch(r"^[2-3]", valor):
      parc_int = int(valor)
      question = False
      return parc_int
    else:
      print("\nOpção inválida! Só é possível realizar 2 ou 3 parcelas")
      input("Pressione ENTER para continuar...")

# Ok
def ImprimirRecibo(valor_da_compra, mdr, valor_liq, tipo_opercao):
  limparTela()
  print(f"""\nRecibo da compra\n
Data da compra: {dt.now().strftime("%d/%m/%Y")}
Hora da compra: {dt.now().strftime("%H:%M")}
Meio de pagamento: {tipo_opercao}
Valor da compra: R$ {"{:.2f}".format(valor_da_compra).replace('.', ',')}
Valor do MDR (taxa de transação): R$ {"{:.2f}".format(mdr).replace('.', ',')}
Valor liquído: R$ {"{:.2f}".format(valor_liq).replace('.', ',')}""")

# Ok
def CalcularDataDeCredito(data_credito):
  if data_credito.isoweekday() == 6:
    data_credito += td(days=2)
  elif data_credito.isoweekday() == 7:
    data_credito += td(days=1)

  print(f"Data de crédito: ({data_credito.strftime("%d/%m/%Y")})\n")

# Ok
def DebitoMdr(valor_da_compra):
  mdr = valor_da_compra * 0.01
  val_liq = valor_da_compra - mdr
  dt_cred = dt.now() + td(days=1)

  ImprimirRecibo(valor_da_compra, mdr, val_liq, "0 - Débito")
  CalcularDataDeCredito(dt_cred)

# Ok
def CreditoMdr(valor_da_compra):
  mdr = valor_da_compra * 0.05
  val_liq = valor_da_compra - mdr
  dt_cred = dt.now() + td(days=30)

  ImprimirRecibo(valor_da_compra, mdr, val_liq, "1 - Crédito a vista")
  CalcularDataDeCredito(dt_cred)

# To do
def CreditoMdrParc(valor_da_compra, qtd_parcelas):
  mdr = valor_da_compra * 0.05
  val_liq = valor_da_compra - mdr
  parc_value = val_liq / qtd_parcelas
  dt_cred = dt.now() + td(days=30)

  ImprimirRecibo(valor_da_compra, mdr, val_liq, "2 - Crédito parcelado")

  for i in range(qtd_parcelas):
    if i > 0:
      dt_cred += td(days=30)
    print(f"""Parcela: {i+1}/{qtd_parcelas}
Valor liquido: {"{:.2f}".format(parc_value).replace('.', ',')}""")
    CalcularDataDeCredito(dt_cred)

opcoes = ("0", "1", "2", "9")
sysRun = True

while sysRun == True:
  ExibirMenu()
  entrada = ValidarEntrada(opcoes)

  if entrada == "0":
    valorCompra = InserirValorDaCompra()
    DebitoMdr(valorCompra)

    input("Pressione ENTER para limpar a tela e continuar...")
    limparTela()

  elif entrada == "1":
    valorCompra = InserirValorDaCompra()
    CreditoMdr(valorCompra)

    input("Pressione ENTER para limpar a tela e continuar...")
    limparTela()

  elif entrada == "2":
    valorCompra = InserirValorDaCompra()
    parcelas = InserirParcelas()

    CreditoMdrParc(valorCompra, parcelas)

    input("Pressione ENTER para limpar a tela e continuar...")
    limparTela()

  elif entrada == "9":
    sysRun = False
    print("\nSimulador encerrado, até logo!\n")
