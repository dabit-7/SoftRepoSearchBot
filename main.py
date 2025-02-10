# main.py
from github_x import fetch_repo_data
from pinecone_x import criar_ou_conectar_indice, inserir_dados_pinecone, consultar_pinecone
from config import INDEX_NAME

def user_interface():
    print("Bem-vindo ao chatbot de repositório de software!")
    repo_url = input("Digite a URL do repositório: ")
    question = input("Digite sua pergunta sobre o repositório: ")
    return repo_url, question

def main():
    # Conectar ao Pinecone
    index = criar_ou_conectar_indice()

    # Obter URL do repositório e a pergunta
    repo_url, question = user_interface()
    
    # Buscar dados do repositório no GitHub
    commits, issues = fetch_repo_data(repo_url)
    
    # Inserir os dados no Pinecone
    textos = [commit['commit']['message'] for commit in commits] + [issue['title'] for issue in issues]
    metadados = [{"type": "commit"} for _ in commits] + [{"type": "issue"} for _ in issues]
    inserir_dados_pinecone(index, textos, metadados)

    # Realizar a consulta
    consultar_pinecone(index, question)

if __name__ == "__main__":
    main()
