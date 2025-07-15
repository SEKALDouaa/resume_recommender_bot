import requests 
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

headers = {
    "Authorization" : f"token {GITHUB_TOKEN}",
    "Accept" : "application/vnd.github.v3+json"
}

def search_resumes(query, per_page=10):
    url = "https://api.github.com/search/code"
    params = {
        "q": query,
        "per_page": per_page
    }
    response = requests.get(url, headers= headers, params=params)
    response.raise_for_status() # we use it to raise an error if the request fails
    return response.json()

def get_default_branch(repo_full_name):
    url = f"https://api.github.com/repos/{repo_full_name}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    repo_info = response.json()
    return repo_info.get("default_branch", "main")  # fallback to 'main'

def download_resume(repo_full_name, file_path,save_dir= "./resumes"):
    branch = get_default_branch(repo_full_name)
    url = f"https://raw.githubusercontent.com/{repo_full_name}/{branch}/{file_path}"    
    response = requests.get(url)
    response.raise_for_status()
    os.makedirs(save_dir, exist_ok=True)
    filename = os.path.join(save_dir, os.path.basename(file_path))
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded {filename}")

def main():
    query = "filename:cv.pdf"
    results = search_resumes(query)
    items = results.get('items', [])
    for item in items:
        repo = item["repository"]["full_name"]
        file_path = item["path"]
        print(f"Found resume in {repo}: {file_path}")
        if file_path.lower().endswith(".pdf"):
            download_resume(repo, file_path)
        else:
            print(f"Skipping non-pdf file: {file_path}")

if __name__== "__main__":
    main()