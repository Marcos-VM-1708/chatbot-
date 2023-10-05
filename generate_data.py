faq = [
    {
        "Pergunta": "Como alterar dados dos Colaboradores na Competência Mensal?",
        "Resposta": {
            "Passos": [
                "Acesse a competência mensal em questão.",
                "Na etapa 8, clique em 'Modificar/Adicionar dados dos colaboradores da competência'.",
                "Na etapa 4, para alterar informações dos colaboradores já cadastrados, basta localizar o colaborador, alterar no campo desejado e clicar em 'salvar' > 'próximo'."
            ],
            "Tutorial": "https://www.youtube.com/watch?v=fz3yIbjPlbc"
        }
    },
    {
        "Pergunta": "Como atualizar colaboradores na etapa 4?",
        "Resposta": {
            "Passos": [
                "Na etapa 4, clique na opção 'Clique aqui'.",
                "Ao baixar a planilha, faça as atualizações necessárias.",
                "Salve a planilha e em seguida anexe no portal na opção 'Escolher arquivo'.",
                "Após validar os dados na tela clique em 'salvar', em seguida clique em 'próximo'."
            ]
        }
    },
    {
        "Pergunta": "Como anexar uma declaração de Não Prestação de Serviço?",
        "Resposta": {
            "Passos": [
                "Na etapa 1 - Confirmar Prestação de Serviço, cliquei em Não.",
                "Baixe o modelo de declaração clicando na opção de 'Clique Aqui'.",
                "Preencha o modelo (A declaração deve ser assinada pelo responsável legal da empresa e deve ser salva em PDF.).",
                "Para anexar, clique em 'Carregar Arquivo' e selecione a documentação.",
                "Clique em 'Próximo'.",
                "Após incluir a declaração e clicar em próximo, o sistema irá para te direcionar para a etapa 05 onde será preciso clicar na opção 'Finalizar'."
            ],
            "Fluxo de validação": [
                "A declaração será analisada pela Bernhoeft de acordo com prazo de análise estabelecido pelo cliente;",
                "Estando a declaração conforme, o documento será encaminhado para que o cliente possa validar se houve ou não a prestação de serviços na competência;",
                "Após a validação do cliente, a informação de NPS (Não Prestação de Serviço) na competência será lançada no sistema e a solicitação de documentos ajustada."
            ],
            "Tutorial": "https://www.youtube.com/watch?v=08tVDMoGJ9M",
            "Nota Importante": "O lançamento da Não prestação de serviços no portal após o envio do relatório de pendências dependerá do tempo de resposta do cliente."
        }
    }
]
import openai
from time import time,sleep

key = "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"
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def gpt_completion(prompt, engine='text-davinci-003', temp=1.0, top_p=1.0, tokens=2048, freq_pen=0.0, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='utf-8', errors='ignore').decode()

    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            #text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            save_file('logs/%s' % filename, prompt + '\n\n----------\n\n' + text)
            return text
        except Exception as fail:
            retry += 1
            if retry >= max_retry:
                return "GPT-3 error: %s" % fail
            print('Error communicating with OpenAI:', fail)
            sleep(1)

