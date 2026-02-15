# 🚀 Quick Start Guide: Scratchy Web Interface

## What's New?

Your Scratchy agent now has a **modern web interface**! You can access it via a browser and deploy it to the cloud with a public URL.

## Local Testing (5 minutes)

```bash
# 1. Navigate to project directory
cd scratchy

# 2. Install dependencies (if not already done)
pip install -r requirements.txt

# 3. Make sure .env is configured
# Edit .env and add your OPENAI_API_KEY

# 4. Run the web server
python app.py
```

Then open your browser to: **http://localhost:8080**

## Deploy to Vercel (10 minutes)

**Best for:** Quick demos, serverless deployment

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Add web interface"
git remote add origin https://github.com/yourusername/scratchy.git
git push -u origin main

# 2. Go to vercel.com
# 3. Click "New Project"
# 4. Import your GitHub repo
# 5. Add environment variables:
#    - LLM_PROVIDER=openai
#    - OPENAI_API_KEY=your-key-here
#    - OPENAI_MODEL=gpt-4o-mini
#    - USE_MOCK_DATA=true
# 6. Click "Deploy"
```

Your app will be live at: `https://your-project.vercel.app`

⚠️ **Note:** Vercel free tier has a 10-second timeout. For full agent runs, use Render instead.

## Deploy to Render (10 minutes)

**Best for:** Production use, no timeout limits

```bash
# 1. Push to GitHub (same as above)

# 2. Go to render.com
# 3. Click "New +" → "Web Service"
# 4. Connect your GitHub repo
# 5. Render auto-detects the render.yaml config
# 6. Add environment variables:
#    - LLM_PROVIDER=openai
#    - OPENAI_API_KEY=your-key-here
#    - OPENAI_MODEL=gpt-4o-mini
#    - USE_MOCK_DATA=true
# 7. Click "Create Web Service"
```

Your app will be live at: `https://your-project.onrender.com`

✅ **Recommended for production!** No timeout limits, free tier available.

## What You Can Do

Once deployed, you can:

1. **Trigger agent runs** - Click the "Run Agent" button
2. **Watch progress** - See real-time updates as the agent works
3. **View reports** - See generated narratives in a beautiful dashboard
4. **Share the link** - Anyone can access your public URL

## Files Created

- `app.py` - Flask web application
- `templates/index.html` - Dashboard UI
- `static/style.css` - Modern styling
- `static/app.js` - Frontend JavaScript
- `vercel.json` - Vercel deployment config
- `render.yaml` - Render deployment config
- `Dockerfile` - Docker containerization
- `Procfile` - Process definition
- `DEPLOYMENT.md` - Full deployment guide

## Need Help?

- **Full deployment guide:** See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Troubleshooting:** Check DEPLOYMENT.md troubleshooting section
- **Local testing issues:** Make sure all dependencies are installed

## Next Steps

1. ✅ Test locally first (`python app.py`)
2. ✅ Choose a platform (Vercel or Render)
3. ✅ Deploy following the steps above
4. ✅ Test your public URL
5. ✅ Share with the world! 🌍
