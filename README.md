# 🚀 AI Travel Planner

> Your personal AI-powered trip assistant for planning vacations with ease.

![AI Travel Planner Banner](https://i.postimg.cc/mr3s2pF4/Screenshot-2025-07-18-222622.png)

## 📖 Description

AI Travel Planner is an intelligent travel assistant that helps users plan personalized trips with detailed itineraries, hotel and restaurant recommendations, and a downloadable PDF of their plan — all powered by AI.

Perfect for travelers who want:
- Stress-free vacation planning
- Personalized recommendations
- Organized itineraries
- Budget-conscious travel options

## 🔗 Live Demo

🌐 [Live App on Render](https://your-app-url.onrender.com)

## ✨ Features

- **Day-by-day itinerary generation** - Get detailed daily plans for your trip
- **Budget breakdowns** - Know exactly how much you'll spend
- **Weather-based recommendations** - Activities suited to the weather
- **Interactive chat interface** - Natural conversation with AI
- **Session-based memory** - Continues context throughout your planning
- **Downloadable travel plan as PDF** - Take your plan offline

## 🛠 Built With

- **Backend**: Python (FastAPI)
- **AI/LLM**: LangChain with Mistral/Groq APIs
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Containerization**: Docker
- **Deployment**: Render
- **PDF Generation**: ReportLab/WeasyPrint

## 🧑‍💻 Getting Started

### Prerequisites

- Python 3.8+
- Docker (optional)
- API key from Groq or OpenAI

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-travel-planner.git
   cd ai-travel-planner
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   ```
   
   Add your API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

3. **Option A: Run with Docker**
   ```bash
   docker build -t travel-bot .
   docker run -p 8000:8000 travel-bot
   ```

4. **Option B: Run locally**
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

5. **Visit the application**
   ```
   http://localhost:8000
   ```

## 🔌 API Endpoints

| Method | Endpoint              | Description                    |
|--------|-----------------------|--------------------------------|
| POST   | `/query`              | Ask a travel-related question  |
| POST   | `/clear-session`      | Reset session memory           |
| GET    | `/generate-pdf/:id`   | Download travel plan as PDF    |
| GET    | `/health`             | Health check                   |

### Example Usage

```bash
# Ask a travel question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Plan a 5-day trip to Paris"}'

# Clear session
curl -X POST "http://localhost:8000/clear-session"
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

## 🐛 Known Issues & To-Do

### 🔧 Known Issues
- Mobile UI responsiveness needs improvement
- PDF generation can be slow for large responses
- Session timeout handling could be better

### ✅ Roadmap
- [ ] Add multilingual support
- [ ] Integrate Google Maps API
- [ ] Add user authentication
- [ ] Implement trip sharing features
- [ ] Add mobile app version

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/abhijyotiba/ai-travel-planner)
![GitHub forks](https://img.shields.io/github/forks/abhijyotiba/ai-travel-planner)
![GitHub issues](https://img.shields.io/github/issues/abhijyotiba/ai-travel-planner)
![GitHub license](https://img.shields.io/github/license/abhijyotiba/ai-travel-planner)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact & Support

**Made with ❤️ by [Abhishek Jyotiba](mailto:your_email@example.com)**

- 📧 Email: abhishekjyotiba00@gmail.com
- 💼 LinkedIn: [linkedin.com](https://www.linkedin.com/in/abhishekjyotiba/)
- 🐦 X: [X-former Twitter](https://x.com/AbhishekJyotiba)
- 🌐 Website: [website]("")

---

⭐ **Star this repo if you found it helpful!**

## 🙏 Acknowledgments

- OpenAI/Groq for AI capabilities
- FastAPI community for excellent documentation
- All contributors who helped improve this project
