# **SoftRepoSearchBot**  
Projeto de Chatbot que pesquisa em repositórios do GITHUB  

### **Requisitos Principais:**  
Free tier do Banco de Dados Vetorial Pinecode (Chave de API)  
Ollama instalado Localmente  

###  **Demais Requisitos**  
accelerate==1.3.0  
certifi==2024.12.14  
charset-normalizer==3.4.1  
colorama==0.4.6  
filelock==3.17.0  
fsspec==2024.12.0  
huggingface-hub==0.27.1  
idna==3.10  
Jinja2==3.1.5  
joblib==1.4.2  
MarkupSafe==3.0.2  
mpmath==1.3.0  
networkx==3.4.2  
numpy==2.2.2  
packaging==24.2  
pillow==11.1.0  
pinecone-client==5.0.1  
pinecone-plugin-inference==1.1.0  
pinecone-plugin-interface==0.0.7  
psutil==6.1.1  
PyYAML==6.0.2  
regex==2024.11.6  
requests==2.32.3  
safetensors==0.5.2  
scikit-learn==1.6.1  
scipy==1.15.1  
sentence-transformers==3.4.0  
setuptools==75.8.0  
sympy==1.13.1  
threadpoolctl==3.5.0  
tokenizers==0.21.0  
torch==2.5.1  
tqdm==4.67.1  
transformers==4.48.1  
typing_extensions==4.12.2  
urllib3==2.3.0  

<br>

### **Funcionamento do Código**

O código **`main.py`** é o ponto de entrada do chatbot para consulta de repositórios do GitHub. Ele realiza três principais tarefas:

1. **Obtém dados do repositório GitHub** (commits e issues).  
2. **Armazena esses dados no Pinecone** (banco vetorial).  
3. **Responde perguntas do usuário sobre o repositório**, recuperando informações relevantes do Pinecone.  

Partes:

---

### **1️⃣ Importação dos Módulos**
```python
from github_x import fetch_repo_data
from pinecone_x import criar_ou_conectar_indice, inserir_dados_pinecone, consultar_pinecone
from config import INDEX_NAME
```
- **`github_x`**: Possui a função `fetch_repo_data()` para buscar informações do repositório (commits e issues).  
- **`pinecone_x`**: Contém funções para interagir com o Pinecone:
  - `criar_ou_conectar_indice()` → Inicializa ou conecta ao banco de dados vetorial.  
  - `inserir_dados_pinecone()` → Insere os dados no Pinecone.  
  - `consultar_pinecone()` → Faz uma consulta ao Pinecone com a pergunta do usuário.  
- **`config`**: Armazena configurações como `INDEX_NAME`, que define o nome do índice no Pinecone.

---

### **2️⃣ Função `user_interface()`**
```python
def user_interface():
    print("Bem-vindo ao chatbot de repositório de software!")
    repo_url = input("Digite a URL do repositório: ")
    question = input("Digite sua pergunta sobre o repositório: ")
    return repo_url, question
```
- Exibe uma mensagem de boas-vindas.  
- Solicita ao usuário uma **URL do repositório** e uma **pergunta**.  
- Retorna esses valores para serem usados no fluxo principal.  

---

### **3️⃣ Função `main()`**
```python
def main():
    # Conectar ao Pinecone
    index = criar_ou_conectar_indice()
```
- **Conecta-se ao Pinecone** (cria um índice se não existir).

```python
    # Obter URL do repositório e a pergunta
    repo_url, question = user_interface()
```
- **Pede ao usuário** a URL do repositório e a pergunta.

```python
    # Buscar dados do repositório no GitHub
    commits, issues = fetch_repo_data(repo_url)
```
- **Baixa dados do repositório** usando `fetch_repo_data(repo_url)`.  
- Retorna **commits** e **issues**.

```python
    # Inserir os dados no Pinecone
    textos = [commit['commit']['message'] for commit in commits] + [issue['title'] for issue in issues]
    metadados = [{"type": "commit"} for _ in commits] + [{"type": "issue"} for _ in issues]
    inserir_dados_pinecone(index, textos, metadados)
```
- **Prepara os dados** para inserção no Pinecone:  
  - Extrai **mensagens de commit** e **títulos de issues**.  
  - Associa **metadados** (`commit` ou `issue`).  
  - Envia os dados para o Pinecone (`inserir_dados_pinecone`).

```python
    # Realizar a consulta
    consultar_pinecone(index, question)
```
- **Faz a consulta no Pinecone** usando a pergunta do usuário.

---

### **4️⃣ Execução do Script**
```python
if __name__ == "__main__":
    main()
```
- **Executa `main()` automaticamente** se o script for rodado diretamente (`python main.py`).

---

### **🔍 Resumo do Fluxo**
1. Conecta-se ao **Pinecone**.  
2. Obtém a **URL do repositório e a pergunta do usuário**.  
3. Busca **commits e issues no GitHub**.  
4. **Armazena os dados no Pinecone**.  
5. **Consulta o Pinecone** e responde à pergunta.  

O código permite transformar um repositório GitHub em uma **base de conhecimento consultável** com Pinecone e embeddings.
