import re
import openai
# ------------------------------------
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
def gpt_request(prompt):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": "você é um assistente literário, seu objetivo é reformular sentenças de maneira dez maneiras diferentes, de maneira conivente. "
        },
        {
          "role": "user",
          "content": prompt
        },
        {
          "role": "assistant",
          "content": "Qual seria o navegador mais adequado para o meu uso?\n\nQual navegador é mais recomendado para mim?\n\nQual navegador atenderia melhor às minhas necessidades?\n\nQual é a melhor opção de navegador para mim?\n\nQual navegador é mais indicado para o meu caso?\n\nQual navegador me proporcionaria a melhor experiência?\n\nQual seria a escolha mais acertada de navegador no meu caso?\n\nQual navegador se encaixaria melhor com as minhas preferências?\n\nQual é o navegador mais apropriado para o que eu preciso?\n\nQual navegador seria mais vantajoso para mim?"
        }
      ],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    return response

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

