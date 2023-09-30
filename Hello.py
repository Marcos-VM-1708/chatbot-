import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import RetrievalQA
from langchain.callbacks.base import BaseCallbackHandler
from langchain.vectorstores import Chroma

from streamlit.logger import get_logger

# ----------------------------------------------------------------------------------

LOGGER = get_logger(__name__)

os.environ["OPENAI_API_KEY"] = "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"
embeddings = OpenAIEmbeddings()
vectordb = Chroma(persist_directory = "./chroma_db", embedding_function = embeddings)
retriever = vectordb.as_retriever(search_type = "mmr")

# ----------------------------------------------------------------------------------
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container: st.delta_generator.DeltaGenerator, initial_text: str = ""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None

    def on_llm_start(self, serialized: dict, prompts: list, **kwargs):
        if prompts[0].startswith("Human"):
            self.run_id_ignore_token = kwargs.get("run_id")

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        if self.run_id_ignore_token == kwargs.get("run_id", False):
            return
        self.text += token
        self.container.markdown(self.text)
# ----------------------------------------------------------------------------------
def run():
    st.set_page_config(page_title = "Chat Bernhoeft - Gestão de Terceirizados", layout = "wide",
                       initial_sidebar_state = "collapsed")
    st.title("Chat Bernhoeft - Gestão de Terceirizados")

    hide_streamlit_style = """
              <style>
              #MainMenu {visibility: hidden;}
              header {visibility: hidden;}
              [data-testid="collapsedControl"] {visibility: hidden;}
              footer {visibility: hidden;}
              </style>
              """
    st.markdown(hide_streamlit_style, unsafe_allow_html = True)


def gpt():
    os.environ["OPENAI_API_KEY"] = "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"
    openai_api_key = "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"

    msgs = StreamlitChatMessageHistory()

    llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5,
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

    if len(msgs.messages) == 0 or st.sidebar.button("Apagar mensagem"):
        msgs.clear()
        msgs.add_ai_message("Olá, como posso te ajudar?")

    avatars = {"human": "user", "ai": "assistant"}

    for msg in msgs.messages:
        st.chat_message(avatars[msg.type]).write(msg.content)

    if user_query := st.chat_input(placeholder = "Escreva uma mensagem"):
        st.chat_message("user").write(user_query)

        with st.chat_message("assistant"):
            stream_handle = StreamHandler(st.empty())
            print(stream_handle)
            response = qa_chain.run(user_query, callbacks = [stream_handle])


# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    run()
    gpt()
