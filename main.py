from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Together.ai API Key
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Request and Response models
class JourneyRequest(BaseModel):
    skill: str

class JourneyResponse(BaseModel):
    roadmap: List[str]

class FeedbackRequest(BaseModel):
    description: str

class FeedbackResponse(BaseModel):
    strengths: List[str]
    improvements: List[str]

# Call Together.ai API
async def call_together_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.2",
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.together.xyz/v1/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['text'].strip()

@app.post("/generate-roadmap", response_model=JourneyResponse)
async def generate_roadmap(req: JourneyRequest):
    prompt = f"Create a personalized 5-step learning roadmap for someone who wants to learn '{req.skill}' from beginner to advanced level. Keep each step concise and clear."
    output = await call_together_ai(prompt)
    roadmap = [line.strip("-•1234567890. ") for line in output.split("\n") if line.strip()]
    return JourneyResponse(roadmap=roadmap[:5])

@app.post("/feedback", response_model=FeedbackResponse)
async def get_feedback(req: FeedbackRequest):
    prompt = f"You are an art critique AI. A user submitted this artwork description: '{req.description}'. List 2 strengths and 2 areas for improvement."
    output = await call_together_ai(prompt)

    # Naive parsing
    parts = output.split("Improvement:")
    strengths = parts[0].replace("Strengths:", "").split("\n")
    improvements = parts[1].split("\n") if len(parts) > 1 else ["N/A"]

    strengths = [s.strip("-• ") for s in strengths if s.strip()]
    improvements = [i.strip("-• ") for i in improvements if i.strip()]

    return FeedbackResponse(strengths=strengths[:2], improvements=improvements[:2])

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Domestika Creative Assistant</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; padding: 40px; background: #f7f7f7; }
                h1 { color: #E66A2B; }
                h2 { margin-top: 40px; color: #333; }
                input, textarea, button {
                    font-size: 16px;
                    margin-top: 10px;
                    padding: 8px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                button {
                    background-color: #E66A2B;
                    color: white;
                    border: none;
                    cursor: pointer;
                    margin-top: 10px;
                }
                button:hover {
                    background-color: #d35400;
                }
                .output-box {
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    margin-top: 20px;
                }
                ul { padding-left: 20px; }
                li { margin: 8px 0; }
            </style>
        </head>
        <body>
            <h1>🎨 Domestika Creative Assistant</h1>

            <h2>1. Personalized Skill Journey</h2>
            <form id="roadmap-form">
                <input type="text" id="skill" placeholder="e.g., watercolor" required />
                <button type="submit">Get Roadmap</button>
            </form>
            <div id="roadmap-result" class="output-box"></div>

            <h2>2. Feedback on Your Art</h2>
            <form id="feedback-form">
                <textarea id="description" rows="4" cols="50" placeholder="Describe your artwork..." required></textarea><br>
                <button type="submit">Get Feedback</button>
            </form>
            <div id="feedback-result" class="output-box"></div>

            <script>
                document.getElementById("roadmap-form").addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const skill = document.getElementById("skill").value;
                    const res = await fetch("/generate-roadmap", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ skill })
                    });
                    const data = await res.json();
                    let html = `<strong>📘 Skill Roadmap for: ${skill}</strong><ul>`;
                    data.roadmap.forEach(item => html += `<li>✅ ${item}</li>`);
                    html += "</ul>";
                    document.getElementById("roadmap-result").innerHTML = html;
                });

                document.getElementById("feedback-form").addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const description = document.getElementById("description").value;
                    const res = await fetch("/feedback", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ description })
                    });
                    const data = await res.json();
                    let html = `<strong>💡 Feedback on: "${description}"</strong><br/><br/>`;
                    html += `<strong>🌟 Strengths:</strong><ul>`;
                    data.strengths.forEach(s => html += `<li>✅ ${s}</li>`);
                    html += `</ul><strong>🛠️ Areas to Improve:</strong><ul>`;
                    data.improvements.forEach(i => html += `<li>⚠️ ${i}</li>`);
                    html += "</ul>";
                    document.getElementById("feedback-result").innerHTML = html;
                });
            </script>
        </body>
    </html>
    """
