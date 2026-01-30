# Railway Deployment Guide - PDF2Editable V2 OCR

## Prerequisites

1. **Railway Account**: https://railway.app/
   - Sign up with GitHub (recommended)
   - Free tier: 500 hours/month

2. **Railway CLI** (optional, for command line):
   ```bash
   npm install -g @railway/cli
   ```

---

## Deployment Method 1: Web UI (Easiest)

### Step 1: Connect GitHub Repository

1. Push code to GitHub:
   ```bash
   cd pdf2editable
   git init
   git add .
   git commit -m "V2 OCR implementation"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. Go to https://railway.app/new
3. Click "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Dockerfile ✅

### Step 2: Configure Environment

Railway will automatically:
- Build Docker image
- Install Tesseract + language data
- Deploy to production URL

No environment variables needed (using defaults from .env.example)

### Step 3: Get URL

After deployment:
- Railway provides URL: `https://[PROJECT-NAME].up.railway.app`
- Copy this URL for testing

---

## Deployment Method 2: Railway CLI

```bash
# Login
railway login

# Initialize project
cd pdf2editable
railway init

# Link to new project
railway link

# Deploy
railway up

# Get domain
railway domain
```

---

## Testing After Deployment

### 1. Health Check

```bash
curl https://[YOUR-APP].up.railway.app/health
```

Expected:
```json
{
  "status": "healthy",
  "app": "PDF2Editable",
  "version": "0.1.0"
}
```

### 2. Test OCR with Scanned PDF

Use the API docs:
```
https://[YOUR-APP].up.railway.app/docs
```

Upload your Chinese PDF and verify:
- [ ] Conversion completes
- [ ] DOCX contains editable text (not images)
- [ ] Chinese characters recognized

---

## Monitoring

### View Logs

**Web UI**: https://railway.app/project/[PROJECT-ID]/deployments

**CLI**:
```bash
railway logs
```

Look for:
```
[V2-OCR] No text found on page 0, applying OCR...
[OCR] Extracted 1234 characters from page 0
```

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Request count
- Response times

---

## Troubleshooting

### Build Fails

Check Railway logs for:
- Tesseract installation errors
- Python dependency conflicts

### OCR Not Working

Verify in logs:
```
tesseract --version
tesseract --list-langs
```

Should show `chi_sim` in language list

### Performance Issues

Free tier limits:
- 512MB RAM (might need upgrade for large PDFs)
- Shared CPU

---

## Cost Estimate

**Free Tier** (first 500 hours):
- $0/month for testing
- Suitable for V2 validation

**Paid** (if exceeded):
- ~$5-10/month for hobby use
- ~$20/month for production

---

## Next Steps After Deployment

1. Get Railway URL
2. Test with scanned PDF
3. Verify OCR accuracy
4. Document results
5. Proceed to V2 Phase 3 (optimization) or V3 (SaaS)
