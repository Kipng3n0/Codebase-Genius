"""CodeAnalyzer Agent - Analyzes code structure and builds code context graph"""

# Node representing a code element (class, function, etc.)
node CodeElement {
    has name: str;
    has type: str;  # "class", "function", "module"
    has file_path: str;
    has line_number: int = 0;
    has docstring: str = "";
    has parameters: list = [];
    has return_type: str = "";
}

# Edge representing relationships between code elements
edge Calls {
    has call_type: str;  # "calls", "inherits", "imports"
}

# Walker to analyze Python files
walker analyze_python_file {
    has file_path: str;
    has classes: list = [];
    has functions: list = [];
    has imports: list = [];
    
    can parse_file with `root entry {
        try {
            with open(self.file_path, "r", encoding="utf-8") as f {
                content = f.read();
                tree = ast.parse(content);
                
                # Extract classes
                for node in ast.walk(tree) {
                    if isinstance(node, ast.ClassDef) {
                        self.classes.append({
                            "name": node.name,
                            "line": node.lineno,
                            "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                            "bases": [b.id if isinstance(b, ast.Name) else str(b) for b in node.bases],
                            "docstring": ast.get_docstring(node) or ""
                        });
                    } elif isinstance(node, ast.FunctionDef) {
                        # Only top-level functions
                        if node.col_offset == 0 {
                            self.functions.append({
                                "name": node.name,
                                "line": node.lineno,
                                "args": [arg.arg for arg in node.args.args],
                                "docstring": ast.get_docstring(node) or ""
                            });
                        }
                    } elif isinstance(node, ast.Import) {
                        for alias in node.names {
                            self.imports.append({"module": alias.name, "alias": alias.asname});
                        }
                    } elif isinstance(node, ast.ImportFrom) {
                        module = node.module or "";
                        for alias in node.names {
                            self.imports.append({"from": module, "import": alias.name, "alias": alias.asname});
                        }
                    }
                }
            }
            print(f"Analyzed {self.file_path}: {len(self.classes)} classes, {len(self.functions)} functions");
        } except Exception as e {
            print(f"Error analyzing {self.file_path}: {str(e)}");
        }
        
        report {
            "classes": self.classes,
            "functions": self.functions,
            "imports": self.imports
        };
    }
}

# Walker to analyze entire repository
walker analyze_repository {
    has repo_path: str;
    has file_tree: dict;
    has analysis_result: dict = {};
    
    can analyze_all with `root entry {
        self.analysis_result = {
            "modules": [],
            "classes": [],
            "functions": [],
            "imports": [],
            "relationships": []
        };
        
        def process_tree(tree: dict) {
            if tree.get("type") == "file" {
                file_path = tree.get("path", "");
                extension = tree.get("extension", "");
                
                if extension == ".py" {
                    # Analyze Python file
                    analyzer = analyze_python_file(file_path=file_path);
                    result = root spawn analyzer;
                    
                    if result {
                        self.analysis_result["classes"].extend(result.get("classes", []));
                        self.analysis_result["functions"].extend(result.get("functions", []));
                        self.analysis_result["imports"].extend(result.get("imports", []));
                        self.analysis_result["modules"].append({
                            "path": file_path,
                            "name": os.path.basename(file_path)
                        });
                    }
                }
            } elif tree.get("type") == "directory" {
                for child in tree.get("children", []) {
                    process_tree(child);
                }
            }
        }
        
        process_tree(self.file_tree);
        
        # Build relationships
        self.analysis_result["relationships"] = self.build_relationships();
        
        print(f"Analysis complete: {len(self.analysis_result['classes'])} classes, {len(self.analysis_result['functions'])} functions");
        
        report {"analysis": self.analysis_result};
    }
    
    can build_relationships with `root entry {
        relationships = [];
        
        # Build inheritance relationships
        for cls in self.analysis_result.get("classes", []) {
            for base in cls.get("bases", []) {
                relationships.append({
                    "from": cls["name"],
                    "to": base,
                    "type": "inherits"
                });
            }
        }
        
        report {"relationships": relationships};
    }
}