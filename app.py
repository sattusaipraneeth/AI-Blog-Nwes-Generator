import streamlit as st
import urllib.request
import json
from io import StringIO
import requests
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Set OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key_here"

def fetch_ai_news(num_articles=10):
    """
    Fetches top AI news using the GNews API and returns a list of articles with their details.
    """
    api_key = "4e21d7361fdd189f4243c9df6725fb60"
    url = f"https://gnews.io/api/v4/search?q=artificial+intelligence&lang=en&country=us&max={num_articles}&sortby=publishedAt&apikey={api_key}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data.get("articles", [])
    except Exception as e:
        st.error(f"An error occurred while fetching AI news: {e}")
        return []

def scrape_content(url: str) -> str:
    """
    Scrapes the content of a given link using Jina AI.
    """
    try:
        response = requests.get("https://r.jina.ai/" + url)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Failed to fetch the content from {url}. Status code: {response.status_code}")
            return ""
    except Exception as e:
        st.error(f"An error occurred while scraping {url}: {e}")
        return ""

def generate_blog(content: str, title: str, instructions: str = "") -> str:
    """
    Generates a professional-quality blog based on the scraped content and user instructions.
    """
    system_prompt = """You are a professional blog writer specializing in creating detailed, insightful, and engaging blogs about AI and technology. 
    Follow these guidelines to create high-quality content:

    1. Structure:
       - Create an engaging title that captures attention
       - Write a compelling introduction that sets the context
       - Develop a well-organized main body with detailed analysis
       - Include practical implications and real-world applications
       - Conclude with key points and future outlook

    2. Style:
       - Maintain a professional yet conversational tone
       - Use clear paragraphs and transitions
       - Include relevant examples and case studies
       - Balance technical detail with accessibility
       - Incorporate industry insights and expert perspectives

    3. Technical Accuracy:
       - Verify technical concepts and terminology
       - Explain complex ideas clearly
       - Provide context for technical innovations
       - Include relevant statistics and data points
       - Reference key developments and trends

    4. Engagement:
       - Use engaging subheadings
       - Include relevant quotes when appropriate
       - Ask thought-provoking questions
       - Provide actionable insights
       - Create a narrative flow

    5. SEO Optimization:
       - Use relevant keywords naturally
       - Create scannable content with proper formatting
       - Include meta description suggestions
       - Structure headings hierarchically
       - Optimize for readability

    Ensure the content is:
    - Well-researched and accurate
    - Engaging and valuable to readers
    - Properly structured and formatted
    - Technical yet accessible
    - Original and insightful"""

    if instructions:
        system_prompt += f"\n\nAdditional instructions: {instructions}"

    chat = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Content: {content}\n\nGenerate a blog with title: {title}")
    ]
    response = chat(messages)
    return response.content

def modify_blog(blog_content: str, modification_instructions: str) -> str:
    """
    Modifies an existing blog based on user instructions while maintaining quality and coherence.
    """
    system_prompt = """    Modifies an existing blog based on user instructions while maintaining quality and coherence.
    Makes changes visibly apparent to the user.
    """
    system_prompt = """You are an expert blog editor specializing in AI and technology content. Your task is to modify the provided blog according to the user's instructions while maintaining its professional quality.

    Follow these two key guidelines:
    1. Content Modification:
       - Apply requested changes precisely while preserving core message
       - Maintain professional quality, technical accuracy, and readability
       - Ensure smooth transitions and logical flow throughout the modified content
       - Make the requested changes regardless of the type (shortening, expanding, changing tone, etc.)
       
    2. Visibility of Changes:
       - Add a "## MODIFICATIONS SUMMARY" section at the very end of the blog
       - List 2-4 bullet points that clearly explain what major changes were made
       - Be specific about what was modified (e.g., "Shortened introduction by 40%", "Added new section on ethics")
       
    Return the complete modified blog with the summary section at the end."""

    chat = ChatOpenAI(model="gpt-4o-mini")
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Original blog:\n\n{blog_content}\n\nPlease modify the blog according to these instructions:\n{modification_instructions}")
    ]
    response = chat(messages)
    return response.content

