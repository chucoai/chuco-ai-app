# Chuco AI - AI Consulting Website

A modern, professional website for Chuco AI, an El Paso-based AI consulting agency specializing in helping small and mid-sized businesses implement practical AI solutions.

## Project Overview

Chuco AI provides AI consulting services including opportunity audits, custom LLM integrations, data strategy, process automation, training, and ongoing support. This website showcases our services and provides a professional online presence for client acquisition.

## Features

- **Dark starfield hero section** with animated stars and gradient text
- **Responsive design** optimized for all devices
- **Professional service showcase** with pricing information
- **About section** highlighting 15+ years of experience
- **Contact integration** with phone and email
- **Modern UI/UX** with purple (#8B5CF6) and gold (#FDB100) branding
- **SEO optimized** structure and content
- **Fast loading** with optimized assets

## Tech Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with gradients, animations, and responsive design
- **JavaScript** - Smooth scrolling, interactive elements, and animations

### Backend (FastAPI)
- **Python 3.8+** - Core language
- **FastAPI** - Modern web framework for APIs
- **Jinja2** - Template engine
- **Uvicorn** - ASGI server

### Dependencies
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
python-multipart==0.0.6
sqlalchemy==2.0.23
alembic==1.12.1
python-dotenv==1.0.0
pydantic==2.5.0
psycopg2-binary==2.9.9
aiofiles==23.2.1
pillow==10.1.0
```

## Project Structure

```
chuco-ai-app/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── static/               # Static assets
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   ├── images/
│   │   ├── favicons/     # Favicon files (16x16, 32x32, etc.)
│   │   └── logos/        # Brand logos
│   └── site.webmanifest  # Web app manifest
├── templates/            # HTML templates
│   └── index.html        # Main page template
└── venv/                # Virtual environment (not in git)
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Local Development

1. **Clone the repository:**
```bash
git clone https://github.com/chucoai/chuco-ai-app.git
cd chuco-ai-app
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the development server:**
```bash
python main.py
# Or: uvicorn main:app --reload
```

6. **Visit the website:**
Open http://localhost:8000 in your browser

## Deployment

### Cloudways Deployment

The website is deployed on Cloudways using Git deployment:

1. **Configure Git deployment** in Cloudways dashboard
2. **Repository:** `https://github.com/chucoai/chuco-ai-app.git`
3. **Branch:** `main`
4. **Deployment Path:** `/public_html/`

### Domain Configuration

- **Primary Domain:** chuco.ai
- **DNS Configuration:** A record pointing to Cloudways server IP
- **SSL Certificate:** Enabled via Cloudways

## Business Information

### Contact Details
- **Phone:** (844) 915-2828
- **Email:** yo@chuco.ai
- **Location:** El Paso, Texas

### Services Offered
1. **AI Opportunity Audits** - Starting at $3,000
2. **Custom AI Chatbots & LLM Integration** - $15,000-$100,000
3. **Data Strategy & Architecture** - Custom pricing
4. **Process Automation** - $10,000-$50,000
5. **AI Training & Change Management** - $5,000-$25,000
6. **Ongoing AI Support** - $1,000-$10,000/month

### Target Market
- Small to mid-sized businesses (<$5M revenue)
- 5-50 employees
- Home services, e-commerce, professional services
- Growth-oriented leadership
- Limited internal AI resources

## Development Workflow

### Making Changes

1. **Create feature branch:**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**

3. **Test locally:**
```bash
python main.py
```

4. **Commit and push:**
```bash
git add .
git commit -m "Description of changes"
git push origin feature/your-feature-name
```

5. **Deploy** via Cloudways Git deployment

### Code Style
- **HTML:** Semantic, accessible markup
- **CSS:** Organized by components, mobile-first responsive design
- **JavaScript:** ES6+ syntax, no external dependencies
- **Python:** PEP 8 compliance, type hints where applicable

## Performance Optimization

- **CSS/JS minification** for production
- **Image optimization** for web delivery
- **Lazy loading** for below-the-fold content
- **Fast loading times** (<3 seconds)
- **SEO optimization** with meta tags and semantic HTML

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Contributing

This is a private business website repository. For internal development:

1. Follow the development workflow above
2. Test thoroughly on multiple devices
3. Ensure all contact information is accurate
4. Maintain professional branding consistency

## License

Private - All rights reserved by Chuco AI

## Support

For technical issues or questions:
- **Developer:** David Negrete
- **Contact:** yo@chuco.ai
- **Phone:** (844) 915-2828

## Changelog

### Version 1.0 (Current)
- Initial website launch
- FastAPI backend implementation
- Responsive design with dark theme
- Service showcase and pricing
- Contact integration
- Cloudways deployment
- Custom domain setup (chuco.ai)

---

**Chuco AI** - Transforming businesses through intelligent automation  
El Paso, Texas | yo@chuco.ai | (844) 915-2828
