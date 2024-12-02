import requests
from deep_translator import GoogleTranslator
import os

# Função para consumir a API de conselhos
def obter_conselhos(qtd=1):
    conselhos = []
    for _ in range(qtd):
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            response.raise_for_status()  # Levanta exceção se status_code não for 200
            dados = response.json()
            conselhos.append((dados['slip']['id'], dados['slip']['advice']))
        except requests.RequestException as e:
            print(f"Erro ao obter conselho: {e}")
            break
    return conselhos

# Função para salvar os conselhos em um arquivo
def salvar_conselhos(conselhos, nome_arquivo="conselhos.txt"):
    if not conselhos:
        print("Não há conselhos para salvar.")
        return
    try:
        with open(nome_arquivo, 'a') as arquivo:
            for id_conselho, conselho in conselhos:
                arquivo.write(f"ID: {id_conselho}\nConselho: {conselho}\n\n")
        print("Conselhos salvos com sucesso!")
    except IOError as e:
        print(f"Erro ao salvar conselhos: {e}")

# Função para exibir os conselhos
def mostrar_conselhos(conselhos):
    if not conselhos:
        print("Nenhum conselho disponível para mostrar.")
        return
    for id_conselho, conselho in conselhos:
        print(f"ID: {id_conselho}")
        print(f"Conselho: {conselho}\n")

# Função para traduzir conselhos
def traduzir_conselhos(conselhos, idioma_destino="pt"):
    if not conselhos:
        print("Nenhum conselho disponível para traduzir.")
        return
    for id_conselho, conselho in conselhos:
        try:
            traducao = GoogleTranslator(source='en', target=idioma_destino).translate(conselho)
            print(f"Conselho traduzido: {traducao}\n")
        except Exception as e:
            print(f"Erro ao traduzir conselho: {e}")

# Função para ler conselhos salvos
def ler_conselhos_salvos(nome_arquivo="conselhos.txt"):
    conselhos = []
    if not os.path.exists(nome_arquivo):
        print("Nenhum conselho salvo.")
        return conselhos
    try:
        with open(nome_arquivo, 'r') as arquivo:
            dados = arquivo.read().strip().split("\n\n")
            for dado in dados:
                partes = dado.split("\n")
                try:
                    id_conselho = partes[0].split(": ")[1]
                    conselho = partes[1].split(": ")[1]
                    conselhos.append((id_conselho, conselho))
                except IndexError:
                    print(f"Erro de formatação no arquivo {nome_arquivo}. Dados corrompidos.")
    except IOError as e:
        print(f"Erro ao ler o arquivo de conselhos: {e}")
    return conselhos

# Função para mostrar o menu interativo
def menu():
    conselhos = []
    while True:
        print("\nMenu:")
        print("1. Falar da Sabedoria! (Perguntar quantos conselhos você quer receber)")
        print("2. Mostrar os Conselhos.")
        print("3. Guardar a Sabedoria! (Salvar conselhos em arquivo)")
        print("4. Mostrar os Conselhos guardados.")
        print("5. Traduzir para os Gringos")
        print("6. Relembrar as Dicas traduzidas. (Conselhos salvos e traduzi-los)")
        print("7. Sair.")
        
        opcao = input("Escolha uma opção (1-7): ")
        
        if opcao == "1":
            try:
                qtd = int(input("Quantos conselhos você quer receber? "))
                if qtd <= 0:
                    print("A quantidade de conselhos deve ser um número positivo.")
                else:
                    conselhos = obter_conselhos(qtd)
                    mostrar_conselhos(conselhos)
            except ValueError:
                print("Por favor, insira um número válido.")
        
        elif opcao == "2":
            mostrar_conselhos(conselhos)
        
        elif opcao == "3":
            salvar_conselhos(conselhos)
        
        elif opcao == "4":
            conselhos_salvos = ler_conselhos_salvos()
            mostrar_conselhos(conselhos_salvos)
        
        elif opcao == "5":
            traduzir_conselhos(conselhos, "pt")
        
        elif opcao == "6":
            conselhos_salvos = ler_conselhos_salvos()
            if conselhos_salvos:
                traduzir_conselhos(conselhos_salvos, "pt")
            else:
                print("Nenhum conselho salvo para traduzir.")
        
        elif opcao == "7":
            print("Saindo do programa...")
            break
        
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
