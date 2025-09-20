# Chatbot RAG - Cardápio do McDonald's

Este projeto é um chatbot inteligente construído em Python, capaz de responder a perguntas sobre o cardápio do McDonald's. Ele utiliza a técnica de **RAG (Retrieval-Augmented Generation)** para fornecer respostas precisas com base em um arquivo de dados local, rodando inteiramente na sua máquina, sem depender de APIs externas pagas.

## Como Funciona

O sistema opera em três etapas principais:

1.  **Indexação (Carga de Dados):** O script lê as informações do arquivo `cardapio.json`, que contém todos os itens do menu, suas descrições e preços.
2.  **Recuperação (Busca Inteligente):** Quando uma pergunta é feita, o sistema converte o texto da pergunta em vetores numéricos (embeddings) usando um modelo local (`SentenceTransformers`). Em seguida, ele busca em um banco de dados vetorial em memória (`ChromaDB`) os itens do cardápio mais relevantes para a pergunta.
3.  **Geração (Criação da Resposta):** O contexto recuperado (os itens relevantes do cardápio) é enviado para um Modelo de Linguagem Grande (LLM) rodando localmente via **Ollama** (ex: Llama 3). O LLM então formula uma resposta coesa e em linguagem natural, baseando-se estritamente nas informações fornecidas.

## Tecnologias Utilizadas

-   **Linguagem:** Python 3.10+
-   **Framework de IA:** LangChain
-   **Modelo de Embeddings:** `SentenceTransformers` (`all-MiniLM-L6-v2`)
-   **Banco de Dados Vetorial:** ChromaDB (in-memory)
-   **LLM (Modelo de Linguagem):** Ollama com o modelo `Llama 3`
-   **Gerenciamento de Dependências:** Pip

## ▶️ Como Executar

Com o Ollama rodando em segundo plano e as dependências instaladas, execute o script principal:

```bash
python iniciar_rag.py
```

O script será iniciado e você poderá fazer suas perguntas diretamente no terminal.

## 💬 Exemplo de Uso

```
========================================
Assistente de Cardápio McDonald's Pronto!
========================================

> Faça sua pergunta (ou digite 'sair'): Qual sanduíche tem bacon?

< Resposta: De acordo com o cardápio, o sanduíche que contém bacon é o McNífico Bacon. Sua descrição é: "Hambúrguer bovino, bacon crocante, queijo, alface, tomate e maionese".

> Faça sua pergunta (ou digite 'sair'): Quanto custa a torta de maçã?

< Resposta: A Torta de Maçã custa R$ 7.90.
```
