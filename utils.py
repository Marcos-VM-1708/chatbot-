import re
import openai
# ------------------------------------
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def data_argumentation(sentence, N, lista):
    for _ in range(N):
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "user",
                    "content": f"Reformule a seguinte sentença : '{sentence}'\n"
                }
            ],
            temperature = 1,
            max_tokens = 60,
            top_p = 1,
            frequency_penalty = 0,
            presence_penalty = 0
        )
        reformulated_sentence = response['choices'][0]['message']['content']
        lista.append(reformulated_sentence)
    return lista

# ------------------------------------

def Clean_data(texto):
    texto_limpo = re.sub(r'[^a-zA-Z0-9\s.,?!áéíóúÁÉÍÓÚâêîôûÂÊÎÔÛãẽĩõũÃẼĨÕŨàèìòùÀÈÌÒÙ]', '', texto)
    return texto_limpo

# ------------------------------------

def load_file(file_path):
    file = openai.File.create(
        file=open(file_path, "rb"),
        purpose='fine-tune'
    )

    print(f"File ID: {file.id}")
    return file.id
# ------------------------------------

def create_model(file_id, model_name, N_epocas):
    if file_id is None:
        file_id = file_id

    if file_id is None:
        raise ValueError("Arquivo não carregado. Chame o método 'load_file' primeiro.")

    job = openai.FineTuningJob.create(training_file=file_id, model= model_name, hyperparameters={"n_epochs":N_epocas})

    print(f"Job ID: {job.id}")
    return job.id

def delete_file(file):
    openai.File.delete(file)

def delete_model(model):
    openai.Model.delete(model)

