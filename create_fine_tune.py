import json
import openai
import pandas as pd
from utils import load_file
from utils import Clean_data
from utils import create_model
from utils import data_argumentation
from collections import defaultdict

# ------------------------------------------------

path : str = "categorias\data_raw.txt"
class train_gpt:
    def __init__(self, path_data, load, model_name, api_key):

        openai.api_key = api_key
        self.path_data = path_data
        self.file_path = "data_model.jsonl"
        self.validate = {} # date Validation
        self.datav2 = []   # default fine tune gpt2
        self.datav3 = []   # default fine tune gpt3
        self.data = None   # jsonl for model
        self.txt = None    # objeto txt (input data)
        self.model_name = model_name # gpt-3.5-turbo/babbage-002/davinci-002
        self.Synthetic_data = []
        self.load = load
        self.file_id = None
        self.job_id = None
        self.model_id = None

    # -------------------------------------------------------------
    def join_data(self):
        with open(self.path_data, "r", encoding = "utf-8") as data:
            self.txt = data.readlines()  # texto aberto
            print(">>> data_join...")

    # -------------------------------------------------------------

    def split_data(self):
        # Orgaaniza os dados de entrada:
        pergunta_atual = None
        resposta_atual = None

        for linha in self.txt:
            if linha.startswith("**Pergunta:**"):
                if pergunta_atual is not None:
                    self.datav2.append((Clean_data(pergunta_atual), Clean_data(resposta_atual)))
                pergunta_atual = linha.lstrip("**Pergunta:** ").strip()
                resposta_atual = ""

            elif pergunta_atual is not None:
                resposta_atual += linha

        if pergunta_atual is not None:
            self.datav2.append((Clean_data(pergunta_atual), Clean_data(resposta_atual)))
        # --------------------------------------------------------------------------------------------
        # data argumentation:
        local_data = []
        for item in self.datav2:
            data_argumentation(sentence = item[0], N = 1, lista = local_data)
            for new_sentence in local_data:
                temp = (new_sentence, item[1])
                self.Synthetic_data.append(temp)
        print(local_data)
        while True:
            input("enter for continue")
            break

        # --------------------------------------------------------------------------------------------
        self.datav2 = [{"prompt": item[0], "completion": item[1]} for item in self.datav2]
        # self.save = pd.DataFrame(self.datav2)
        # self.save.to_csv("dados.csv")
        print(">>> split_data...")

    # -------------------------------------------------------------

    def transformer_data(self):
        # transformação gpt v3
        for example in self.datav2:

            formatted_example = {
                "messages": [
                    {"role": "system",
                     "content": "seu nome é Bernhoeftgpt, você é um assistente de suporte, seu objetivo e ajudar clientes com suas duvidas."},
                    {"role": "user", "content": example["prompt"]},
                    {"role": "assistant", "content": example["completion"]}
                ]
            }

            self.datav3.append(formatted_example)

        self.data = "\n".join(json.dumps(formatted_example) for formatted_example in self.datav3)

        with open(self.file_path, 'w', encoding = "utf-8") as arquivo_jsonl:
            for linha in self.data.splitlines():
                objeto_json = json.loads(linha)
                json.dump(objeto_json, arquivo_jsonl, ensure_ascii = False)
                arquivo_jsonl.write('\n')

        print(">>> transform_data...")

    # -------------------------------------------------------------

    def resize(self):
        # formatação p/ validação openai
        for line in self.data.split('\n'):
            if line.strip():
                json_obj = json.loads(line)
                self.validate.update(json_obj)

    # -------------------------------------------------------------

    def validate_data(self):
        # validação openai:
        format_errors = defaultdict(int)

        for ex in self.validate:

            if not isinstance(ex, dict):
                format_errors["data_type"]
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
            print(">>>Found errors...")
            for k, v in format_errors.items():
                print(f">>> {k}: {v}...")
        else:
            print(">>> No errors found...")

    # -------------------------------------------------------------

    def training(self, file_id, N_epocas):
        if self.load:
            self.get_id = load_file(self.file_path)
            self.get_model = create_model(file_id = self.get_id, model_name = self.model_name, N_epocas = N_epocas)
        else:
            print(">>> arquivos não foram enviados para openai...")



model = train_gpt(path_data = path, model_name = "gpt-3.5-turbo", load = False, api_key = "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")
model.join_data()
model.split_data()
# model.transformer_data()
# # model.resize()
# model.validate_data()
# model.training(file_id = None, N_epocas = 7)
