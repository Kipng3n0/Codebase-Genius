import streamlit as st
import requests
import time

st.set_page_config(page_title="Codebase Genius", page_icon=" ", layout="wide")

# Enhanced CSS with better visibility
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
    }
    
    /* Content area */
    .main .block-container {
        background: white;
        border-radius: 20px;
        padding: 3rem;
        margin-top: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Header */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        color: #0891b2;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .feature-text {
        font-size: 1.1rem;
        color: #2d3748;
        text-align: center;
        margin: 2rem 0;
        line-height: 1.8;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 50px;
        box-shadow: 0 8px 20px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 30px rgba(6, 182, 212, 0.6);
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        border-radius: 15px;
        border: 3px solid #e2e8f0;
        padding: 1rem;
        font-size: 1.1rem;
        color: #2d3748;
        background: #f7fafc;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #06b6d4;
        box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2);
        background: white;
    }
    
    /* Metrics */
    .stMetric {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stMetric label {
        color: #4a5568 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #0891b2 !important;
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06b6d4 0%, #0891b2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #06b6d4 0%, #0891b2 100%);
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: #f0fdf4;
        color: #166534;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #22c55e;
    }
    
    .stError {
        background: #fef2f2;
        color: #991b1b;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #ef4444;
    }
    
    /* Download button */
    .stDownloadButton>button {
        background: #22c55e;
        color: white;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
    }
    
    /* Section headers */
    h3 {
        color: #2d3748 !important;
        font-weight: 700 !important;
    }
    
    /* Markdown content styling */
    .main h1 {
        color: #1a202c !important;
    }
    
    .main h2 {
        color: #2d3748 !important;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
    }
    
    .main p {
        color: #1a202c !important;
    }
    
    .main a {
        color: #1a202c !important;
        text-decoration: underline;
    }
    
    .main a:hover {
        color: #2d3748 !important;
    }
    
    .main strong {
        color: #2d3748 !important;
    }
    
    .main li {
        color: #1a202c !important;
    }
    
    .main code {
        background: #f7fafc;
        color: #0891b2;
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("About")
    st.markdown("""
    ### Codebase Genius
    
    Transform any GitHub repository into comprehensive documentation with AI-powered analysis.
    
    **Features:**
    - Deep code analysis
    - Statistics & metrics
    - Auto-documentation
    - Downloadable reports
    - Lightning fast
    
    ---
    
    ### How It Works
    
    1. **Clone** - We fetch your repository
    2. **Analyze** - AI scans the codebase
    3. **Generate** - Creates beautiful docs
    4. **Download** - Get your documentation
    
    ---
    
    ### Supported
    - Python projects
    - Public repositories
    - No authentication needed
    
    ---
    
    **Made with Precision**
    
    Powered by Jac, FastAPI & Streamlit
    """)
    
    # Hidden API URL (hardcoded)
    api_url = "http://localhost:8000"
    
    st.markdown("---")
    if st.button("Check API Status", use_container_width=True):
        try:
            r = requests.get(f"{api_url}/status", timeout=5)
            if r.status_code == 200:
                st.success("API Online")
                st.json(r.json())
        except:
            st.error("Connection failed")

# Main content
st.markdown('<h1 class="main-header">Codebase Genius</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Code Documentation Generator</p>', unsafe_allow_html=True)

st.markdown('<p class="feature-text">Instantly analyze and document any GitHub repository with advanced AI technology. Get comprehensive insights into code structure, classes, functions, and more - all in seconds!</p>', unsafe_allow_html=True)

st.markdown("---")

# Input section with better spacing
st.markdown("### Enter Repository URL")
st.markdown("<p style='color: #4a5568; margin-bottom: 1rem;'>Paste any public GitHub repository URL below to get started</p>", unsafe_allow_html=True)

repo_url = st.text_input(
    "Repository URL",
    placeholder="https://github.com/username/repository",
    label_visibility="collapsed"
)

# Example repositories
st.markdown("<p style='color: #718096; font-size: 0.9rem; margin-top: 0.5rem;'>Try examples: <code>https://github.com/pallets/flask</code> or <code>https://github.com/psf/requests</code></p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Generate Documentation", type="primary", use_container_width=True):
    if not repo_url:
        st.error("Please enter a repository URL")
    else:
        progress = st.progress(0)
        status = st.empty()
        
        try:
            status.markdown("### Cloning repository...")
            status.caption("This may take a few minutes for large repositories")
            progress.progress(20)
            
            # Increased timeout for large repositories like Flask
            response = requests.post(f"{api_url}/analyze", json={"repo_url": repo_url}, timeout=300)
            
            status.markdown("### Analyzing code...")
            status.caption("Processing files and generating documentation...")
            progress.progress(80)
            time.sleep(0.3)
            
            if response.status_code == 200:
                result = response.json()
                progress.progress(100)
                status.empty()
                progress.empty()
                
                st.success(f"Successfully analyzed **{result.get('repo_name')}**!")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("### Analysis Summary")
                st.markdown("<p style='color: #4a5568; margin-bottom: 1.5rem;'>Here's what we found in your repository:</p>", unsafe_allow_html=True)
                analysis = result.get('analysis', {})
                
                col1, col2, col3, col4, col5 = st.columns(5)
                col1.metric("Files", analysis.get('total_files', 0))
                col2.metric("Lines", f"{analysis.get('total_lines', 0):,}")
                col3.metric("Classes", analysis.get('classes', 0))
                col4.metric("Functions", analysis.get('functions', 0))
                col5.metric("Modules", analysis.get('modules', 0))
                
                st.markdown("---")
                st.markdown("### Generated Documentation")
                st.markdown("<p style='color: #4a5568; margin-bottom: 1rem;'>Your comprehensive documentation is ready! Download it or view it below.</p>", unsafe_allow_html=True)
                
                doc = result.get("documentation", {}).get("markdown", "")
                
                col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
                with col_dl2:
                    st.download_button(
                        "Download Documentation",
                        doc,
                        file_name=f"{result.get('repo_name')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Display documentation in a nice container
                with st.container():
                    st.markdown(doc)
            else:
                st.error(f"Error: {response.json().get('detail')}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
        finally:
            progress.empty()
            status.empty()

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <p style='color: #4a5568; font-size: 1.1rem; margin-bottom: 0.5rem;'>
            <strong>Codebase Genius</strong> - Making code documentation effortless
        </p>
        <p style='color: #718096; font-size: 0.9rem;'>
            Powered by <strong>Jac</strong>, <strong>FastAPI</strong> & <strong>Streamlit</strong>
        </p>
        <p style='color: #a0aec0; font-size: 0.8rem; margin-top: 1rem;'>
            © 2025 Codebase Genius | Built with precision for developers
        </p>
    </div>
""", unsafe_allow_html=True)