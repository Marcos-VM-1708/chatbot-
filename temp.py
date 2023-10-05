import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

os.environ["OPENAI_API_KEY"] = "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"

from langchain.document_loaders import DirectoryLoader
script_dir = os.path.dirname(os.path.abspath(__file__))
txt_folder_path = os.path.join(script_dir, "categorias")

txt_loader = DirectoryLoader(txt_folder_path, glob="**/*.txt")
loaders = [txt_loader]
documents = []
for loader in loaders:
    documents.extend(loader.load())

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(documents, embeddings, persist_directory="./chroma_db")


def txt_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as txtfile:
        lines = txtfile.read().split('\n')

    pairs = []
    current_question = None

    for line in lines:

        if line.strip().startswith("**Pergunta**"):
            # Remove o marcador e adiciona a pergunta
            current_question = line.strip().replace("**Pergunta**: ", "")

        elif line.strip().startswith("**Resposta**"):
            # Remove o marcador e adiciona a resposta
            if current_question:
                answer = line.strip().replace("**Resposta**: ", "")
                pairs.append((current_question, answer))
            else:
                print("A resposta não tem uma pergunta correspondente, será ignorada.")

    # Cria um DataFrame com as perguntas e respostas
    df = pd.DataFrame(pairs, columns=['Pergunta', 'Resposta'])

    # Salva o DataFrame como um arquivo CSV
    df.to_csv(output_file, index=False, encoding='utf-8')



#
# if __name__ == "__main__":
#     input_file  = "C:\\Users\katia\OneDrive\Documentos\GitHub\chatbot-\categorias\categoria_1.txt"
#     output_file = "output.csv"
#
#     txt_to_csv(input_file, output_file)
