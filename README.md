Kunal — AI Portfolio Assistant
A sleek, interactive AI-powered portfolio assistant built with Streamlit and LangChain. This application allows visitors to query professional information about Kunal—such as skills, experience, projects, and achievements—in a conversational, chat-based interface.

🚀 Features
Intelligent Agent: Uses LangChain's AgentExecutor and ChatGroq to retrieve specific profile information from a local knowledge base.

Custom UI: A modern, dark-themed interface with custom CSS for a premium feel.

Context-Aware: Maintains chat history for a natural conversational flow.

Quick Actions: Pre-defined buttons for instant access to common queries (Projects, Skills, Experience).

Direct Download: Seamless resume download integration directly from the sidebar.

🛠 Tech Stack
Frontend: Streamlit

LLM Framework: LangChain

AI Model: Groq API (using llama3 or similar via ChatGroq)

Styling: Custom CSS/HTML injection via Streamlit

📦 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/yourusername/kunal-portfolio-assistant.git
cd kunal-portfolio-assistant
Install dependencies:

Bash
pip install -r requirements.txt
Environment Variables:
Create a .env file in the root directory and add your Groq API key:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
Add your Data:
Ensure you have the following files in your root directory:

Kunal_Master_Professional_Profile.txt (The source text for the AI).

kunalresume.pdf (The resume file for the download button).

Run the application:

Bash
streamlit run app.py
📝 Usage
Chat: Use the chat interface to ask any questions about Kunal’s professional background.

Demo: https://kunal-portfolio-ai-assistant.streamlit.app

Quick Topics: Click the buttons in the sidebar or the main interface to trigger common queries.

Resume: Click the "Download Resume" button in the sidebar to get a copy of the PDF.

💡 How it works
The agent is designed to use the get_professional_info tool whenever a user asks about professional details. It reads from Kunal_Master_Professional_Profile.txt, ensuring that the AI provides accurate, verifiable information directly from your provided documentation.
