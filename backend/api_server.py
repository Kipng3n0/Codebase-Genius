"""FastAPI server to expose Jac walkers as REST API endpoints"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
import tempfile
import git
import ast
from typing import Optional, Dict

app = FastAPI(
    title="Codebase Genius API",
    description="AI-powered code documentation generator",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for analysis results
analysis_cache = {}

class AnalyzeRequest(BaseModel):
    repo_url: str
    output_dir: Optional[str] = "./outputs"


def clone_repository(repo_url: str, target_dir: str) -> str:
    """Clone a GitHub repository"""
    repo_name = repo_url.rstrip('/').split('/')[-1].replace('.git', '')
    repo_path = os.path.join(target_dir, repo_name)
    
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    
    git.Repo.clone_from(repo_url, repo_path)
    return repo_path


def analyze_python_file(file_path: str) -> Dict:
    """Analyze a Python file and extract classes, functions, imports"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tree = ast.parse(content)
            
        classes = []
        functions = []
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes.append({
                    "name": node.name,
                    "line": node.lineno,
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    "docstring": ast.get_docstring(node) or ""
                })
            elif isinstance(node, ast.FunctionDef) and node.col_offset == 0:
                functions.append({
                    "name": node.name,
                    "line": node.lineno,
                    "args": [arg.arg for arg in node.args.args],
                    "docstring": ast.get_docstring(node) or ""
                })
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "alias": alias.asname})
        
        return {"classes": classes, "functions": functions, "imports": imports}
    except Exception as e:
        return {"classes": [], "functions": [], "imports": [], "error": str(e)}


def build_file_tree(path: str, ignored_dirs=None) -> Dict:
    """Build a file tree structure"""
    if ignored_dirs is None:
        ignored_dirs = ['.git', 'node_modules', '__pycache__', 'venv', '.venv', 'build', 'dist']
    
    tree = {"name": os.path.basename(path), "type": "directory", "children": []}
    
    try:
        items = sorted(os.listdir(path))
        for item in items:
            if item in ignored_dirs or item.startswith('.'):
                continue
            
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tree["children"].append(build_file_tree(item_path, ignored_dirs))
            else:
                tree["children"].append({
                    "name": item,
                    "type": "file",
                    "path": item_path,
                    "extension": os.path.splitext(item)[1]
                })
    except Exception:
        pass
    
    return tree


def analyze_repository_code(repo_path: str, file_tree: Dict) -> Dict:
    """Analyze all Python files in the repository"""
    analysis = {
        "modules": [],
        "classes": [],
        "functions": [],
        "imports": [],
        "total_files": 0,
        "total_lines": 0
    }
    
    def process_tree(tree: Dict):
        if tree.get("type") == "file" and tree.get("extension") == ".py":
            file_path = tree.get("path", "")
            result = analyze_python_file(file_path)
            
            analysis["classes"].extend(result.get("classes", []))
            analysis["functions"].extend(result.get("functions", []))
            analysis["imports"].extend(result.get("imports", []))
            analysis["modules"].append({"path": file_path, "name": os.path.basename(file_path)})
            analysis["total_files"] += 1
            
            try:
                with open(file_path, 'r') as f:
                    analysis["total_lines"] += len(f.readlines())
            except:
                pass
                
        elif tree.get("type") == "directory":
            for child in tree.get("children", []):
                process_tree(child)
    
    process_tree(file_tree)
    return analysis


def generate_documentation(repo_name: str, repo_url: str, analysis: Dict, file_tree: Dict) -> str:
    """Generate markdown documentation"""
    doc = f"# {repo_name}\n\n"
    doc += f"**Repository:** [{repo_url}]({repo_url})\n\n"
    doc += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    doc += "---\n\n"
    
    # Summary
    doc += "## Summary\n\n"
    doc += f"- **Total Files:** {analysis['total_files']}\n"
    doc += f"- **Total Lines:** {analysis['total_lines']}\n"
    doc += f"- **Classes:** {len(analysis['classes'])}\n"
    doc += f"- **Functions:** {len(analysis['functions'])}\n"
    doc += f"- **Modules:** {len(analysis['modules'])}\n\n"
    doc += "---\n\n"
    
    # Classes
    if analysis['classes']:
        doc += "## Classes\n\n"
        for cls in analysis['classes'][:10]:  # Limit to first 10
            doc += f"### `{cls['name']}`\n\n"
            if cls.get('docstring'):
                doc += f"{cls['docstring']}\n\n"
            if cls.get('methods'):
                doc += "**Methods:**\n"
                for method in cls['methods'][:5]:
                    doc += f"- `{method}()`\n"
                doc += "\n"
    
    # Functions
    if analysis['functions']:
        doc += "## Functions\n\n"
        for func in analysis['functions'][:10]:  # Limit to first 10
            args = ", ".join(func.get('args', []))
            doc += f"### `{func['name']}({args})`\n\n"
            if func.get('docstring'):
                doc += f"{func['docstring']}\n\n"
    
    return doc


@app.get("/")
async def root():
    return {
        "message": "Codebase Genius API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "/analyze": "POST - Analyze a repository",
            "/status": "GET - Check API status"
        }
    }


@app.get("/status")
async def get_status():
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "cached_analyses": len(analysis_cache)
    }


@app.post("/analyze")
async def analyze_repository(request: AnalyzeRequest):
    """Analyze a GitHub repository and generate documentation"""
    try:
        # Validate repo URL
        if not request.repo_url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Invalid repository URL")
        
        repo_name = request.repo_url.rstrip('/').split('/')[-1].replace('.git', '')
        
        # Check cache
        if request.repo_url in analysis_cache:
            return analysis_cache[request.repo_url]
        
        # Create temp directory for cloning
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Step 1: Clone repository
            print(f"Cloning {request.repo_url}...")
            repo_path = clone_repository(request.repo_url, temp_dir)
            
            # Step 2: Build file tree
            print("Building file tree...")
            file_tree = build_file_tree(repo_path)
            
            # Step 3: Analyze code
            print("Analyzing code...")
            analysis = analyze_repository_code(repo_path, file_tree)
            
            # Step 4: Generate documentation
            print("Generating documentation...")
            documentation = generate_documentation(repo_name, request.repo_url, analysis, file_tree)
            
            result = {
                "status": "success",
                "repo_url": request.repo_url,
                "repo_name": repo_name,
                "documentation": {
                    "markdown": documentation
                },
                "analysis": {
                    "total_files": analysis['total_files'],
                    "total_lines": analysis['total_lines'],
                    "classes": len(analysis['classes']),
                    "functions": len(analysis['functions']),
                    "modules": len(analysis['modules'])
                },
                "file_tree": file_tree
            }
            
            # Cache the result
            analysis_cache[request.repo_url] = result
            
            return result
            
        finally:
            # Cleanup temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except git.exc.GitCommandError as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    print("Starting Codebase Genius API...")
    print("API will be available at http://localhost:8000")
    print("API docs at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)