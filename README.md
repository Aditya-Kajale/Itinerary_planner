.

🤖 AI Trip Planner - Gen AI Hackathon Submission
A sophisticated, AI-powered travel companion built with Flask and Google Cloud. This project moves beyond static itinerary generation to offer a dynamic, conversational, and hyper-personalized trip planning experience.

✨ Live Demo
You can interact with the live prototype here:

https://ui-service-96251359436.asia-south1.run.app/

(Suggestion: Record a short GIF of your app working and replace the link above to make your README even more impressive!)

🚀 Key Features
🧠 Conversational AI Agent: A stateful chat interface powered by Gemini 1.5 Flash, allowing for natural, multi-turn conversations about travel plans.

🛠️ Intelligent Tool Use: The AI agent dynamically decides when to use external tools to fetch real-time data, such as searching for flights, hotels, or activities.

🔍 Advanced Recommendation Engine: Leverages Vertex AI Search to provide semantic, context-aware recommendations for travel, stays, and activities based on nuanced user queries.

✨ Rich, Interactive UI: A polished frontend built with Flask, custom HTML/CSS, and JavaScript, featuring:

An interactive map that updates based on the conversation.

Rich "cards" to display structured information for hotels, flights, etc.

A dynamic cost tracker and itemized breakdown.

A persona-driven user profile to simulate hyper-personalization.

⚡ Real-time Streaming: AI responses are streamed word-by-word for a dynamic and engaging user experience.

☁️ Fully Serverless Architecture: The entire application is built on a scalable, secure, and cost-effective serverless foundation using Google Cloud Run and Cloud Functions.

🛠️ Tech Stack & Architecture
This project is built on a modern, decoupled, and scalable architecture.

Tech Stack
Category	Technology / Service
Frontend	Flask, HTML, CSS, JavaScript, Leaflet.js
Backend	Python, Flask, Google Cloud Run
AI / ML	Gemini 1.5 Flash, Vertex AI Search
Cloud & DevOps	Google Cloud Functions, IAM, Secret Manager

Export to Sheets
Architecture Diagram
The system is composed of a frontend UI service that communicates with a central "Mission Control Platform" (MCP) server. The MCP server orchestrates calls to the Gemini AI, which in turn uses serverless "tool" functions to fetch data from the recommendation engine.

Code snippet

graph TD
    subgraph User Browser
        A[User]
    end

    subgraph Google Cloud
        B(Flask UI on Cloud Run);
        C(MCP Server on Cloud Run);
        D{Gemini 1.5 Flash AI};
        E[find_options Function];
        F[get_realtime_conditions Function];
        G[(Vertex AI Search)];

        C -- 1. Sends prompt --> D;
        D -- 2. Decides to call tool --> E;
        E -- 3. Queries --> G;
        G -- 4. Returns results --> E;
        E -- 5. Returns data --> C;
        C -- 6. Sends tool data back --> D;
        D -- 7. Generates final response --> C;
    end

    A <--> B;
    B <--> C;
⚙️ Getting Started (Local Setup)
To run this project locally, you will need Python 3.10+, the Google Cloud CLI, and a configured Google Cloud project.

Clone the repository:

Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
Set up a virtual environment:

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install dependencies:
The project has multiple requirements.txt files. Install them all:

Bash

pip install -r requirements.txt
pip install -r server/requirements.txt
pip install -r functions/find_options/requirements.txt
pip install -r functions/realtime_conditions/requirements.txt
Authenticate with Google Cloud:
This allows your local code to access Google Cloud services.

Bash

gcloud auth application-default login
Deploy Backend Services:
The Flask UI requires the backend services to be live. Follow the deployment steps in the project documentation to deploy the server and functions to Google Cloud.

Run the Flask UI:
Once the backend is deployed, update the BACKEND_URL in ui.py with your live MCP Server URL and run the local UI server:

Bash

python ui.py
☁️ Deployment
The application is designed to be fully serverless.

UI Service (ui.py): Deployed as a containerized web service on Google Cloud Run.

MCP Server (server/app.py): Deployed as a separate, secure service on Google Cloud Run, using a dedicated service account with least-privilege permissions.

Tools (functions/): Each tool is deployed as a lightweight, independent Google Cloud Function.

This serverless approach ensures high availability, automatic scaling, and cost efficiency.

🔮 Future Improvements
True Itinerary Generation: Enhance the prompt.txt to instruct the AI to not just suggest options, but to organize them into a structured, day-by-day itinerary.

Live Map Integration: Connect the AI's responses to the Leaflet.js map, automatically adding pins for suggested locations.

Payment Gateway: Integrate a real payment gateway (like Stripe or Razorpay) with the "Checkout" button.

Database Persistence: Use Firestore to save user profiles and their trip histories across sessions.

👤 Author
Aditya Kajale / R.U.B.I.C.K