# Deployment Guide: Scratchy Agent

This guide covers deploying the Scratchy AI agent to various hosting platforms with a web interface.

## 🚀 Quick Start (Local Testing)

Before deploying to the cloud, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Make sure .env is configured with your API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the web server
python app.py
```

Visit `http://localhost:8080` in your browser!

---

## ☁️ Deployment Options

### Option 1: Vercel (Recommended for Serverless)

**Pros:** Free tier, auto-deploys from Git, serverless
**Cons:** Function timeout limits (10s free, 60s pro)

#### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/scratchy.git
   git push -u origin main
   ```

2. **Deploy to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect the `vercel.json` config

3. **Configure Environment Variables**
   - In Vercel dashboard → Settings → Environment Variables
   - Add these variables:
     ```
     LLM_PROVIDER=openai
     OPENAI_API_KEY=your-key-here
     OPENAI_MODEL=gpt-4o-mini
     USE_MOCK_DATA=true
     ```

4. **Deploy**
   - Click "Deploy"
   - Your app will be live at `https://your-project.vercel.app`

#### Important Notes:
- Vercel has a **60-second timeout** on Pro plan, **10 seconds** on free tier
- For long-running agent tasks, consider using Render instead
- Vercel is best for quick demos with mock data

---

### Option 2: Render (Recommended for Production)

**Pros:** Free tier, persistent storage, no timeout limits, easy setup
**Cons:** Cold starts on free tier

#### Steps:

1. **Push to GitHub** (same as Vercel step 1)

2. **Deploy to Render**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` config

3. **Configure Environment Variables**
   - In Render dashboard → Environment
   - Add these variables:
     ```
     LLM_PROVIDER=openai
     OPENAI_API_KEY=your-key-here
     OPENAI_MODEL=gpt-4o-mini
     OPENAI_BASE_URL=https://api.openai.com/v1
     USE_MOCK_DATA=true
     ```

4. **Deploy**
   - Click "Create Web Service"
   - Your app will be live at `https://your-project.onrender.com`

#### Important Notes:
- Free tier has **no timeout limits** - perfect for long-running agent tasks
- Free tier instances spin down after 15 minutes of inactivity (cold start ~30s)
- Upgrade to paid tier ($7/month) for always-on instances

---

### Option 3: Docker (Any Platform)

Use Docker to deploy to any platform (DigitalOcean, AWS, GCP, Azure, etc.)

#### Build and Run Locally:

```bash
# Build the image
docker build -t scratchy-agent .

# Run the container
docker run -p 8080:8080 --env-file .env scratchy-agent
```

Visit `http://localhost:8080`

#### Deploy to Cloud:

**DigitalOcean App Platform:**
1. Push to GitHub
2. Create new App in DigitalOcean
3. Select "Docker" as source
4. Configure environment variables
5. Deploy

**AWS ECS / Google Cloud Run / Azure Container Instances:**
1. Build and push image to container registry
2. Create service from image
3. Configure environment variables
4. Deploy

---

## 🔐 Environment Variables Reference

Required variables for all platforms:

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | LLM provider to use | `openai` or `local` |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `OPENAI_MODEL` | Model to use | `gpt-4o-mini` |
| `USE_MOCK_DATA` | Use mock data (true/false) | `true` |

Optional variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Port to run on | `8080` |
| `DEBUG` | Enable debug mode | `false` |
| `OPENAI_BASE_URL` | OpenAI API base URL | `https://api.openai.com/v1` |
| `LOCAL_LLM_BASE_URL` | Local LLM URL (if using local) | `http://localhost:11434` |
| `LOCAL_LLM_MODEL` | Local LLM model name | `llama3` |

---

## 📊 Platform Comparison

| Feature | Vercel | Render | Docker (Self-hosted) |
|---------|--------|--------|---------------------|
| **Free Tier** | ✅ Yes | ✅ Yes | N/A (you pay for hosting) |
| **Timeout** | ⚠️ 10s (free), 60s (pro) | ✅ None | ✅ None |
| **Cold Starts** | ✅ Fast (~1s) | ⚠️ Slow (~30s on free) | ✅ None (always on) |
| **Setup Difficulty** | ⭐ Easy | ⭐ Easy | ⭐⭐ Moderate |
| **Best For** | Quick demos | Production | Full control |

---

## 🧪 Testing Your Deployment

After deployment, test these endpoints:

1. **Homepage:** `https://your-app.com/`
2. **Health Check:** `https://your-app.com/health`
3. **Trigger Run:** `POST https://your-app.com/api/run`
4. **Get Status:** `https://your-app.com/api/status`
5. **Latest Report:** `https://your-app.com/api/latest`

---

## 🐛 Troubleshooting

### "Module not found" errors
- Make sure all dependencies are in `requirements.txt`
- Rebuild/redeploy

### "Environment variable not set" errors
- Check that all required env vars are configured in platform dashboard
- Restart the service after adding env vars

### Timeout errors (Vercel)
- Agent runs take 30-90 seconds with LLM calls
- Vercel free tier has 10s timeout - upgrade to Pro or use Render

### Cold start delays (Render free tier)
- First request after 15min inactivity takes ~30s
- Upgrade to paid tier for always-on instances

### Reports not persisting
- Vercel/serverless platforms have ephemeral storage
- Reports are lost on restart
- For persistent storage, use Render or self-hosted Docker

---

## 🎯 Recommended Setup

**For Development/Testing:**
- Use **Vercel** with mock data
- Fast deploys, easy to iterate

**For Production:**
- Use **Render** with real data
- No timeout limits, persistent storage
- Upgrade to paid tier ($7/month) for better performance

**For Enterprise:**
- Use **Docker** on your own infrastructure
- Full control, custom scaling, private deployment

---

## 🔄 Continuous Deployment

Both Vercel and Render support auto-deployment from Git:

1. Push changes to GitHub
2. Platform automatically rebuilds and deploys
3. New version live in 1-2 minutes

To enable:
- **Vercel:** Enabled by default
- **Render:** Enable "Auto-Deploy" in settings

---

## 📝 Next Steps

After deployment:

1. **Test the web interface** - Click "Run Agent" and verify it works
2. **Switch to real data** - Set `USE_MOCK_DATA=false` and configure API keys
3. **Add custom domain** - Both Vercel and Render support custom domains
4. **Monitor usage** - Check LLM API costs and adjust as needed
5. **Scale up** - Upgrade to paid tiers for better performance

---

## 💡 Tips

- **Start with mock data** to test deployment without API costs
- **Monitor LLM costs** - Each run costs ~$0.05-$0.10 with gpt-4o-mini
- **Use caching** - Consider caching LLM responses to reduce costs
- **Set rate limits** - Add rate limiting to prevent abuse on public deployments

---

Need help? Check the main [README.md](README.md) or open an issue on GitHub!
