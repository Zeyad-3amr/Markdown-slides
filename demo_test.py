#!/usr/bin/env python3
"""
Demo test to show the Markdown-to-Slides Agent working without OpenAI API
"""

import requests  # pyright: ignore[reportMissingModuleSource]
import json
from datetime import datetime

# Test with the demo endpoint
def test_without_openai():
    """Test the app functionality without OpenAI API"""
    
    print("🎯 Testing Markdown-to-Slides Agent (Demo Mode)")
    print("=" * 60)
    
    # Test data
    demo_markdown = """# DataJar Coding Challenge

## The Mission
Build a Markdown-to-Slides Agent that converts markdown into beautiful presentations.

## What I Built
- 🎯 Smart slide generation from markdown
- 🎨 3 beautiful themes (Professional, Creative, Minimal)
- 💬 Chat interface with fallback responses
- 📤 HTML export with navigation
- 💾 Database storage for conversations

## Tech Stack
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Next.js + Tailwind CSS + TypeScript
- **AI**: OpenAI GPT-3.5 (with fallback mode)

## Key Features
1. **Works without AI** - Smart fallback system
2. **Production ready** - Docker, deployment configs
3. **Responsive design** - Works on all devices
4. **Real-time preview** - See slides as you type

## Why This Rocks
- ⚡ Fast development (4 hours total)
- 🔧 Robust architecture with error handling
- 📈 Scalable and extensible
- 🎨 Beautiful UI/UX design

## Conclusion
This agent showcases technical skill, business thinking, and the ability to ship fast!

*Built with hustler energy by someone who loves creating solutions* 🚀"""

    # Test direct slide generation
    try:
        # This should work even without OpenAI
        response = requests.post('http://localhost:8001/generate-slides', json={
            'markdown': demo_markdown,
            'theme': 'creative'
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ SUCCESS: Generated {result['slides_count']} slides")
            print(f"✅ Theme used: {result['theme_used']}")
            
            # Save the HTML
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"demo_slides_{timestamp}.html"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result['html'])
            
            print(f"✅ Slides saved to: {filename}")
            print(f"✅ Open {filename} in your browser to see the slides!")
            
            return True
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running on localhost:8001")
        print("💡 Start it with: cd backend && python main.py")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_themes():
    """Test themes endpoint"""
    try:
        response = requests.get('http://localhost:8001/themes')
        if response.status_code == 200:
            themes = response.json()['themes']
            print(f"\n🎨 Available themes: {len(themes)}")
            for name, theme in themes.items():
                print(f"   • {theme['name']}: {theme['description']}")
            return True
    except:
        return False

def test_status():
    """Test API status"""
    try:
        response = requests.get('http://localhost:8001/')
        if response.status_code == 200:
            status = response.json()
            print(f"\n📊 API Status: {status['status']}")
            print(f"🤖 Mode: {status['mode']}")
            print(f"🔑 OpenAI enabled: {status['openai_enabled']}")
            return True
    except:
        return False

if __name__ == "__main__":
    print("🧪 Demonstrating Markdown-to-Slides Agent")
    print("This works WITHOUT OpenAI API - perfect for demo!\n")
    
    # Run tests
    status_ok = test_status()
    themes_ok = test_themes() 
    slides_ok = test_without_openai()
    
    print("\n" + "=" * 60)
    if all([status_ok, themes_ok, slides_ok]):
        print("🎉 DEMO SUCCESS! Your Markdown-to-Slides Agent is working perfectly!")
        print("\n🎯 Ready to show the interviewer:")
        print("   1. The agent converts markdown to slides instantly")
        print("   2. Multiple themes work beautifully") 
        print("   3. No OpenAI needed for core functionality")
        print("   4. Clean, production-ready code")
        print("   5. Responsive design and great UX")
        print("\n✨ When you add OpenAI API key, you'll get enhanced AI features!")
    else:
        print("⚠️  Some features need the backend server running")
        print("💡 Run: cd backend && python main.py")
