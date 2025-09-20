import os
import json
from getpass import getpass

# --- PARTE 1: CONFIGURAÇÃO E CARREGAMENTO DOS DADOS ---

# 1. Configuração da Chave de API (boa prática para os próximos passos)
# Se a variável de ambiente não existir, o script pedirá para você colar a chave.
# Por enquanto, não vamos usá-la, mas já deixamos pronto.
if "GOOGLE_API_KEY" not in os.environ:
    # A função getpass esconde a chave enquanto você digita
    os.environ["GOOGLE_API_KEY"] = getpass("Cole aqui sua Google API Key (não será usada nesta parte): ")


# 2. Conteúdo do seu JSON
# Colamos aqui o JSON que você forneceu.
cardapio_json_string = """
{
  "McDonalds_Menu": {
    "Sanduiches": [
      { "id": 1, "nome": "Big Mac", "descricao": "Dois hambúrgueres, alface, queijo, molho especial, cebola e picles no pão com gergelim", "preco": 24.90 },
      { "id": 2, "nome": "Quarterão com Queijo", "descricao": "Hambúrguer 100% carne bovina com queijo cheddar, cebola, picles, ketchup e mostarda", "preco": 22.90 },
      { "id": 3, "nome": "McChicken", "descricao": "Frango empanado crocante, alface e maionese especial no pão com gergelim", "preco": 20.90 },
      { "id": 4, "nome": "Cheddar McMelt", "descricao": "Hambúrguer bovino com molho cremoso de cheddar e cebola ao shoyu", "preco": 23.90 },
      { "id": 5, "nome": "Duplo Quarterão", "descricao": "Dois hambúrgueres bovinos, queijo cheddar, cebola, ketchup e mostarda", "preco": 27.90 },
      { "id": 6, "nome": "McFish", "descricao": "Filé de peixe empanado, queijo e molho tártaro no pão fofo", "preco": 21.90 },
      { "id": 7, "nome": "McVeggie", "descricao": "Hambúrguer vegetal com alface, tomate e molho especial", "preco": 22.50 },
      { "id": 8, "nome": "McNífico Bacon", "descricao": "Hambúrguer bovino, bacon crocante, queijo, alface, tomate e maionese", "preco": 25.90 }
    ],
    "Acompanhamentos": [
      { "id": 9, "nome": "McFritas Pequena", "descricao": "Batatas fritas crocantes tamanho pequeno", "preco": 8.90 },
      { "id": 10, "nome": "McFritas Média", "descricao": "Batatas fritas crocantes tamanho médio", "preco": 11.90 },
      { "id": 11, "nome": "McFritas Grande", "descricao": "Batatas fritas crocantes tamanho grande", "preco": 14.90 },
      { "id": 12, "nome": "Chicken McNuggets 6 unid.", "descricao": "Nuggets de frango empanado", "preco": 15.90 },
      { "id": 13, "nome": "Chicken McNuggets 10 unid.", "descricao": "Nuggets de frango empanado", "preco": 22.90 },
      { "id": 14, "nome": "Cheddar McFritas", "descricao": "Batata frita coberta com molho cheddar cremoso e bacon", "preco": 16.90 },
      { "id": 15, "nome": "Salada Premium", "descricao": "Mix de folhas, tomate-cereja, croutons e molho à escolha", "preco": 14.50 }
    ],
    "Sobremesas": [
      { "id": 16, "nome": "McFlurry Oreo", "descricao": "Sorvete de baunilha com pedaços de Oreo e calda", "preco": 12.90 },
      { "id": 17, "nome": "McFlurry M&Ms", "descricao": "Sorvete de baunilha com M&Ms e calda de chocolate", "preco": 12.90 },
      { "id": 18, "nome": "Torta de Maçã", "descricao": "Clássica torta quente de maçã", "preco": 7.90 },
      { "id": 19, "nome": "Casquinha Baunilha", "descricao": "Casquinha de sorvete sabor baunilha", "preco": 4.50 },
      { "id": 20, "nome": "Casquinha Mista", "descricao": "Casquinha de sorvete baunilha e chocolate", "preco": 4.90 },
      { "id": 21, "nome": "Sunday Chocolate", "descricao": "Sorvete de baunilha com calda de chocolate", "preco": 8.90 },
      { "id": 22, "nome": "Sunday Morango", "descricao": "Sorvete de baunilha com calda de morango", "preco": 8.90 }
    ],
    "Bebidas": [
      { "id": 23, "nome": "Coca-Cola 300ml", "descricao": "Refrigerante Coca-Cola gelado", "preco": 6.90 },
      { "id": 24, "nome": "Coca-Cola 500ml", "descricao": "Refrigerante Coca-Cola gelado", "preco": 8.90 },
      { "id": 25, "nome": "Fanta Laranja 300ml", "descricao": "Refrigerante Fanta sabor laranja", "preco": 6.90 },
      { "id": 26, "nome": "Sprite 500ml", "descricao": "Refrigerante Sprite sabor limão", "preco": 8.90 },
      { "id": 27, "nome": "Água Mineral", "descricao": "Água mineral sem gás", "preco": 5.50 },
      { "id": 28, "nome": "Suco de Laranja", "descricao": "Suco natural de laranja 300ml", "preco": 7.90 },
      { "id": 29, "nome": "Café Expresso", "descricao": "Café expresso curto", "preco": 4.90 },
      { "id": 30, "nome": "Capuccino", "descricao": "Café expresso com leite vaporizado e espuma cremosa", "preco": 8.50 }
    ]
  }
}
"""

# Salva o conteúdo em um arquivo para o script poder ler
nome_arquivo = 'cardapio.json'
with open(nome_arquivo, 'w', encoding='utf-8') as f:
    f.write(cardapio_json_string)

print(f"Arquivo '{nome_arquivo}' criado com sucesso.")


# 3. Função para carregar e preparar os dados
def carregar_e_preparar_cardapio(caminho_arquivo):
    """
    Carrega o cardápio de um arquivo JSON e o formata em uma lista de strings.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    documentos_formatados = []
    # Acessa o dicionário principal que contém as categorias
    menu = dados['McDonalds_Menu']

    # Itera sobre cada categoria (ex: "Sanduiches") e a lista de itens
    for categoria, itens in menu.items():
        for item in itens:
            # Cria um texto bem formatado para cada item do cardápio
            texto_item = (
                f"Categoria: {categoria}\n"
                f"Nome: {item['nome']}\n"
                f"Descrição: {item['descricao']}\n"
                f"Preço: R$ {item['preco']:.2f}"
            )
            documentos_formatados.append(texto_item)
    
    return documentos_formatados


# 4. Execução e Verificação
# Chamamos a função e guardamos o resultado na variável 'documentos'
documentos = carregar_e_preparar_cardapio(nome_arquivo)

print("\n--- Processamento concluído! ---")