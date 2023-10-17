import json
import openai
from utils import load_file

from utils import Clean_data
from utils import create_model
from collections import defaultdict
import pandas as pd
from utils import gpt_request
# ------------------------------------------------
openai.api_key = "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"
# path : str = "categorias\data_raw.txt"
# df = pd.read_csv("dados.csv")
# print(df["prompt"])
#
# def data_argumentation(df):
#     df = df["prompt"]
#     for linha in df:
#         prompt = gpt_request(linha)
#         print(prompt)
#         break
#
#
# # data_argumentation(df)
import openai

def data_argumentation(sentence, N):
    reformulated_sentences = []
    for _ in range(N):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "user",
                    "content": f"Reformule a seguinte sentença: '{sentence}'\n"
                }
            ],
            temperature = 1,
            max_tokens = 256,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        reformulated_sentence = response['choices'][0]['message']['content']
        reformulated_sentences.append(reformulated_sentence)
    return reformulated_sentences


user_input = "qual o navegador utilizar?"
num_reformulations = 10

# Reformular a sentença dez vezes e armazenar as reformulações em uma lista
reformulations = reformulate_sentence(user_input, num_reformulations)

print("Sentença original:", user_input)
print("Reformulações:")
for i, reformulation in enumerate(reformulations, start=1):
    print(f"Reformulação {i}: {reformulation}")