def generate_newspaper(articles: list = None, custom_prompt: str = None, instructions: str = "") -> str:
    """
    Generates a comprehensive multi-page newspaper format with in-depth analysis of AI news.
    Supports both:
    - Article-based newspaper generation
    - Custom prompt-based newspaper generation
    """

    # Define the base system prompt
    system_prompt = """You are an experienced newspaper editor-in-chief specializing in AI and technology. 
    Create a comprehensive, multi-page newspaper that deeply analyzes the provided content.
    
    NEWSPAPER STRUCTURE:
    FRONT PAGE:
    1. Main Headline & Lead Story
       - Compelling primary headline
       - Engaging subheadline
       - In-depth analysis of key story
       - Related infographic descriptions
       - Expert quotes and insights
    TECHNOLOGY SECTION:
    2. Technical Deep Dives
       - Detailed technical analysis
       - Architecture and implementation details
       - Expert technical perspectives
       - Innovation challenges and solutions
       - Future technical implications
    BUSINESS & INDUSTRY:
    3. Market Impact Analysis
       - Industry trends and patterns
       - Market predictions
       - Investment implications
       - Startup ecosystem insights
       - Corporate strategy analysis
    SOCIETY & ETHICS:
    4. Societal Implications
       - Workforce impact analysis
       - Ethical considerations
       - Policy and regulation updates
       - Privacy and security concerns
       - Social responsibility discussion
    INNOVATION SPOTLIGHT:
    5. Research & Development
       - Latest breakthroughs
       - Academic perspectives
       - Emerging technologies
       - Innovation roadmaps
       - Future predictions
    EDITORIAL & OPINION:
    6. Expert Commentary
       - Industry leader perspectives
       - Academic viewpoints
       - Policy maker opinions
       - Public discourse analysis
       - Strategic recommendations
    
    FORMAT GUIDELINES:
    - Use newspaper-style formatting
    - Include clear section breaks
    - Add relevant subheadings
    - Maintain consistent style
    - Use proper citations
    
    WRITING STYLE:
    - Professional and authoritative
    - Technically accurate
    - Balanced and objective
    - Engaging and insightful
    - Forward-thinking
    """

    chat = ChatOpenAI(model="gpt-4o-mini")
    
    # Generate messages based on the input type
    messages = [SystemMessage(content=system_prompt)]
    
    if custom_prompt:
        # Custom Prompt Path
        user_prompt = f"""
        User Prompt: {custom_prompt}
        
        Additional Instructions: {instructions}
        
        Generate a comprehensive, multi-page newspaper focusing on the topics and analysis described.
        """
        messages.append(HumanMessage(content=user_prompt))

    elif articles:
        # Article-based Path
        user_prompt = f"""
        Articles to include:
        
        {json.dumps(articles, indent=2)}
        
        Additional Instructions: {instructions}
        
        Generate a comprehensive newspaper analyzing these articles.
        """
        messages.append(HumanMessage(content=user_prompt))
    
    else:
        raise ValueError("Either 'articles' or 'custom_prompt' must be provided.")
    
    response = chat(messages)
    return response.content

# Streamlit UI with enhanced styling
st.set_page_config(page_title="AI News Hub", page_icon="📰", layout="wide")


# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button, .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .stSelectbox>div>div>input {
        border-radius: 5px;
    }
    .news-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    .tab-content {
        padding: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin-bottom: 1.5rem;
        background-color: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# Main title with custom styling
st.title("🤖 AI News Hub")
st.markdown("---")

# Initialize session state
if "articles" not in st.session_state:
    st.session_state.articles = []
if "custom_links" not in st.session_state:
    st.session_state.custom_links = []
if "generated_blogs" not in st.session_state:
    st.session_state.generated_blogs = {}
if "newspaper" not in st.session_state:
    st.session_state.newspaper = ""

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    st.markdown("---")
    
    # News fetch configuration
    st.subheader("📊 News Settings")
    num_articles = st.slider(
        "Number of articles to fetch:",
        min_value=0,
        max_value=10,
        value=5,
        step=5,
        help="Select how many AI news articles to fetch"
    )
    
    # Custom link input
    st.subheader("🔗 Add Custom Link")
    with st.form("custom_link_form"):
        custom_url = st.text_input("URL:", placeholder="https://example.com")
        custom_title = st.text_input("Title:", placeholder="Article title")
        custom_source = st.text_input("Source:", placeholder="Website name")
        submitted = st.form_submit_button("Add Link")
        
        if submitted and custom_url and custom_title:
            st.session_state.custom_links.append({
                'url': custom_url,
                'title': custom_title,
                'source': {'name': custom_source or 'Custom Source'},
                'publishedAt': 'Custom',
                'description': 'User-added article'
            })
            st.success("✅ Link added successfully!")

# Create main tabs for the application
news_tab, blog_tab, newspaper_tab = st.tabs([
    "📰 AI Fetch News", 
    "✍️ Blog Generation", 
    "📄 Newspaper"
])

# TAB 1: AI Fetch News
with news_tab:
    st.header("🔍 Latest AI News")
    
    if st.button("🔄 Fetch Latest AI News", help="Get fresh AI news articles"):
        with st.spinner("Fetching latest news..."):
            st.session_state.articles = fetch_ai_news(num_articles)
            st.success(f"📚 {len(st.session_state.articles)} articles fetched!")

    # Display all sources
    all_sources = st.session_state.articles + st.session_state.custom_links
    
    if all_sources:
        st.subheader("📰 Available Sources")
        
        # Create tabs for different source types
        fetched_news_tab, custom_links_tab = st.tabs(["📄 Fetched News", "🔗 Custom Links"])
        
        with fetched_news_tab:
            if st.session_state.articles:
                for i, article in enumerate(st.session_state.articles):
                    with st.container():
                        st.markdown(f"""
                            <div class="news-card">
                                <h3>{article['title']}</h3>
                                <p><strong>Source:</strong> {article['source']['name']}</p>
                                <p><strong>Published:</strong> {article['publishedAt']}</p>
                                <p>{article['description']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No fetched news yet. Click 'Fetch Latest AI News' to get started.")
        
        with custom_links_tab:
            if st.session_state.custom_links:
                for i, link in enumerate(st.session_state.custom_links):
                    with st.container():
                        st.markdown(f"""
                            <div class="news-card">
                                <h3>{link['title']}</h3>
                                <p><strong>Source:</strong> {link['source']['name']}</p>
                                <p><strong>URL:</strong> {link['url']}</p>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No custom links added yet. Use the sidebar to add custom links.")
    else:
        st.info("No news sources available. Fetch news or add custom links to get started.")

# TAB 2: Blog Generation
with blog_tab:
    st.header("✍️ Blog Generation")
    
    # Get all sources for blog generation
    all_sources = st.session_state.articles + st.session_state.custom_links
    
    if all_sources:
        st.subheader("📝 Generation Options")
        
        # Option to choose sources or custom prompt
        generation_type = st.radio(
            "Choose Blog Generation Method:",
            ("From Sources", "Custom Prompt"),
            help="Generate a blog from fetched news sources or a custom prompt."
        )
        
        if generation_type == "From Sources":
            selected_sources = st.multiselect(
                "Select sources for blog generation:",
                range(len(all_sources)),
                format_func=lambda x: all_sources[x]['title']
            )
            
            if selected_sources:
                with st.container():
                    st.markdown('<div class="card">', unsafe_allow_html=True)
                    blog_instructions = st.text_area(
                        "Additional instructions (optional):",
                        placeholder="E.g., 'Focus on technical aspects' or 'Make it business-oriented'",
                        help="Provide specific instructions for blog generation"
                    )
                    
                    if st.button("🚀 Generate Blog Content"):
                        for idx in selected_sources:
                            source = all_sources[idx]
                            with st.spinner(f"Processing: {source['title']}"):
                                content = scrape_content(source['url'])
                                if content:
                                    blog = generate_blog(content, source['title'], blog_instructions)
                                    st.session_state.generated_blogs[idx] = {
                                        'title': source['title'],
                                        'content': blog,
                                        'version': 1
                                    }
                                    st.success(f"✅ Generated: {source['title']}")
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("Select sources from the list to generate blog content.")
        
        elif generation_type == "Custom Prompt":
            custom_title = st.text_input("Blog Title:", placeholder="Enter a catchy title")
            custom_prompt = st.text_area(
                "Custom Prompt:",
                placeholder="Describe what you want the blog to be about.",
                help="Provide a detailed description of the blog you want generated."
            )
            
            if st.button("🚀 Generate Custom Blog"):
                with st.spinner("Generating custom blog..."):
                    blog = generate_blog(custom_prompt, custom_title)
                    st.session_state.generated_blogs["custom_prompt"] = {
                        'title': custom_title,
                        'content': blog,
                        'version': 1
                    }
                    st.success(f"✅ Custom Blog Generated: {custom_title}")

        # ===== Move generated blogs display BELOW the form =====
        st.markdown("---")
        st.subheader("ℹ️ Generated Blogs")
        if st.session_state.generated_blogs:
            for idx, blog in st.session_state.generated_blogs.items():
                with st.expander(f"📄 {blog['title']}"):
                    st.markdown(blog['content'])
                    
                    # Modification controls
                    st.markdown("### ✏️ Modify Content")
                    mod_instructions = st.text_area(
                        "Modification instructions:",
                        key=f"blog_mod_{idx}",
                        help="Describe how you want to modify this blog content"
                    )
                    
                    if st.button("🔄 Apply Changes", key=f"blog_mod_btn_{idx}"):
                        with st.spinner("Applying modifications..."):
                            modified = modify_blog(blog['content'], mod_instructions)
                            st.session_state.generated_blogs[idx]['content'] = modified
                            st.session_state.generated_blogs[idx]['version'] += 1
                            st.success(f"✅ Changes applied! (Version {st.session_state.generated_blogs[idx]['version']})")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("💾 Save as TXT", key=f"save_txt_{idx}"):
                            filename = f"{blog['title'].replace(' ', '_')}.txt"
                            with open(filename, "w", encoding="utf-8") as f:
                                f.write(blog['content'])
                            st.success(f"✅ Saved as '{filename}'")
                    
                    with col2:
                        # Prepare download
                        txt_io = StringIO(blog['content'])
                        download_filename = f"{blog['title'].replace(' ', '_')}.txt"
                        st.download_button(
                            label="📥 Download TXT",
                            data=txt_io.getvalue(),
                            file_name=download_filename,
                            mime="text/plain",
                            key=f"download_btn_{idx}"
                        )
                    
                    with col3:
                        if st.button("🗑️ Clear Blog", key=f"clear_blog_{idx}"):
                            st.session_state.generated_blogs.pop(idx)
                            st.success("✅ Blog cleared!")
                            st.experimental_rerun()
        else:
            st.info("No blogs generated yet.")
    else:
        st.warning("⚠️ No sources available. Fetch news or add custom links first.")

# TAB 3: Newspaper Generation
with newspaper_tab:
    st.header("📰 AI Newspaper Generation")
    
    # Get all sources for newspaper generation
    all_sources = st.session_state.articles + st.session_state.custom_links
    
    if all_sources:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Select Sources or Enter Custom Prompt")
            
            # Select sources for newspaper generation
            newspaper_sources = st.multiselect(
                "Select sources for newspaper generation:",
                range(len(all_sources)),
                format_func=lambda x: all_sources[x]['title'],
                key="newspaper_sources"
            )

            # Custom prompt input
            custom_prompt = st.text_area(
                "Or enter a custom prompt for AI Newspaper Generation:",
                placeholder="E.g., 'Generate a newspaper article on the latest AI breakthroughs...'",
                help="Provide a custom prompt to generate an AI-powered newspaper."
            )
            
            # Optional instructions
            st.subheader("🎯 Newspaper Options")
            newspaper_instructions = st.text_area(
                "Additional instructions (optional):",
                placeholder="E.g., 'Focus on business impact' or 'Highlight ethical considerations'",
                help="Provide specific instructions for newspaper generation",
                key="newspaper_instructions"
            )
            
            if st.button("🚀 Generate Newspaper"):
                with st.spinner("Generating comprehensive newspaper..."):
                    if custom_prompt.strip():
                        # Custom Prompt Logic
                        newspaper_content = generate_newspaper(
                            custom_prompt=custom_prompt,
                            instructions=newspaper_instructions
                        )
                        st.session_state.newspaper = {
                            'content': newspaper_content,
                            'version': 1
                        }
                        st.success("✅ Newspaper generated from custom prompt!")
                    elif newspaper_sources:
                        # Selected Sources Logic
                        selected_articles = []
                        for idx in newspaper_sources:
                            source = all_sources[idx]
                            content = scrape_content(source['url'])
                            if content:
                                selected_articles.append({
                                    'title': source['title'],
                                    'content': content,
                                    'source': source['source']['name'],
                                    'url': source['url']
                                })
                        
                        if selected_articles:
                            newspaper_content = generate_newspaper(
                                articles=selected_articles,
                                instructions=newspaper_instructions
                            )
                            st.session_state.newspaper = {
                                'content': newspaper_content,
                                'version': 1
                            }
                            st.success("✅ Newspaper generated!")
                        else:
                            st.error("⚠️ Could not retrieve content from any of the selected sources.")
                    else:
                        st.warning("Please select sources or provide a custom prompt.")
    
        # Sidebar for viewing sources
        with col2:
            st.subheader("ℹ️ Selected Sources")
            if newspaper_sources:
                for idx in newspaper_sources:
                    source = all_sources[idx]
                    st.markdown(f"""
                        <div class="news-card">
                            <h4>{source['title']}</h4>
                            <p><strong>Source:</strong> {source['source']['name']}</p>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No sources selected yet.")
        
        # Display generated newspaper
        if st.session_state.newspaper:
            st.markdown("---")
            st.subheader("📰 Generated Newspaper")
            with st.expander("📄 AI Newspaper", expanded=True):
                st.markdown(st.session_state.newspaper['content'])
                
                # Modification controls
                st.markdown("### ✏️ Modify Newspaper")
                newspaper_mod_instructions = st.text_area(
                    "Modification instructions:",
                    key="newspaper_mod",
                    help="Describe how you want to modify this newspaper content"
                )
                
                if st.button("🔄 Apply Changes", key="newspaper_mod_btn"):
                    with st.spinner("Applying modifications..."):
                        modified = modify_blog(st.session_state.newspaper['content'], newspaper_mod_instructions)
                        st.session_state.newspaper['content'] = modified
                        st.session_state.newspaper['version'] += 1
                        st.success(f"✅ Changes applied! (Version {st.session_state.newspaper['version']})")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("💾 Save as TXT", key="save_txt_newspaper"):
                        filename = f"AI_Newspaper_V{st.session_state.newspaper['version']}.txt"
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(st.session_state.newspaper['content'])
                        st.success(f"✅ Saved as '{filename}'")
                
                with col2:
                    # Prepare download
                    txt_io = StringIO(st.session_state.newspaper['content'])
                    download_filename = f"AI_Newspaper_V{st.session_state.newspaper['version']}.txt"
                    st.download_button(
                        label="📥 Download Newspaper",
                        data=txt_io.getvalue(),
                        file_name=download_filename,
                        mime="text/plain",
                        key="download_btn_newspaper"
                    )
                
                with col3:
                    if st.button("🗑️ Clear Newspaper", key="clear_newspaper"):
                        st.session_state.newspaper = ""
                        st.success("✅ Newspaper cleared!")
                        st.experimental_rerun()

    else:
        st.warning("⚠️ No sources available. Fetch news or add custom links first.")

