import PyPDF2
import pandas as pd
import re
import zipfile
import os


def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto = ""
        for pagina in range(len(reader.pages)):
            texto += reader.pages[pagina].extract_text()
    return texto


def processar_dados(texto):
    dados_extraidos = []
    linhas = texto.split("\n")
    
    for linha in linhas:
       
        partes = re.split(r'\s+', linha)
        if len(partes) >= 3:
            dados_extraidos.append([partes[0], partes[1], partes[2]])
    
    return dados_extraidos

def substituir_abreviacoes(dados):
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            if dados[i][j] == "OD":
                dados[i][j] = "Seg.Odontológica"
            elif dados[i][j] == "AMB":
                dados[i][j] = "Ambulatório"


def salvar_em_csv(colunas, dados, nome_arquivo):
    df = pd.DataFrame(dados, columns=colunas)
    df.to_csv(nome_arquivo, index=False)
    print(f"Arquivo CSV '{nome_arquivo}' gerado com sucesso!")


def compactar_em_zip(nome_arquivo_csv, nome_arquivo_zip):
    with zipfile.ZipFile(nome_arquivo_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(nome_arquivo_csv, nome_arquivo_csv)
    print(f"Arquivo ZIP '{nome_arquivo_zip}' gerado com sucesso!")


def main():
    caminho_pdf = "C:/Users/admin/IdeaProjects/transformacao-de-dados2/src/main/resources/Anexo1.pdf"  
    texto_pdf = extrair_texto_pdf(caminho_pdf)  
    
    dados = processar_dados(texto_pdf)

    
    substituir_abreviacoes(dados)

   
    colunas = ["Código", "Descrição", "Tipo"]

   
    salvar_em_csv(colunas, dados, "saida_dados.csv")

    
    usuario_nome = os.getlogin()  
    nome_arquivo_zip = f"Teste_{usuario_nome}.zip"  
    
    compactar_em_zip("saida_dados.csv", nome_arquivo_zip)


if __name__ == "__main__":
    main()
