import os
import json
import openai
import subprocess
import pandas as pd
from utils import load_file
from utils import Clean_data
from utils import create_model
from collections import defaultdict
# ---------------------------------
path_data = "categorias/input_data.txt"

with open(path_data, "r", encoding ="utf-8") as data:
    df = data.readlines()
    print(">>> data_join...")
    print(df)

perguntas_respostas: list = []
pergunta_atual = None
resposta_atual = None

for linha in df:
    if linha.startswith("**Pergunta:**"):
        # Se encontrarmos uma nova pergunta, armazenamos a pergunta anterior e começamos uma nova
        if pergunta_atual is not None:
            perguntas_respostas.append((Clean_data(pergunta_atual), Clean_data(resposta_atual)))
        pergunta_atual = linha.lstrip("**Pergunta:** ").strip()
        resposta_atual = ""

    elif pergunta_atual is not None:
        resposta_atual += linha

if pergunta_atual is not None:
    perguntas_respostas.append((Clean_data(pergunta_atual), Clean_data(resposta_atual)))

data = [{"prompt": item[0], "completion": item[1]} for item in perguntas_respostas]
save = pd.DataFrame(data)
print(save.shape)
save.to_csv("Data_raw.csv")
# -----------------------------------------------------------------------------------------

formatted_data = []

for example in data:
    formatted_example = {
        "messages": [
            {"role": "system", "content": "Bernhoeftgpt e um assistente de suporte, seu objetivo e ajudar clientes com suas duvidas."},
            {"role": "user", "content": example["prompt"]},
            {"role": "assistant", "content": example["completion"]}
        ]
    }
    formatted_data.append(formatted_example)

print(formatted_data)
json_data = "\n".join(json.dumps(formatted_example) for formatted_example in formatted_data)

# with open("data_modelv4.jsonl", 'w', encoding= "utf-8") as arquivo_jsonl:
#     for linha in json_data.splitlines():
#         objeto_json = json.loads(linha)
#         json.dump(objeto_json, arquivo_jsonl, ensure_ascii=False)
#         arquivo_jsonl.write('\n')

#_-----------------------------------------------------------------------------------
openai.api_key = "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"

# load_file("Data_modelV4.jsonl") # mode = fine-tune/training

create_model("file-Ie2Jujf5QDynYZHV36jb3s2O", "gpt-3.5-turbo", 5) # model = gpt-3.5-turbo/babbage-002/davinci-002
# ------------------------------------------------------------------
# completion = openai.ChatCompletion.create(
#   model="ftjob-hixiBKPQcwQ2jqorpp2uynDW",
#   messages=[
#     {"role": "user", "content": "qual navegador é o recomendado pelo sistema?"}
#   ]
# )
# print(completion.choices[0].message)



