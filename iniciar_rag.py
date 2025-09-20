import os
import json
import logging
from typing import List
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def carregar_e_preparar_cardapio(caminho_arquivo: str) -> List[str]:
    """Carrega o cardápio em JSON e retorna textos formatados para embeddings."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except FileNotFoundError:
        logging.error("Arquivo de cardápio não encontrado: %s", caminho_arquivo)
        raise

    documentos_formatados = []
    menu = dados.get("McDonalds_Menu", {})
    for categoria, itens in menu.items():
        for item in itens:
            texto_item = (
                f"Categoria: {categoria}\n"
                f"Nome: {item['nome']}\n"
                f"Descrição: {item['descricao']}\n"
                f"Preço: R$ {item['preco']:.2f}"
            )
            documentos_formatados.append(texto_item)

    return documentos_formatados


def inicializar_vector_store(documentos: List[str]):
    """Cria embeddings e inicializa o banco vetorial."""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    docs_langchain = [Document(page_content=doc) for doc in documentos]
    vector_store = Chroma.from_documents(documents=docs_langchain, embedding=embeddings)
    return vector_store.as_retriever(search_kwargs={"k": 3})


def inicializar_chain(retriever):
    """Configura o RAG chain com modelo e prompt."""
    llm = Ollama(model="llama3") 
    prompt_template = """
    Você é um assistente especialista do cardápio do McDonald's.
    Use apenas o contexto fornecido para responder.
    Se a informação não estiver no contexto, diga que não encontrou.
    
    Contexto:
    {context}
    
    Pergunta:
    {question}
    
    Resposta:
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    return (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )


def main():

    documentos = carregar_e_preparar_cardapio("cardapio.json")
    logging.info("%d documentos carregados.", len(documentos))

    retriever = inicializar_vector_store(documentos)
    rag_chain = inicializar_chain(retriever)

    logging.info("Assistente do McDonald's pronto para uso!")

    while True:
        pergunta = input("\n> Faça sua pergunta (ou digite 'sair'): ")
        if pergunta.lower() == "sair":
            break
        try:
            resposta = rag_chain.invoke(pergunta)
            print(f"\n< Resposta: {resposta}")
        except Exception as e:
            logging.error("Erro ao gerar resposta: %s", str(e))

    print("\nAté a próxima!")


if __name__ == "__main__":
    main()
