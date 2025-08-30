# 🚀 Deployment Guide - Markdown-to-Slides Agent

## Overview

This guide will help you deploy your Markdown-to-Slides Agent to production using:

- **Frontend**: Vercel (recommended for Next.js)
- **Backend**: Railway (recommended for Python/FastAPI)

## 📋 Prerequisites

1. **Git repository** (GitHub, GitLab, etc.)
2. **Vercel account** (free tier available)
3. **Railway account** (free tier available)
4. **OpenAI API key** (optional - app works in demo mode without it)

## 🔧 Pre-Deployment Setup

### 1. Update Frontend API URL

Before deploying, you'll need to update the frontend to point to your deployed backend URL.

In `frontend/src/lib/api.ts`, update line 3:

```typescript
// Replace this line:
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';

// With this (after you get your Railway URL):
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://your-railway-app.railway.app';
```

## 🚂 Phase 1: Deploy Backend to Railway

### Step 1: Prepare Your Repository

1. **Push your code** to GitHub/GitLab
2. Make sure all files are committed, especially:
   - `backend/Dockerfile`
   - `backend/railway.json`
   - `backend/requirements.txt`
   - `backend/main.py`

### Step 2: Deploy to Railway

1. **Go to** [railway.app](https://railway.app)
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**
6. **Select the `/backend` folder** as the source
7. **Railway will automatically**:
   - Detect the Dockerfile
   - Build and deploy your app
   - Assign a public URL

### Step 3: Configure Environment Variables

In Railway dashboard:

1. **Go to Variables tab**
2. **Add these variables**:
   ```
   DATABASE_URL=sqlite:///./data/slides_app.db
   OPENAI_API_KEY=your_openai_key_here (optional)
   ```

### Step 4: Get Your Backend URL

- Railway will provide a URL like: `https://your-app-name.railway.app`
- **Copy this URL** - you'll need it for the frontend

## ⚡ Phase 2: Deploy Frontend to Vercel

### Step 1: Update API URL

In `frontend/src/lib/api.ts`:

```typescript
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || 'https://your-railway-app.railway.app';
```

### Step 2: Deploy to Vercel

1. **Go to** [vercel.com](https://vercel.com)
2. **Sign up/Login** with GitHub
3. **Click "New Project"**
4. **Import your repository**
5. **Configure project**:
   - Framework: Next.js (auto-detected)
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

### Step 3: Configure Environment Variables

In Vercel dashboard:

1. **Go to Settings > Environment Variables**
2. **Add**:
   ```
   NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
   ```

### Step 4: Deploy

- **Click Deploy**
- Vercel will provide a URL like: `https://your-app.vercel.app`

## 🎯 Quick Deploy Commands

### Option 1: Using Git + Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy backend
cd backend
railway deploy

# Get the deployed URL
railway domain
```

### Option 2: Using Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy frontend
cd frontend
vercel

# Follow the prompts
```

## 🔧 Environment Variables Summary

### Backend (Railway)

```
DATABASE_URL=sqlite:///./data/slides_app.db
OPENAI_API_KEY=sk-your-key-here
PORT=8000
```

### Frontend (Vercel)

```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

## ✅ Post-Deployment Checklist

1. **Test the deployed backend**:

   ```bash
   curl https://your-railway-app.railway.app
   ```

2. **Test the deployed frontend**:

   - Visit your Vercel URL
   - Try the "Try Demo" button
   - Test slide generation

3. **Test the connection**:
   - Check browser console for API errors
   - Verify themes load correctly
   - Test slide navigation

## 🛠️ Troubleshooting

### Common Issues:

1. **CORS Errors**:

   - Make sure your Railway URL is correct in frontend
   - Check that backend is running on Railway

2. **Build Errors on Railway**:

   - Check that all dependencies are in `requirements.txt`
   - Verify Dockerfile is correct

3. **Frontend Build Errors on Vercel**:

   - Make sure `package.json` is in the `frontend` folder
   - Check that all imports are correct

4. **Database Issues**:
   - SQLite will work fine for demo purposes
   - For production, consider upgrading to Railway PostgreSQL

## 🎉 Alternative Free Deployment Options

### Backend Alternatives:

- **Heroku** (has free tier limitations)
- **Render** (free tier available)
- **Google Cloud Run** (pay-per-use)
- **AWS Lambda** (serverless, free tier)

### Frontend Alternatives:

- **Netlify** (free tier, great for static sites)
- **GitHub Pages** (free, but limited to static sites)
- **Cloudflare Pages** (free tier available)

## 📱 Final Result

After successful deployment, you'll have:

- **Backend**: `https://your-app.railway.app`
- **Frontend**: `https://your-app.vercel.app`
- **Full functionality**: AI-powered markdown to slides conversion
- **Professional demo**: Ready to show to DataJar!

## 🎯 Next Steps for DataJar

1. **Share the live demo URL** with DataJar
2. **Provide the GitHub repository** link
3. **Highlight key features**:
   - AI integration (OpenAI)
   - Modern tech stack (FastAPI + Next.js)
   - Professional UI/UX
   - Database persistence
   - Export functionality

Good luck with your DataJar application! 🚀
