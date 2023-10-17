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
path_data = "categorias\data_raw.txt"

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

with open("dados_model.jsonl", 'w', encoding="utf-8") as arquivo_jsonl:
    for linha in json_data.splitlines():
        objeto_json = json.loads(linha)
        json.dump(objeto_json, arquivo_jsonl, ensure_ascii=False)
        arquivo_jsonl.write('\n')
#--------------------------------------------------------------------------------------
data_dict = {}

for line in json_data.split('\n'):
    if line.strip():
        json_obj = json.loads(line)
        data_dict.update(json_obj)

format_errors = defaultdict(int)

for ex in data_dict:
    if not isinstance(ex, dict):
        format_errors["data_type"] += 1
        continue

    messages = ex.get("messages", None)
    if not messages:
        format_errors["missing_messages_list"] += 1
        continue

    for message in messages:
        if "role" not in message or "content" not in message:
            format_errors["message_missing_key"] += 1

        if any(k not in ("role", "content", "name", "function_call") for k in message):
            format_errors["message_unrecognized_key"] += 1

        if message.get("role", None) not in ("system", "user", "assistant", "function"):
            format_errors["unrecognized_role"] += 1

        content = message.get("content", None)
        function_call = message.get("function_call", None)

        if (not content and not function_call) or not isinstance(content, str):
            format_errors["missing_content"] += 1

    if not any(message.get("role", None) == "assistant" for message in messages):
        format_errors["example_missing_assistant_message"] += 1

if format_errors:
    print("Found errors:")
    for k, v in format_errors.items():
        print(f"{k}: {v}")
else:
    print("No errors found")

#_-----------------------------------------------------------------------------------
# openai.api_key = "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"

# load_file(data = "data_argumentation.jsonl", mode = "fine-tune") # mode = fine-tune/training

# create_model(train = "file-EYMcQxlukxsg0khuTbCg450z", model = "gpt-3.5-turbo", N_epocas = 7) # model = gpt-3.5-turbo/babbage-002/davinci-002
# ------------------------------------------------------------------
# completion = openai.ChatCompletion.create(
#   model="ftjob-hixiBKPQcwQ2jqorpp2uynDW",
#   messages=[
#     {"role": "user", "content": "qual navegador é o recomendado pelo sistema?"}
#   ]
# )
# print(completion.choices[0].message)



