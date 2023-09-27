import os
import streamlit as st
from streamlit.logger import get_logger

# ----------------------------------------------------------------------------------

LOGGER = get_logger(__name__)


# ----------------------------------------------------------------------------------
def run():
  st.set_page_config(page_title="Chat Bernhoeft - Gestão de Terceirizados", layout="wide", initial_sidebar_state="collapsed")
  st.title("Chat Bernhoeft - Gestão de Terceirizados")

  hide_streamlit_style = """
              <style>
              #MainMenu {visibility: hidden;}
              header {visibility: hidden;}
              [data-testid="collapsedControl"] {visibility: hidden;}
              footer {visibility: hidden;}
              </style>
              """
  st.markdown(hide_streamlit_style, unsafe_allow_html=True)

  def gpt():
    os.environ["OPENAI_API_KEY"] = "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"
    openai_api_key = "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"

    embeddings = OpenAIEmbeddings()
    vectordb = Chroma(persist_directory = "./chroma_db", embedding_function = embeddings)
    retriever = vectordb.as_retriever(search_type = "mmr")

    msgs = StreamlitChatMessageHistory()

    llm = ChatOpenAI(
      model_name = "gpt-3.5-turbo",
      temperature = 0,
      streaming = True
    )
    memory = ConversationBufferMemory(memory_key = "chat_history", chat_memory = msgs, return_messages = True)

    qa_chain = RetrievalQA.from_chain_type(
      llm = llm,
      chain_type = "stuff",
      retriever = retriever,
      memory = memory,
      verbose = True,
    )

if __name__ == "__main__":
    run()
