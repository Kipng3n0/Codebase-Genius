"""DocGenie Agent - Generates markdown documentation from analysis results"""

# Walker to generate documentation
walker generate_documentation {
    has repo_url: str;
    has repo_path: str;
    has file_tree: dict;
    has readme_summary: str;
    has analysis: dict;
    has output_path: str = "./outputs";
    has documentation: str = "";
    
    can generate with `root entry {
        print("Generating documentation...");
        
        # Build markdown document
        md_content = [];
        
        # Header
        md_content.append(f"# Documentation for {os.path.basename(self.repo_path)}");
        md_content.append("");
        md_content.append(f"**Generated on:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}");
        md_content.append(f"**Repository:** {self.repo_url}");
        md_content.append("");
        md_content.append("---");
        md_content.append("");
        
        # Table of Contents
        md_content.append("## Table of Contents");
        md_content.append("");
        md_content.append("1. [Project Overview](#project-overview)");
        md_content.append("2. [Repository Structure](#repository-structure)");
        md_content.append("3. [Code Analysis](#code-analysis)");
        md_content.append("4. [API Reference](#api-reference)");
        md_content.append("");
        md_content.append("---");
        md_content.append("");
        
        # Project Overview
        md_content.append("## Project Overview");
        md_content.append("");
        md_content.append(self.readme_summary if self.readme_summary else "No README found.");
        md_content.append("");
        md_content.append("---");
        md_content.append("");
        
        # Repository Structure
        md_content.append("## Repository Structure");
        md_content.append("");
        md_content.append("```");
        md_content.append(self.format_tree(self.file_tree));
        md_content.append("```");
        md_content.append("");
        md_content.append("---");
        md_content.append("");
        
        # Code Analysis
        md_content.append("## Code Analysis");
        md_content.append("");
        
        classes = self.analysis.get("classes", []);
        functions = self.analysis.get("functions", []);
        modules = self.analysis.get("modules", []);
        
        md_content.append(f"**Total Modules:** {len(modules)}");
        md_content.append(f"**Total Classes:** {len(classes)}");
        md_content.append(f"**Total Functions:** {len(functions)}");
        md_content.append("");
        
        # Classes
        if classes {
            md_content.append("### Classes");
            md_content.append("");
            for cls in classes {
                md_content.append(f"#### `{cls['name']}`");
                md_content.append("");
                if cls.get("docstring") {
                    md_content.append(cls["docstring"]);
                    md_content.append("");
                }
                if cls.get("methods") {
                    md_content.append("**Methods:**");
                    for method in cls["methods"] {
                        md_content.append(f"- `{method}()`");
                    }
                    md_content.append("");
                }
                if cls.get("bases") {
                    md_content.append(f"**Inherits from:** {', '.join(cls['bases'])}");
                    md_content.append("");
                }
            }
        }
        
        # Functions
        if functions {
            md_content.append("### Functions");
            md_content.append("");
            for func in functions {
                args = ", ".join(func.get("args", []));
                md_content.append(f"#### `{func['name']}({args})`");
                md_content.append("");
                if func.get("docstring") {
                    md_content.append(func["docstring"]);
                    md_content.append("");
                }
            }
        }
        
        md_content.append("---");
        md_content.append("");
        
        # API Reference
        md_content.append("## API Reference");
        md_content.append("");
        md_content.append("This section contains detailed API documentation.");
        md_content.append("");
        
        # Join all content
        self.documentation = "\n".join(md_content);
        
        # Save to file
        self.save_documentation();
        
        print("Documentation generated successfully!");
        report {"documentation": self.documentation, "output_path": self.output_path};
    }
    
    can format_tree(tree: dict, prefix: str = "", is_last: bool = True) -> str {
        result = [];
        
        if tree.get("type") == "directory" {
            result.append(f"{prefix}{'└── ' if is_last else '├── '}{tree['name']}/");
            children = tree.get("children", []);
            for i, child in enumerate(children) {
                is_last_child = (i == len(children) - 1);
                new_prefix = prefix + ("    " if is_last else "│   ");
                result.append(self.format_tree(child, new_prefix, is_last_child));
            }
        } else {
            result.append(f"{prefix}{'└── ' if is_last else '├── '}{tree.get('name', '')}");
        }
        
        return "\n".join(result);
    }
    
    can save_documentation {
        try {
            # Create output directory
            repo_name = os.path.basename(self.repo_path);
            output_dir = os.path.join(self.output_path, repo_name);
            os.makedirs(output_dir, exist_ok=True);
            
            # Save markdown file
            doc_file = os.path.join(output_dir, "documentation.md");
            with open(doc_file, "w", encoding="utf-8") as f {
                f.write(self.documentation);
            }
            
            self.output_path = doc_file;
            print(f"Documentation saved to {doc_file}");
        } except Exception as e {
            print(f"Error saving documentation: {str(e)}");
        }
    }
}