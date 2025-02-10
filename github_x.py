import requests

def fetch_repo_data(repo_url):
    # Extrair o nome do repositório da URL
    try:
        # Remover parte do caminho para pegar apenas o repositório
        repo_name = repo_url.split("github.com/")[1].split("?")[0]  # Pega tudo até o ? (se houver)
        owner, repo = repo_name.split("/")[:2]  # Garante que só pega os dois primeiros valores
        
        # API do GitHub para obter informações do repositório
        commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        issues_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        
        commits = requests.get(commits_url).json()
        issues = requests.get(issues_url).json()
        
        return commits, issues
    
    except IndexError as e:
        print(f"Erro ao processar a URL do repositório: {repo_url}")
        return [], []

