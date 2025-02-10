import os
from pinecone_x import Pinecone, ServerlessSpec
import requests


# Configuração da API Key e inicialização do Pinecone
api_key = "pcsk_67P5Ci_DWJy7BSmJTrttRFf5LxL22WHQD1BGMaWdTKoKuZkvuTDePYzxSagzVd2z1nm1Tj"
pinecone = Pinecone(api_key=api_key)

# Nome do índice
index_name = "chatbot-index"

# Excluir o índice existente se necessário
#if index_name in pinecone.list_indexes().names():
#    pinecone.delete_index(index_name)
#    print(f"Índice '{index_name}' excluído.")

# Criar um novo índice com a dimensão correta
pinecone.create_index(
    name=index_name,
    dimension=384,  # Dimensão do modelo "paraphrase-MiniLM-L6-v2"
    metric='cosine',
    spec=ServerlessSpec(cloud='aws', region='us-east-1')
)
print(f"Índice '{index_name}' criado com sucesso!")

# Conectar ao índice existente
index = pinecone.Index(index_name)  # Atualização aqui
print(f"Conectado ao índice: {index_name}")


from sentence_transformers import SentenceTransformer
# Carregue o modelo de embeddings
embedder = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Função para inserir dados no Pinecone
def inserir_dados_pinecone(textos, metadados=None):
    # Gere embeddings para os textos
    embeddings = embedder.encode(textos).tolist()

    # Prepare o formato para o Pinecone
    items = []
    for i, embedding in enumerate(embeddings):
        item = {
            "id": f"doc-{i}",
            "values": embedding,
            "metadata": metadados[i] if metadados else {}
        }
        items.append(item)

    # Insira no Pinecone
    index.upsert(items)
    print(f"Inseridos {len(items)} itens no índice.")

# Exemplo de textos a serem inseridos
textos = ["Mensagem de commit 1", "Mensagem de commit 2"]
metadados = [{"type": "commit"}, {"type": "issue"}]

# Inserir dados
inserir_dados_pinecone(textos, metadados)

# Função para consulta no Pinecone
def consultar_pinecone(consulta, top_k=3):
    # Gere o embedding da consulta
    consulta_embedding = embedder.encode([consulta])[0]  # Use [0] para acessar o vetor gerado

    # Converta o embedding para uma lista, pois o Pinecone não aceita ndarrays diretamente
    consulta_embedding = consulta_embedding.tolist()

    # Realize a busca no Pinecone
    resultados = index.query(vector=consulta_embedding, top_k=top_k, include_metadata=True)

    # Mostre os resultados
    print("Resultados encontrados:")
    for match in resultados['matches']:
        print(f"ID: {match['id']}, Similaridade: {match['score']}, Metadados: {match['metadata']}")


def user_interface():
    print("Bem-vindo ao chatbot de repositório de software!")
    repo_url = input("Digite a URL do repositório: ")
    question = input("Digite sua pergunta sobre o repositório: ")
    return repo_url, question




def fetch_repo_data(repo_url):
    # Extrair o nome do repositório da URL
    repo_name = repo_url.split("github.com/")[1]
    owner, repo = repo_name.split("/")
    
    # API do GitHub para obter informações do repositório
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    
    commits = requests.get(commits_url).json()
    issues = requests.get(issues_url).json()
    
    return commits, issues