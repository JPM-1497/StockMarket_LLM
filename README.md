Stock Market Copilot
 Stock Market Copilot is an AI-powered web application that helps users explore, analyze, and compare
 stock performance using natural language. Built using a full-stack architecture with FastAPI,
 PostgreSQL, Qdrant, and a modern React + Vite frontend, the app enables seamless interaction
 between large language models (LLMs), real-time data, and clean visualizations.
 Features- Natural language stock comparison - Interactive line charts with KPI cards - Real-time news
 integration per stock - Semantic search via Qdrant and sentence-transformers - JWT-based login and
 signup system - Fully Dockerized for local or cloud deployment
 Tech Stack
 Frontend: React (with Vite and TailwindCSS) Backend: FastAPI (Python) Database: PostgreSQL
 Vector DB: Qdrant LLMs: OpenAI or Hugging Face (FLAN-T5 / LLaMA-ready) Auth: JWT Deployment:
 Docker and Docker Compose
 Local Setup
 1. Clone the repo: git clone https://github.com/yourusername/stock-market-copilot.git cd
 stock-market-copilot 2. Start Docker containers: docker compose up --build 3. Populate stock data:
 docker compose exec backend python scripts/populate_stocks.py 4. Load historical prices: docker
 compose exec backend python scripts/populate_historical_prices.py
 Authentication
 The app uses email/password login with secure JWT-based authentication. Visit /signup to create an
 account, then login via /login.
 How to Use
 Enter queries like: - Compare Google and Meta from Jan to March 2025 - Top 5 financial companies in
 the last quarter - Show me which energy companies outperformed Tesla in 2024 The app returns
 AI-generated stock insights, KPI cards, line charts, and related news.
 Environment Variables
 Copy .env.example to .env and fill in required keys: OPENAI_API_KEY=your_key_here
 QDRANT_HOST=qdrant DATABASE_URL=postgresql://postgres:postgres@postgres/stock_db
Project Structure
 /backend /api -> FastAPI routes /services -> Core business logic /models -> SQLAlchemy models
 /scripts -> Data scripts /frontend /src /components -> React UI components /pages -> Chat, Login,
 Signup
 Contributing
 Pull requests are welcome. Features like watchlists, real-time prices, and advanced LLM orchestration
 are on the roadmap.
 Credits
 Built using FastAPI, React, Vite, Qdrant, and OpenAI by Your Name.