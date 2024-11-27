import requests
from deep_translator import GoogleTranslator
import os

# Função para consumir a API de conselhos
def obter_conselhos(qtd=1):
    conselhos = []
    for _ in range(qtd):
        response = requests.get("https://api.adviceslip.com/advice")
        if response.status_code == 200:
            dados = response.json()
            conselhos.append((dados['slip']['id'], dados['slip']['advice']))
        else:
            print("Erro ao obter conselho.")
    return conselhos

# Função para salvar os conselhos em um arquivo
def salvar_conselhos(conselhos, nome_arquivo="conselhos.txt"):
    with open(nome_arquivo, 'a') as arquivo:
        for id_conselho, conselho in conselhos:
            arquivo.write(f"ID: {id_conselho}\nConselho: {conselho}\n\n")
    print("Conselhos salvos com sucesso!")

# Função para exibir os conselhos
def mostrar_conselhos(conselhos):
    for id_conselho, conselho in conselhos:
        print(f"ID: {id_conselho}")
        print(f"Conselho: {conselho}\n")

# Função para traduzir conselhos
def traduzir_conselhos(conselhos, idioma_destino="pt"):
    for id_conselho, conselho in conselhos:
        traducao = GoogleTranslator(source='en', target=idioma_destino).translate(conselho)
        print(f"Conselho traduzido: {traducao}\n")

# Função para ler conselhos salvos
def ler_conselhos_salvos(nome_arquivo="conselhos.txt"):
    if not os.path.exists(nome_arquivo):
        print("Nenhum conselho salvo.")
        return []
    with open(nome_arquivo, 'r') as arquivo:
        dados = arquivo.read().strip().split("\n\n")
        conselhos = []
        for dado in dados:
            partes = dado.split("\n")
            id_conselho = partes[0].split(": ")[1]
            conselho = partes[1].split(": ")[1]
            conselhos.append((id_conselho, conselho))
        return conselhos

# Função para mostar como o menu interativo funciona
def menu():
    conselhos = []
    while True:
        print("\nMenu:")
        print("1. Falar da Sabedoria!(Perguntar quantos conselhos ele quer receber)")
        print("2. Mostrar os Conselhos.")
        print("3. Guardar a Sabedoria! (Salvar conselhos em arquivo)")
        print("4. Mostrar os Conselhos guardados.")
        print("5. Traduzir para os Gringos")
        print("6. Relembrar as Dicas traduzidas. (Conselhos salvos e traduzi-los)")
        print("7. Sair.")
        
        opcao = input("Escolha uma opção (1-7): ")
        
        if opcao == "1":
            qtd = int(input("Quantos conselhos você quer receber? "))
            conselhos = obter_conselhos(qtd)
            mostrar_conselhos(conselhos)
        
        elif opcao == "2":
            mostrar_conselhos(conselhos)
        
        elif opcao == "3":
            salvar_conselhos(conselhos)
        
        elif opcao == "4":
            conselhos_salvos = ler_conselhos_salvos()
            mostrar_conselhos(conselhos_salvos)
        
        elif opcao == "5":
            traduzir_conselhos(conselhos, "en")
        
        elif opcao == "6":
            conselhos_salvos = ler_conselhos_salvos()
            acao = input("Deseja traduzir os conselhos salvos? (sim/não): ")
            if acao.lower() == "sim":
                traduzir_conselhos(conselhos_salvos, "pt")
        
        elif opcao == "7":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
