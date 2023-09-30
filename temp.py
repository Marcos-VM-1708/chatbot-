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