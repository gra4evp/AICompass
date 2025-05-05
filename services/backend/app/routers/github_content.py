from fastapi import APIRouter, HTTPException
import requests
import markdown2

router = APIRouter(prefix="/github", tags=["GitHub"])

def get_github_raw_url(repo_url: str, path: str) -> str:
    """Convert GitHub repository URL to raw content URL"""
    # Convert from https://github.com/username/repo/tree/branch/path
    # to https://raw.githubusercontent.com/username/repo/branch/path
    parts = repo_url.split('/')
    if 'github.com' not in parts:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")
    
    # Find the index of 'github.com'
    github_index = parts.index('github.com')
    
    # Get username and repo
    username = parts[github_index + 1]
    repo = parts[github_index + 2]
    
    # Get branch (default to 'main' if not specified)
    branch = 'main'
    if 'tree' in parts:
        tree_index = parts.index('tree')
        if tree_index + 1 < len(parts):
            branch = parts[tree_index + 1]
    
    # Construct raw URL
    return f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/{path}"

@router.get("/content")
async def get_github_content(repo_url: str, path: str):
    try:
        raw_url = get_github_raw_url(repo_url, path)
        response = requests.get(raw_url)
        response.raise_for_status()
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(response.text)
        
        return {
            "content": html_content,
            "raw_url": raw_url
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=404, detail=f"Could not fetch content: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}") 