import re
import os
import csv
import openai
import pandas as pd
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
#------------------------------
data = "C:\\Users\katia\OneDrive\Documentos\GitHub\chatbot-\categorias\categoria_1.txt"

# Listas para armazenar perguntas e respostas
perguntas = []
respostas = []

# Abrir o arquivo em modo de leitura
with open(data, 'r') as arquivo:
    conteudo = arquivo.read()
    print(conteudo)

padrao = r'\*\*Pergunta(.*?)\*\*Resposta'
correspondencias = re.findall(padrao, conteudo, re.DOTALL)

# Iterar pelas correspondências e salvar perguntas e respostas nas listas
for correspondencia in correspondencias:
    partes = correspondencia.split('**Resposta')
    print(partes)
    if len(partes) == 2:
        perguntas.append(partes[0].strip())
        respostas.append(partes[1].strip())

# Agora você tem as perguntas em 'perguntas' e as respostas em 'respostas'
print("Perguntas:")
for pergunta in perguntas:
    print(pergunta)

print("\nRespostas:")
for resposta in respostas:
    print(resposta)
