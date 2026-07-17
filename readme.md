<div align="center">

# 🌾 Agronova AI

### AI-Powered Agricultural Intelligence Platform

[![Next.js](https://img.shields.io/badge/Next.js-15.3-black?style=for-the-badge&logo=next.js)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=for-the-badge&logo=typescript)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-38bdf8?style=for-the-badge&logo=tailwind-css)](https://tailwindcss.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev/)

**Empowering farmers with AI-driven insights for sustainable and profitable agriculture**

[Features](#-features) • [Installation](#-installation) • [Tech Stack](#-tech-stack) • [Contributing](#-contributing)

</div>

---

## 📖 About

Agronova AI is a comprehensive agricultural decision-support platform that leverages cutting-edge artificial intelligence to provide farmers with actionable insights. Built specifically for Indian farmers, the platform offers multilingual support and addresses real-world agricultural challenges through intelligent data analysis.

### 🎯 Problem Statement

Farmers face numerous challenges:
- Unpredictable crop yields
- Pest and disease identification
- Soil health management
- Market price volatility
- Language barriers in accessing technology

### 💡 Our Solution

Agronova AI provides:
- **AI-powered crop yield predictions** using multi-factor analysis
- **Intelligent pest & disease diagnosis** from plant images
- **Soil analysis & recommendations** for optimal crop selection
- **Real-time weather data** integration
- **Market price tracking** for informed selling decisions
- **Multilingual interface** (English, Hindi, Odia, Telugu)
- **Interactive field management** with map-based tools

---

## ✨ Features

### 🌱 Core Features

| Feature | Description |
|---------|-------------|
| **🎯 Yield Prediction** | AI-powered predictions using field data, weather, and soil conditions |
| **🐛 Pest & Disease Detection** | Image-based diagnosis with treatment recommendations |
| **🧪 Soil Analysis** | NPK analysis with crop recommendations and fertility reports |
| **🗺️ Field Management** | Interactive map-based field drawing and area calculation |
| **🌤️ Weather Integration** | Real-time weather data with 7-day forecasts |
| **💰 Market Prices** | Live market price tracking for major crops |
| **🌍 Multilingual** | Support for 4 Indian languages with text-to-speech |
| **📊 Analytics Dashboard** | Comprehensive insights and data visualization |

### 🎨 Design Features

- **Premium Glass Morphism** - Modern, depth-rich UI
- **Advanced Gradients** - Multi-color transitions and mesh backgrounds
- **Smooth Animations** - 60fps GPU-accelerated effects
- **Dark Mode** - Fully optimized dark theme
- **Responsive Design** - Works on all devices
- **Accessibility** - WCAG compliant with screen reader support

---


## 🚀 Installation

### Prerequisites

- **Node.js** 20.x or later
- **Python** 3.11.x
- **Google Gemini API Key**
- **WeatherAPI.com Key**

### Project Structure

```text
agrivision-ai/
├── backend/                # FastAPI ML Service
│   ├── api/                # API Endpoints & ML Logic
│   │   ├── main_api.py     # Primary FastAPI Entry Point
│   │   ├── train_model.py  # Model Training Script
│   │   └── best_pipeline.pkl
│   ├── requirements.txt    # Python Dependencies
│   └── Procfile           # Deployment Config
├── frontend/               # Next.js Application
│   ├── src/
│   │   ├── ai/             # Genkit Flows & AI Logic
│   │   ├── app/            # Next.js App Router
│   │   ├── components/     # UI Components
│   │   └── lib/            # Utilities & Translations
│   └── package.json        # Frontend Dependencies
├── Dockerfile              # Container Configuration
└── start.sh                # Multi-service Startup Script
```

### Quick Start

1. **Clone the repository**

```bash
git clone https://github.com/bitun123/agro-nova-2.git
cd agrivision-ai
```

2. **Frontend Setup**

```bash
cd frontend
npm install
cp .env.example .env # Add your API keys here
npm run dev
```

3. **Backend Setup**

```bash
cd ../backend
pip install -r requirements.txt
cd api
python main_api.py
```

### Using Docker

```bash
docker build -t agronova-ai .
docker run -p 3000:3000 -e GEMINI_API_KEY=your_key -e WEATHER_API_KEY=your_key agronova-ai
```

### Set up environment variables**

Create a `.env.local` file in the root directory:

```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here
```

**Get your API key:**
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Click "Create API key"
- Copy and paste into `.env.local`

4. **Run the development server**

```bash
npm run dev
# or
yarn dev
```

5. **Open your browser**

Navigate to [http://localhost:9002](http://localhost:9002)

### Build for Production

```bash
npm run build
npm start
```

---

## 🛠️ Tech Stack

### Frontend

- **[Next.js 15.3](https://nextjs.org/)** - React framework with App Router
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe development
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first styling
- **[Radix UI](https://www.radix-ui.com/)** - Accessible component primitives
- **[Lucide React](https://lucide.dev/)** - Beautiful icons
- **[Recharts](https://recharts.org/)** - Data visualization
- **[Leaflet](https://leafletjs.com/)** - Interactive maps

### AI & Backend

- **[Google Gemini](https://ai.google.dev/)** - Generative AI models
- **Custom ML Model** - Crop prediction (Python/FastAPI)
- **FastAPI** - Python backend for ML predictions

### State Management

- **React Context API** - Global state
- **Local Storage** - Data persistence
- **React Hook Form** - Form management
- **Zod** - Schema validation

### Development Tools

- **ESLint** - Code linting
- **Prettier** - Code formatting
- **TypeScript** - Type checking

---

## 📁 Project Structure

```
agrivision-ai/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (routes)/          # Application routes
│   │   ├── api/               # API routes
│   │   ├── globals.css        # Global styles
│   │   └── layout.tsx         # Root layout
│   ├── components/
│   │   ├── agrivision/        # Feature components
│   │   └── ui/                # Reusable UI components
│   ├── contexts/              # React contexts
│   │   ├── FieldsContext.tsx  # Field management
│   │   └── LanguageContext.tsx # Internationalization
│   ├── lib/
│   │   ├── translations.ts    # i18n translations
│   │   └── utils.ts           # Utility functions
│   └── ai/
│       ├── flows/             # AI workflows
│       └── prompts/           # AI prompts
├── public/                    # Static assets
├── .env.local                 # Environment variables
├── package.json               # Dependencies
├── tailwind.config.ts         # Tailwind configuration
└── tsconfig.json             # TypeScript configuration
```

---

## 🌍 Multilingual Support

AgriVision AI supports 4 languages:

| Language | Code | Status |
|----------|------|--------|
| 🇬🇧 English | `en` | ✅ Complete |
| 🇮🇳 Hindi (हिंदी) | `hi` | ✅ Complete |
| 🇮🇳 Odia (ଓଡ଼ିଆ) | `or` | ✅ Complete |
| 🇮🇳 Telugu (తెలుగు) | `te` | ✅ Complete |

### Adding New Languages

1. Add translations to `src/lib/translations.ts`
2. Update the `Translation` type
3. Add language option in Settings

---

## 🎨 Design System
<<<<<<< HEAD

### Color Palette

```css
/* Primary (Green) */
--primary: 142 70% 45%;

/* Secondary (Blue) */
--secondary: 221 83% 53%;

/* Accent (Amber) */
--accent: 43 74% 66%;
```

### Components

All components follow:
- **Accessibility** standards (WCAG 2.1)
- **Responsive** design (mobile-first)
- **Dark mode** support
- **Animation** best practices

---


## 📝 API Documentation

### AI Flows

#### Yield Prediction

```typescript
import { predictYieldFromPrompt } from '@/ai/flows/yield-prediction-from-prompt';

const result = await predictYieldFromPrompt({
  fieldDescription: "5 acre wheat field in Odisha",
  // Additional context provided via Genkit
});
```

#### Weather Integration

```typescript
import { getWeatherData } from '@/ai/flows/get-weather-data-flow';

const weather = await getWeatherData(20.2961, 85.8245);
// Now using WeatherAPI.com backend
```
import { diagnosePestDisease } from '@/ai/flows/diagnose-pest-disease-flow';

const diagnosis = await diagnosePestDisease({
  imageUrl: "data:image/jpeg;base64,...",
  cropType: "wheat"
});
```

### Custom ML Model

The Python FastAPI backend provides:

```python
# Endpoint: POST /predict
{
  "N": 50,
  "P": 40,
  "K": 30,
  "temperature": 25,
  "humidity": 70,
  "ph": 6.5,
  "rainfall": 100
}
```
=======
>>>>>>> 1cb0eeb5befef40c93066beda345e9c4b3a94e57
### run backend 
python -m uvicorn main_api:app --reload
### run frontend 
npm run dev
---

## 🔒 Security

- **API Keys** - Never commit `.env` to version control
- **Input Validation** - All user inputs are validated with Zod
- **XSS Protection** - React's built-in protection
- **CORS** - Configured for production domains


---

## 📊 Performance

### Lighthouse Scores

| Metric | Score |
|--------|-------|
| Performance | 95+ |
| Accessibility | 100 |
| Best Practices | 100 |
| SEO | 100 |

### Optimizations

- ⚡ **Next.js App Router** - Automatic code splitting
- 🖼️ **Image Optimization** - Next/Image component
- 🎨 **CSS-in-JS** - Tailwind CSS (JIT)
- 📦 **Bundle Size** - Tree shaking enabled
- 🚀 **Edge Functions** - Deployed on Vercel Edge

---

## 🧪 Testing

```bash
# Run type checking
npm run typecheck

# Run linting
npm run lint

# Build test
npm run build
```


### AUTHOR:- SATYAJIT DAS MAHAPATRA 
### GITHUB:-https://github.com/bitun123
---
