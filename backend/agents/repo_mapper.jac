"""RepoMapper Agent - Handles repository cloning and file tree generation"""

# Walker to clone a GitHub repository
walker clone_repository {
    has repo_url: str;
    has target_dir: str = "./temp_repos";
    has repo_path: str = "";
    has success: bool = False;
    
    can clone with `root entry {
        try {
            # Extract repo name from URL
            repo_name = self.repo_url.split("/")[-1].replace(".git", "");
            self.repo_path = os.path.join(self.target_dir, repo_name);
            
            # Create target directory if it doesn't exist
            os.makedirs(self.target_dir, exist_ok=True);
            
            # Clone the repository
            print(f"Cloning {self.repo_url} to {self.repo_path}...");
            git.Repo.clone_from(self.repo_url, self.repo_path);
            
            self.success = True;
            print(f"Successfully cloned to {self.repo_path}");
        } except Exception as e {
            print(f"Error cloning repository: {str(e)}");
            self.success = False;
        }
        
        report {
            "success": self.success,
            "repo_path": self.repo_path
        };
    }
}

# Walker to generate file tree structure
walker generate_file_tree {
    has repo_path: str;
    has file_tree: dict = {};
    has ignored_dirs: list = [".git", "node_modules", "__pycache__", "venv", ".venv", "build", "dist"];
    
    can build_tree with `root entry {
        def traverse_directory(path: str, prefix: str = "") -> dict {
            tree = {"name": os.path.basename(path), "type": "directory", "children": []};
            
            try {
                items = sorted(os.listdir(path));
                for item in items {
                    if item in self.ignored_dirs or item.startswith(".") {
                        continue;
                    }
                    
                    item_path = os.path.join(path, item);
                    if os.path.isdir(item_path) {
                        tree["children"].append(traverse_directory(item_path, prefix + "  "));
                    } else {
                        tree["children"].append({
                            "name": item,
                            "type": "file",
                            "path": item_path,
                            "extension": os.path.splitext(item)[1]
                        });
                    }
                }
            } except Exception as e {
                print(f"Error traversing {path}: {str(e)}");
            }
            
            return tree;
        }
        
        self.file_tree = traverse_directory(self.repo_path);
        print(f"Generated file tree for {self.repo_path}");
        
        report {"file_tree": self.file_tree};
    }
}

# Walker to summarize README
walker summarize_readme {
    has repo_path: str;
    has summary: str = "";
    
    can read_readme with `root entry {
        readme_files = ["README.md", "README.txt", "README", "readme.md"];
        
        for readme_file in readme_files {
            readme_path = os.path.join(self.repo_path, readme_file);
            if os.path.exists(readme_path) {
                try {
                    with open(readme_path, "r", encoding="utf-8") as f {
                        content = f.read();
                        # Take first 500 characters as summary
                        self.summary = content[:500] + "..." if len(content) > 500 else content;
                        print(f"Read README from {readme_path}");
                        break;
                    }
                } except Exception as e {
                    print(f"Error reading README: {str(e)}");
                }
            }
        }
        
        if not self.summary {
            self.summary = "No README found";
        }
        
        report {"summary": self.summary};
    }
}