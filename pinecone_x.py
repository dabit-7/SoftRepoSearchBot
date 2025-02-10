# pinecone_handler.py
import subprocess
import json
from pinecone import Pinecone, ServerlessSpec
from config import API_KEY, INDEX_NAME

# Inicialização do Pinecone
pinecone = Pinecone(api_key=API_KEY)

# Criar ou conectar ao índice
def criar_ou_conectar_indice():
    # Se o índice não existir, cria
    if INDEX_NAME not in pinecone.list_indexes().names():
        pinecone.create_index(
            name=INDEX_NAME,
            dimension=384,  # Dimensão do modelo "paraphrase-MiniLM-L6-v2"
            metric='cosine',
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        print(f"Índice '{INDEX_NAME}' criado com sucesso!")
    
    # Conecta ao índice existente
    index = pinecone.Index(INDEX_NAME)
    print(f"Conectado ao índice: {INDEX_NAME}")
    return index

# Função para gerar embeddings usando o Ollama
def gerar_embeddings_ollama(textos):
    try:
        # Aqui, se você estiver chamando o Ollama via subprocess, imprime a resposta
        result = subprocess.run(['ollama', 'embed', '--text', '\n'.join(textos)], capture_output=True, text=True)

        print(f"Resposta do Ollama: {result.stdout}")  # Imprime a resposta para debug

        # Agora tenta carregar como JSON
        embeddings_json = json.loads(result.stdout)
        embeddings = embeddings_json.get("embeddings", [])
        return embeddings
    except Exception as e:
        print(f"Erro ao gerar embeddings: {e}")
        return []


# Função para inserir dados no Pinecone
def inserir_dados_pinecone(index, textos, metadados=None):
    embeddings = gerar_embeddings_ollama(textos)
    if not embeddings:
        print("Nenhum embedding gerado.")
        return

    items = []
    for i, embedding in enumerate(embeddings):
        item = {
            "id": f"doc-{i}",
            "values": embedding,
            "metadata": metadados[i] if metadados else {}
        }
        items.append(item)

    # Depuração: Verifique os dados antes de enviar para Pinecone
    print(f"Itens a serem inseridos no Pinecone: {items}")

    try:
        index.upsert(items)
        print(f"Inseridos {len(items)} itens no índice.")
    except Exception as e:
        print(f"Erro ao inserir no Pinecone: {e}")

    
# Função para consulta no Pinecone
def consultar_pinecone(index, consulta, top_k=3):
    consulta_embedding = gerar_embeddings_ollama([consulta])[0]
    resultados = index.query(vector=consulta_embedding, top_k=top_k, include_metadata=True)
    
    print("Resultados encontrados:")
    for match in resultados['matches']:
        print(f"ID: {match['id']}, Similaridade: {match['score']}, Metadados: {match['metadata']}")
