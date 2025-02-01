import streamlit as st
import subprocess

# Função para rodar o Ollama via comando do sistema
def run_ollama(question):
    command = [
        "C:\\Users\\Administrador\\AppData\\Local\\Programs\\Ollama\\ollama.exe",
        "run",
        "llama3.2",
        "--question",
        question
    ]
    result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
    return result.stdout

# Interface principal do Streamlit
def main():
    st.title("Interação com Ollama")
    user_query = st.text_input("Digite sua pergunta para o Ollama:")
    if st.button("Obter Resposta"):
        if user_query:
            response = run_ollama(user_query)
            st.text_area("Resposta do Ollama:", value=response, height=300)
        else:
            st.error("Por favor, insira uma pergunta.")

if __name__ == "__main__":
    main()
