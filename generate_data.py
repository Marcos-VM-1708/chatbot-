import io
import openai
import pandas as pd
from time import time,sleep
#-------------------------------------------------------------------------------------------
#>>> Etapa 1 pipe line, correção dos dados txt
# task criar script que corrige o document txt line in line

data : str = "C:\\Users\katia\OneDrive\Documentos\GitHub\chatbot-\categorias\categoria_1.txt"


# Join data:
# mudar o codigo0 para abrir no formato utf-8 - ok

try:
    with io.open(data, mode="r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
        # arquivo = arquivo.read()   # ou um ou outro

except FileNotFoundError:
    print(f"O arquivo '{data}' não foi encontrado.")

except Exception as e:
    print(f"Ocorreu um erro: {str(e)}")

# ----------------------------------------
# Splite:

perguntas = []
respostas = []

for palavra in linhas:
    if palavra.startswith("**Pergunta** :"):
        perguntas.append(palavra.replace("Pergunta: ", ""))
    elif palavra.startswith("**Resposta** :"):
        respostas.append(palavra.replace("Resposta: ", ""))

# Exiba as listas separadas
print("Perguntas:")
for pergunta in perguntas:
    print(pergunta)

print("\nRespostas:")
for resposta in respostas:
    print(resposta)

df = pd.DataFrame()
df["prompt"] = perguntas
df["completion"] = respostas

# ----------------------------------------
df["prompt"] = df["prompt"].str.replace("**Pergunta** :", '').str.strip()
df["completion"] = df["completion"].str.replace("**Resposta** :", '').str.strip()
print(df.head())

# df.to_csv("prompt.csv")
print(df.columns)

# openai tools fine_tunes.prepare_data -f prompt.csv
# set OPENAI_API_KEY= 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

#-------------------------------------------------------------------------------------------
# fine tune:

# openai api fine_tunes.create -t prompt_prepared.jsonl -m ada
openai.api_key = "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"

openai.File.create(
  file=open("prompt_prepared.jsonl", "rb"),
  purpose='fine-tune'
)

openai.FineTuningJob.create(training_file="file-abc123", model="gpt-3.5-turbo")
openai.FineTuningJob.list(limit=10)

# openai api fine_tunes.follow -i <YOUR_FINE_TUNE_JOB_ID>
#-------------------------------------------------------------------------------------------
# MODEL
1594511518946516122515515


completion = openai.ChatCompletion.create(
  model="ft:gpt-3.5-turbo:my-org:custom_suffix:id",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "qual navegador devo utilizar? "}
  ]
)
print(completion.choices[0].message)