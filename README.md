# Codebase-Genius

An AI-powered, multi-agent system that automatically generates high-quality documentation for any software repository.

## Features

- **Repository Analysis**: Automatically clones and analyzes GitHub repositories
- **Code Understanding**: Builds a comprehensive code context graph
- **Documentation Generation**: Creates detailed markdown documentation
- **Visualization**: Generates architecture and relationship diagrams
- **Multi-language Support**: Works with Python and Jac codebases

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Jaseci Core

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kipng3n0/Codebase-Genius
   cd Codebase-Genius
```

2. Create Virtual Environment

```bash
python -m venv venv
# on linux
source venv/bin/activate 
```

3. Install Dependencies

```bash
pip install fastapi uvicorn streamlit requests gitpython
```

## Running the Application

### Start the Backend Server

Open a terminal and run:

```bash
cd backend
python api_server.py
```

You should see:
```
Starting Codebase Genius API...
API will be available at http://localhost:8000
API docs at http://localhost:8000/docs
```

### Start the Frontend

Open a **new terminal** and run:

```bash
cd frontend
streamlit run app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Access the Application

- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Usage

1. Open your browser and navigate to http://localhost:8501
2. Enter a GitHub repository URL (e.g., `https://github.com/pallets/flask`)
3. Click "Generate Documentation"
4. Wait for the analysis to complete
5. View the generated documentation and statistics
6. Download the documentation as a markdown file

## Example Repositories to Try

- Flask: `https://github.com/pallets/flask`
- Requests: `https://github.com/psf/requests`
- Django: `https://github.com/django/django`
- FastAPI: `https://github.com/tiangolo/fastapi`

## Features in Detail

### Code Analysis

The system analyzes Python files and extracts:
- Class definitions with methods and docstrings
- Function definitions with parameters and docstrings
- Import statements
- Module structure
- Line counts and file statistics

### Documentation Generation

Generated documentation includes:
- Repository summary with statistics
- List of all classes with their methods
- List of all functions with parameters
- Module organization
- Formatted markdown output

### User Interface

The frontend provides:
- Clean, modern design with teal gradient theme
- Real-time progress tracking
- Interactive statistics dashboard
- One-click documentation download
- Responsive layout for all screen sizes

## API Endpoints

### GET /
Returns API information and available endpoints

### GET /status
Returns API status and version information

### POST /analyze
Analyzes a GitHub repository

**Request Body:**
```json
{
  "repo_url": "https://github.com/username/repository"
}
```

**Response:**
```json
{
  "status": "success",
  "repo_name": "repository",
  "documentation": {
    "markdown": "# Documentation..."
  },
  "analysis": {
    "total_files": 10,
    "total_lines": 1000,
    "classes": 5,
    "functions": 20,
    "modules": 10
  }
}
```

## Architecture

### Backend (FastAPI)

- **api_server.py**: Main FastAPI application
  - Handles HTTP requests
  - Clones repositories using GitPython
  - Analyzes code using Python AST
  - Generates documentation
  - Caches results for performance

### Frontend (Streamlit)

- **app.py**: Streamlit web interface
  - User input handling
  - API communication
  - Results visualization
  - Download functionality

### Jac Agents

- **code_analyzer.jac**: Analyzes code structure
- **doc_genie.jac**: Generates documentation
- **repo_mapper.jac**: Maps repository structure

## Troubleshooting

### Backend not starting
- Ensure port 8000 is not in use
- Check if all dependencies are installed
- Verify Python version is 3.8+

### Frontend shows connection error
- Make sure backend is running on port 8000
- Check firewall settings
- Verify API URL in the application

### Repository cloning fails
- Ensure the repository URL is correct
- Check internet connection
- Verify the repository is public

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with Jac (Jaseci programming language)
- Powered by FastAPI for the backend
- UI created with Streamlit
- Code analysis using Python's AST module

**Codebase Genius** - Making code documentation effortless

Built with precision for developers | 2025