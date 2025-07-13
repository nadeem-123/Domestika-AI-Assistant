Domestika Creative Assistant — Prototype
An AI-powered web assistant that helps creative learners on Domestika:

Generate personalized learning roadmaps

Get AI-driven feedback on their creative work

Features
1. Skill Roadmap Generator
Enter a creative skill (e.g., “watercolor”) → Get a 5-step personalized roadmap using a real open-source LLM.

2. Artwork Feedback Engine
Describe your artwork → Get 2 strengths + 2 improvement suggestions from an AI art critique agent.

Setup Instructions
1. Clone the repo and install dependencies
pip install fastapi uvicorn httpx python-dotenv

2. Create a .env file
Add your Together.ai API key:
TOGETHER_API_KEY=your_api_key_here

3. Run the server
uvicorn main:app --reload

4. Open the UI
Visit http://localhost:8000 in your browser to interact with the assistant.

File Structure
File	            Purpose
main.py	            FastAPI backend, HTML frontend, API endpoints
.env	            Stores your Together.ai API key securely

Known Gaps
1. No image upload yet (text-only feedback)
2. LLM output parsing is naive (improvements needed for structure)
3. Only one model used (Mistral-7B); can be extended to support more

Next Experiments
Add image upload + AI vision feedback (e.g., with LLaVA)
Integrate peer recommendation engine
Save user sessions to track long-term progress
A/B test different prompt styles (descriptive vs. direct)

Prototype Screenshot:
<img width="1470" height="872" alt="Screenshot 2025-07-13 at 6 35 36 PM" src="https://github.com/user-attachments/assets/18d8c73e-70ca-48e6-8a8c-8c7a7b8e3457" />
