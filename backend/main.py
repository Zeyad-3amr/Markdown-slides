from fastapi import FastAPI, HTTPException, Depends  # pyright: ignore[reportMissingImports]
from fastapi.middleware.cors import CORSMiddleware  # pyright: ignore[reportMissingImports]
from fastapi.responses import HTMLResponse, FileResponse  # pyright: ignore[reportMissingImports]
from fastapi.staticfiles import StaticFiles  # pyright: ignore[reportMissingImports]
from pydantic import BaseModel  # pyright: ignore[reportMissingImports]
from sqlalchemy.orm import Session  # pyright: ignore[reportMissingImports]
import os
from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
import openai  # pyright: ignore[reportMissingImports]
import markdown  # pyright: ignore[reportMissingModuleSource]
import re
from typing import Optional, List
from datetime import datetime
from database import get_db, create_tables
import crud

# Load environment variables
load_dotenv()

# Create database tables
create_tables()

app = FastAPI(title="Markdown-to-Slides Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app", "https://*.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    slides_html: Optional[str] = None
    theme_suggestion: Optional[str] = None
    conversation_id: str

class SlideTheme(BaseModel):
    name: str
    primary_color: str
    secondary_color: str
    background: str
    font_family: str
    description: str

# Database-backed storage
slide_themes = {
    "professional": SlideTheme(
        name="Professional",
        primary_color="#2563eb",
        secondary_color="#64748b",
        background="linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)",
        font_family="Inter, system-ui, sans-serif",
        description="Clean and corporate design with blue accents"
    ),
    "creative": SlideTheme(
        name="Creative",
        primary_color="#7c3aed",
        secondary_color="#ec4899",
        background="linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%)",
        font_family="Poppins, sans-serif",
        description="Vibrant and modern with purple-pink gradients"
    ),
    "minimal": SlideTheme(
        name="Minimal",
        primary_color="#374151",
        secondary_color="#9ca3af",
        background="#ffffff",
        font_family="Source Sans Pro, sans-serif",
        description="Clean and simple monochromatic design"
    )
}

def parse_markdown_to_slides(markdown_content: str) -> List[dict]:
    """Parse markdown content into individual slides"""
    # Split by h1 or h2 headers to create slides
    slides = []
    
    # Split content by headers
    sections = re.split(r'^(#{1,2}\s+.+)$', markdown_content, flags=re.MULTILINE)
    
    current_slide = {"title": "", "content": ""}
    
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
            
        # Check if it's a header
        if re.match(r'^#{1,2}\s+', section):
            # Save previous slide if it has content
            if current_slide["title"] or current_slide["content"]:
                slides.append(current_slide.copy())
            
            # Start new slide
            current_slide = {
                "title": re.sub(r'^#{1,2}\s+', '', section),
                "content": ""
            }
        else:
            # Add content to current slide
            current_slide["content"] += section + "\n"
    
    # Add the last slide
    if current_slide["title"] or current_slide["content"]:
        slides.append(current_slide)
    
    # If no slides were created from headers, create one slide with all content
    if not slides:
        slides.append({
            "title": "Presentation",
            "content": markdown_content
        })
    
    return slides

def generate_html_slides(slides: List[dict], theme: SlideTheme) -> str:
    """Generate HTML slide deck from parsed slides"""
    
    html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Slides</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Poppins:wght@300;400;600;700&family=Source+Sans+Pro:wght@300;400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: {theme.font_family};
            background: {theme.background};
            overflow-x: hidden;
        }}
        
        .slide-container {{
            display: none;
            min-height: 100vh;
            padding: 60px 40px;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            position: relative;
        }}
        
        .slide-container.active {{
            display: flex;
        }}
        
        .slide-title {{
            font-size: 3rem;
            font-weight: 700;
            color: {theme.primary_color};
            margin-bottom: 2rem;
            line-height: 1.2;
        }}
        
        .slide-content {{
            font-size: 1.5rem;
            color: {theme.secondary_color};
            max-width: 800px;
            line-height: 1.6;
        }}
        
        .slide-content h3 {{
            color: {theme.primary_color};
            margin: 1.5rem 0 1rem 0;
        }}
        
        .slide-content ul {{
            text-align: left;
            margin: 1rem 0;
        }}
        
        .slide-content li {{
            margin: 0.5rem 0;
        }}
        
        .navigation {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 15px;
            z-index: 100;
        }}
        
        .nav-btn {{
            background: {theme.primary_color};
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        
        .nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }}
        
        .nav-btn:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        
        .slide-counter {{
            position: fixed;
            top: 30px;
            right: 30px;
            background: rgba(255,255,255,0.9);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            color: {theme.primary_color};
        }}
        
        @media (max-width: 768px) {{
            .slide-title {{
                font-size: 2rem;
            }}
            
            .slide-content {{
                font-size: 1.2rem;
            }}
            
            .slide-container {{
                padding: 40px 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="slide-counter">
        <span id="current-slide">1</span> / <span id="total-slides">{len(slides)}</span>
    </div>
'''

    # Add slides
    for i, slide in enumerate(slides):
        active_class = "active" if i == 0 else ""
        content_html = markdown.markdown(slide["content"])
        
        html_template += f'''
    <div class="slide-container {active_class}" data-slide="{i}">
        <h1 class="slide-title">{slide["title"]}</h1>
        <div class="slide-content">
            {content_html}
        </div>
    </div>
'''

    # Add navigation and JavaScript
    html_template += '''
    <div class="navigation">
        <button class="nav-btn" id="prev-btn">← Previous</button>
        <button class="nav-btn" id="next-btn">Next →</button>
    </div>

    <script>
        let currentSlide = 0;
        const totalSlides = document.querySelectorAll('.slide-container').length;
        
        function showSlide(n) {
            console.log('showSlide called with n:', n);
            const slides = document.querySelectorAll('.slide-container');
            console.log('Found slides:', slides.length);
            
            // Handle wrapping
            if (n >= totalSlides) currentSlide = totalSlides - 1;
            if (n < 0) currentSlide = 0;
            
            console.log('Setting currentSlide to:', currentSlide);
            
            slides.forEach((slide, index) => {
                slide.classList.remove('active');
                console.log('Removed active from slide', index);
            });
            
            if (slides[currentSlide]) {
                slides[currentSlide].classList.add('active');
                console.log('Added active to slide', currentSlide);
            } else {
                console.error('Slide not found at index:', currentSlide);
            }
            
            const currentSlideElement = document.getElementById('current-slide');
            if (currentSlideElement) {
                currentSlideElement.textContent = currentSlide + 1;
                console.log('Updated slide counter to:', currentSlide + 1);
            }
            
            // Update navigation buttons
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');
            
            if (prevBtn) prevBtn.disabled = currentSlide === 0;
            if (nextBtn) nextBtn.disabled = currentSlide === totalSlides - 1;
            
            console.log('Navigation buttons updated. Prev disabled:', currentSlide === 0, 'Next disabled:', currentSlide === totalSlides - 1);
        }
        
        function changeSlide(direction) {
            console.log('changeSlide called with direction:', direction);
            console.log('current slide before:', currentSlide);
            currentSlide += direction;
            console.log('current slide after:', currentSlide);
            showSlide(currentSlide);
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(event) {
            if (event.key === 'ArrowLeft') changeSlide(-1);
            if (event.key === 'ArrowRight') changeSlide(1);
        });
        
        // Add event listeners for navigation buttons
        document.addEventListener('DOMContentLoaded', function() {
            console.log('DOM loaded, setting up navigation');
            
            const prevBtn = document.getElementById('prev-btn');
            const nextBtn = document.getElementById('next-btn');
            
            if (prevBtn) {
                prevBtn.addEventListener('click', function() {
                    console.log('Previous button clicked');
                    changeSlide(-1);
                });
            } else {
                console.error('Previous button not found');
            }
            
            if (nextBtn) {
                nextBtn.addEventListener('click', function() {
                    console.log('Next button clicked');
                    changeSlide(1);
                });
            } else {
                console.error('Next button not found');
            }
            
            // Initialize
            showSlide(0);
        });
    </script>
</body>
</html>
'''
    
    return html_template

async def get_ai_response(user_message: str) -> dict:
    """Get AI response for chat and slide generation with fallback for API issues"""
    
    # Check if OpenAI API key is available and valid
    api_key = os.getenv("OPENAI_API_KEY")
    
    # Analyze if this looks like meaningful markdown content for slides
    has_headers = any(indicator in user_message for indicator in ['#', '##', '###'])
    has_sufficient_content = len(user_message.strip()) > 50  # Minimum content length
    mentions_slides = any(word in user_message.lower() for word in ['markdown', 'slide', 'presentation'])
    
    # Only generate slides if there are actual headers AND sufficient content
    has_markdown = has_headers and has_sufficient_content
    
    # Simple theme suggestion based on content
    theme_name = "professional"  # default
    if any(word in user_message.lower() for word in ['creative', 'fun', 'colorful', 'vibrant', 'modern']):
        theme_name = "creative"
    elif any(word in user_message.lower() for word in ['minimal', 'simple', 'clean', 'basic']):
        theme_name = "minimal"
    
    # Try OpenAI API first, then fallback to rule-based responses
    if api_key and api_key.startswith('sk-'):
        try:
            # Create a prompt for the AI
            prompt = f'''
You are a helpful AI agent that converts markdown to slide presentations and suggests themes.

User message: "{user_message}"

If the user provided markdown content, analyze it and:
1. Suggest an appropriate theme (professional, creative, or minimal) based on the content
2. Provide a helpful response about the slides you'll generate
3. If there are any improvements or suggestions for the markdown structure, mention them

If the user is asking for changes or has questions, respond conversationally.

Respond in a friendly, helpful tone. Keep responses concise but informative.
'''

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that specializes in creating slide presentations from markdown content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "message": ai_response,
                "has_markdown": has_markdown,
                "suggested_theme": theme_name
            }
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            # Fall through to rule-based response
    
    # Fallback rule-based responses when OpenAI API is not available
    if has_markdown:
        slide_count = user_message.count('#')
        ai_response = f"""Perfect! I've detected markdown content with {slide_count} sections. 
        
I'll convert this into a beautiful slide presentation for you! Here's what I found:

✨ **Theme Suggestion**: I recommend the '{slide_themes[theme_name].name}' theme - {slide_themes[theme_name].description}

🎯 **Slide Structure**: Your content will be automatically organized into slides based on your headings.

📝 **Pro tip**: Your slides look great! You can switch themes and preview them on the right side.

Your slides are being generated now! 🚀"""
    else:
        # Check if user is asking for help or just chatting
        if any(word in user_message.lower() for word in ['help', 'how', 'what', 'hello', 'hi']):
            ai_response = """Hello! I'm your Markdown-to-Slides Agent. 🎯

I can help you convert markdown content into beautiful slide presentations! Here's how:

1. **Paste your markdown** with headings (# ## ###)
2. **I'll suggest themes** (Professional, Creative, or Minimal)  
3. **Preview your slides** with navigation
4. **Download as HTML** for presentations

Just paste your markdown content and I'll get started! You can include:
- Headers for slide titles
- Bullet points for content
- Any text you want to present

What would you like to create slides about?"""
        else:
            ai_response = """I'd be happy to help you create slides! 

To generate a slide presentation, please paste your markdown content with headings like:

```
# Main Title
## Section 1
Your content here...
## Section 2  
More content...
```

I'll convert it into beautiful slides with theme suggestions. Try the "Demo" button above for an example! 🎯"""
    
    return {
        "message": ai_response,
        "has_markdown": has_markdown,
        "suggested_theme": theme_name
    }

@app.get("/api/")
async def api_root():
    api_key = os.getenv("OPENAI_API_KEY")
    has_openai = api_key and api_key.startswith('sk-')
    
    return {
        "message": "Markdown-to-Slides Agent API", 
        "status": "running",
        "openai_enabled": has_openai,
        "mode": "AI-powered" if has_openai else "Demo mode (rule-based responses)"
    }

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the frontend HTML file"""
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    index_file = os.path.join(static_dir, "server", "app", "index.html")
    
    if os.path.exists(index_file):
        return FileResponse(index_file, media_type="text/html")
    else:
        # Fallback to API response if frontend not found
        return {"message": "Markdown-to-Slides Agent API - Frontend not built yet"}

@app.get("/demo")
async def demo_endpoint():
    """Get demo markdown content for testing"""
    demo_markdown = """# Welcome to Markdown-to-Slides Agent

## What is this?
A smart AI agent that converts your markdown into beautiful slide presentations!

## Key Features
- 🎯 Smart slide generation from markdown
- 🎨 AI-powered theme suggestions
- 💬 Conversational chat interface
- 📤 HTML export with navigation
- 📱 Responsive design

## Available Themes
- **Professional**: Clean corporate design
- **Creative**: Vibrant modern style
- **Minimal**: Simple and elegant

## How to Use
1. Paste your markdown content
2. Get AI theme suggestions
3. Preview your slides
4. Download as HTML

## Conclusion
Built with FastAPI, Next.js, and OpenAI for the ultimate slide creation experience!

*Thank you for trying the Markdown-to-Slides Agent!*"""

    return {
        "markdown": demo_markdown,
        "description": "Demo content showing various markdown features"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """Main chat endpoint that handles conversations and slide generation"""
    
    # Generate conversation ID if not provided
    conversation_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"
    
    # Get AI response
    ai_result = await get_ai_response(request.message)
    
    # Check if user provided markdown content
    slides_html = None
    theme_suggestion = None
    
    if ai_result["has_markdown"] or any(char in request.message for char in ['#', '##', '###']):
        # Parse markdown and generate slides
        slides = parse_markdown_to_slides(request.message)
        
        if slides:
            theme = slide_themes[ai_result["suggested_theme"]]
            slides_html = generate_html_slides(slides, theme)
            theme_suggestion = f"I suggest the '{theme.name}' theme: {theme.description}"
    
    # Store conversation in database
    # Check if conversation exists, create if not
    if not crud.get_conversation(db, conversation_id):
        crud.create_conversation(db, conversation_id)
    
    # Store user message
    crud.create_message(
        db=db,
        conversation_id=conversation_id,
        role="user",
        content=request.message
    )
    
    # Store AI response
    crud.create_message(
        db=db,
        conversation_id=conversation_id,
        role="assistant",
        content=ai_result["message"],
        slides_html=slides_html,
        theme_suggestion=theme_suggestion,
        slides_generated=slides_html is not None
    )
    
    return ChatResponse(
        message=ai_result["message"],
        slides_html=slides_html,
        theme_suggestion=theme_suggestion,
        conversation_id=conversation_id
    )

@app.get("/themes")
async def get_themes():
    """Get available slide themes"""
    return {"themes": slide_themes}

@app.get("/conversations/{conversation_id}")
async def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    """Get conversation history"""
    conversation = crud.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = crud.get_conversation_messages(db, conversation_id)
    return {
        "conversation_id": conversation_id,
        "created_at": conversation.created_at,
        "messages": messages
    }

@app.get("/conversations")
async def get_recent_conversations(db: Session = Depends(get_db)):
    """Get recent conversations"""
    conversations = crud.get_recent_conversations(db)
    return {"conversations": conversations}

@app.post("/generate-slides")
async def generate_slides_endpoint(request: dict):
    """Direct endpoint for generating slides from markdown"""
    
    markdown_content = request.get("markdown", "")
    theme_name = request.get("theme", "professional")
    
    if not markdown_content:
        raise HTTPException(status_code=400, detail="No markdown content provided")
    
    if theme_name not in slide_themes:
        theme_name = "professional"
    
    slides = parse_markdown_to_slides(markdown_content)
    theme = slide_themes[theme_name]
    html_output = generate_html_slides(slides, theme)
    
    return {
        "html": html_output,
        "theme_used": theme_name,
        "slides_count": len(slides)
    }

if __name__ == "__main__":
    import uvicorn  # pyright: ignore[reportMissingImports]
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

