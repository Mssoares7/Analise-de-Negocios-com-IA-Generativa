import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings  
from llama_index.llms.ollama import Ollama  
from llama_index.core import VectorStoreIndex, Settings, Document
from scripts.read_dados import read_pdf_files, read_word_files  # Atualizado para incluir PDF
import warnings

warnings.filterwarnings('ignore')

# Configurações do Streamlit
st.set_page_config(page_title="Análise de Negócios com IA Generativa", page_icon=":robot_face:", layout="centered")
st.title("Análise de Negócios Baseada em IA Generativa com Ollama, LLM e RAG")

# Inicializa "messages" no estado da sessão, se ainda não existir
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Digite sua pergunta"}
    ]

# Define o LLM (Large Language Model)
llm = Ollama(model="llama3.2", request_timeout=600.0)

# Define o modelo de embeddings
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Diretórios dos dados
pdf_dir = "data/pdf"  # Diretório atualizado para PDF
word_dir = "data/word"

# Função para carregar os dados do diretório
def carregar_dados():
    # Carrega os dados do PDF
    pdf_docs = read_pdf_files(pdf_dir)
    # Carrega os textos do Word
    word_docs = read_word_files(word_dir)
    # Combina os documentos
    all_docs = pdf_docs + word_docs
    # Converte os documentos para objetos Document
    docs = [Document(text=doc, doc_id=f"doc_{i+1}") for i, doc in enumerate(all_docs)]
    return docs

# Função para o Módulo de RAG com LlamaIndex, cacheada pelo Streamlit
@st.cache_resource(show_spinner=False)
def carregar_rag():
    with st.spinner("Carregando e indexando os documentos – aguarde!"):
        docs = carregar_dados()
        # Configura o LLM e o modelo de embeddings nos settings globais
        Settings.llm = llm
        Settings.embed_model = embed_model
        # Cria o índice de vetores a partir dos documentos
        index = VectorStoreIndex.from_documents(docs)
        return index

# Carrega o índice de dados
index = carregar_rag()

# Inicializa o motor de chat se não estiver na sessão
if "chat_engine" not in st.session_state:
    st.session_state["chat_engine"] = index.as_chat_engine(chat_mode="condense_question", verbose=True)

# Verifica se há uma entrada de chat do usuário
if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Exibe as mensagens na interface de chat
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Gera uma resposta se a última mensagem não for do assistente
if st.session_state["messages"][-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            user_message = st.session_state["messages"][-1]["content"]
            contextual_prompt = f"Você é um analista de negócios especializado. O usuário fez a seguinte pergunta: '{user_message}'. Considere todos os relatórios disponíveis e forneça uma resposta detalhada e precisa."
            response = st.session_state["chat_engine"].chat(contextual_prompt)
            st.write(response.response)
            st.session_state["messages"].append({"role": "assistant", "content": response.response})
st.markdown("""
---
#### Desenvolvido por [Matheus da Silva Soares](https://br.linkedin.com/in/matheus-da-silva-soares)
""", unsafe_allow_html=True)