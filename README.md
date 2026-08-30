# 🌿 PlantVision AI — Vercel Web Application

**PlantVision AI** is a production-grade Computer Vision web application for plant disease detection across **Potato, Tomato, and Apple** crops, optimized specifically for **Vercel** deployment.

---

## 🚀 Key Features

1. **User Authentication:** Sign in, register, and guest testing with persistent browser sessions.
2. **Plant Selector:** Supports **Potato, Tomato, and Apple** (+ roadmap badges for Corn and Grape).
3. **Canvas Preprocessor:** Automatically normalizes any uploaded leaf image to exact **224 × 224 × 3 RGB** tensor specifications.
4. **1-Click Test Samples:** Built-in instant test samples for **Early Blight, Late Blight, Apple Scab, Black Rot, and Healthy Foliage**.
5. **AI Diagnosis & Prescription Card:**
   * Severity tags (🟢 Healthy, 🟡 Moderate, 🔴 High / Critical).
   * Confidence percentage gauge.
   * Treatment tabs: **🌿 Organic Remedies**, **🧪 Chemical Fungicides & Dosages**, and **🛡️ Preventative Guidelines**.
   * Multi-class probability distribution bars.
6. **Personal Scan History:** Automatically logs all scans to user profile with search and filtering.
7. **Analytics Dashboard:** Visual metrics for total scans, healthy ratio, crop volume breakdown, and disease frequency rankings.
8. **Plant Pathology Encyclopedia:** Complete searchable offline guide for all crops.
9. **Printable / PDF Pathology Report:** 1-click diagnostic report generator.

---

## ⚡ 1-Click Vercel Deployment

### Method 1: Deploy via GitHub (Recommended)
1. Push this directory (plantvision-ai-web) to a new GitHub repository:
   `ash
   git init
   git add .
   git commit -m Initial commit of PlantVision AI Web
   git branch -M main
   git remote add origin https://github.com/your-username/plantvision-ai-web.git
   git push -u origin main
   `
2. Go to [vercel.com/new](https://vercel.com/new).
3. Import your plantvision-ai-web repository.
4. Framework Preset will be automatically detected as **Vite**.
5. Click **Deploy** — your app is live on a global CDN in under 1 minute!

### Method 2: Deploy with Vercel CLI
`ash
npm i -g vercel
vercel
`

---

## ☁️ Connecting with Google Drive / Python Backend

1. When running on Vercel, the app defaults to the high-accuracy mock inference engine.
2. Click the ⚙️ **Settings** icon in the navbar.
3. Switch off mock mode and enter your backend URL (e.g. your FastAPI server, Render backend, or Colab Ngrok tunnel).
4. The frontend will automatically route the preprocessed 224x224 RGB image to your server at ${API_URL}/predict!
