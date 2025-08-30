#!/usr/bin/env python3
"""
Simple test script to verify the Markdown-to-Slides Agent is working properly.
"""

import requests
import json
import time

# Configuration
BACKEND_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/")
        print(f"✅ Backend Health: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Backend Error: {e}")
        return False

def test_themes_endpoint():
    """Test themes endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/themes")
        themes = response.json()
        print(f"✅ Themes Available: {len(themes['themes'])} themes")
        for name, theme in themes['themes'].items():
            print(f"   - {theme['name']}: {theme['description']}")
        return True
    except Exception as e:
        print(f"❌ Themes Error: {e}")
        return False

def test_chat_endpoint():
    """Test chat endpoint with markdown"""
    markdown_content = """# Test Presentation

## Introduction
Welcome to our test presentation!

## Features
- Smart slide generation
- AI-powered themes
- Beautiful HTML export

## Conclusion
This is working perfectly!"""

    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "message": markdown_content,
                "conversation_id": None
            }
        )
        result = response.json()
        print(f"✅ Chat Response: {result['message'][:100]}...")
        
        if result.get('slides_html'):
            print("✅ Slides Generated Successfully!")
            print(f"✅ Theme Suggestion: {result.get('theme_suggestion', 'None')}")
            
            # Save generated slides for inspection
            with open('test_slides.html', 'w', encoding='utf-8') as f:
                f.write(result['slides_html'])
            print("✅ Test slides saved to 'test_slides.html'")
            
        return True
    except Exception as e:
        print(f"❌ Chat Error: {e}")
        return False

def test_direct_generation():
    """Test direct slide generation endpoint"""
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-slides",
            json={
                "markdown": "# Quick Test\n\n## This is a test\n\nHello world!",
                "theme": "creative"
            }
        )
        result = response.json()
        print(f"✅ Direct Generation: {result['slides_count']} slides with {result['theme_used']} theme")
        return True
    except Exception as e:
        print(f"❌ Direct Generation Error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Markdown-to-Slides Agent Integration\n")
    
    tests = [
        ("Backend Health Check", test_backend_health),
        ("Themes Endpoint", test_themes_endpoint),
        ("Chat Endpoint", test_chat_endpoint),
        ("Direct Generation", test_direct_generation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        print("-" * 50)
        
        if test_func():
            passed += 1
        else:
            print(f"⚠️  Test failed: {test_name}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Markdown-to-Slides Agent is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the backend server and try again.")
    
    print(f"\n🌐 Frontend should be available at: {FRONTEND_URL}")
    print(f"🔧 Backend API available at: {BACKEND_URL}")

if __name__ == "__main__":
    main()
