

import time
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.tools import tool

from langchain_classic.agents import AgentExecutor, create_tool_calling_agent

load_dotenv()
st.set_page_config(
    page_title="Kunal — Portfolio Assistant",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown("""

<style>

/* Hide default Streamlit chrome */

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.block-container { padding: 1rem 2rem !important; max-width: 100% !important; }

/* Dark background */

html, body, [class*="css"] {

    background-color: #0a0a0f;

    color: #f1f0ff;

}

/* Sidebar */

[data-testid="stSidebar"] {

    background: #0f0f1a !important;

    border-right: 1px solid rgba(139,92,246,0.18) !important;

}

/* Chat bubbles */

[data-testid="stChatMessage"] {

    background: #13131f !important;

    border: 1px solid rgba(139,92,246,0.18) !important;

    border-radius: 14px !important;

    padding: 12px 16px !important;

}
[data-testid="stHeader"] {
    background-color: transparent !important;
}
/* Chat input box */

[data-testid="stChatInput"] textarea {

    background: #13131f !important;

    border: 1px solid rgba(139,92,246,0.3) !important;

    border-radius: 10px !important;

    color: #f1f0ff !important;

    padding:1rem 2rem !important;

}

[data-testid="stChatInput"] textarea:focus {

    border-color: rgba(139,92,246,0.6) !important;

    box-shadow: 0 0 0 3px rgba(139,92,246,0.1) !important;

}

/* Send button */

[data-testid="stChatInput"] button {

    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;

    border-radius: 10px !important;
    text-align:center;

}

/* Sidebar buttons */

.stButton > button {

    background: rgba(139,92,246,0.1) !important;

    border: 1px solid rgba(139,92,246,0.3) !important;

    border-radius: 20px !important;

    color: #c4b5fd !important;

    font-size: 12px !important;

}
 .stDownloadButton{
  background: rgba(139,92,246,0.1) !important;

    border: 1px solid rgba(139,92,246,0.3) !important;

    border-radius: 20px !important;

    color: #c4b5fd !important;

    font-size: 12px !important;
 }
.stButton > button:hover {

    background: rgba(139,92,246,0.2) !important;

    transform: translateY(-1px) !important;

}
[data-testid="stChatMessage"][data-author="user"] {
    background-color: #1e1e2e !important; /* Change this to your desired color */
    border: 1px solid #7c3aed !important; /* Optional: different border color */
    color: #ffffff !important;            /* Text color */
}

</style>

""", unsafe_allow_html=True)

st.markdown("""
<div style="display:flex; align-items:center; gap:12px; padding:16px 0;">
<div style="width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg,#7c3aed,#06b6d4); display:flex; align-items:center; justify-content:center; font-size:20px;">✦</div>
<div>
<div style="font-size:16px; font-weight:600; color:#f1f0ff;">Kunal — AI Portfolio Assistant </div>
<div style="font-size:12px; color:#22c55e;">● Online · Responds instantly</div>
</div>
</div>
""", unsafe_allow_html=True)

if "messages"  not in st.session_state:
    st.session_state.messages=[] 

llm=ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.5
)

@tool
def get_professional_info(skills:str)->str:
    """ Search and retrieve information from Kunal's professional profile and resume.
    Use this tool when asked about skills, experience, education, projects, 
    achievements, or any professional background information.
    """

    with open("Kunal_Master_Professional_Profile.txt","r",encoding="utf-8") as f:
        content=f.read()
        return content



tools=[get_professional_info]



for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👨‍💻").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="🤖").write(msg["content"])


if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")
else:
    prompt=st.chat_input("Ask me anything about kunal professional life")
if len(st.session_state.messages) == 0 and "pending_prompt" not in st.session_state:
    with st.chat_message("assistant", avatar="🤖"):
        st.write("Hey there! I'm Kunal's AI assistant. I can tell you everything about his work, skills, and projects. What would you like to know?")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⚡ Projects", use_container_width=True, key="pill1"):
                st.session_state.pending_prompt = "What are your best projects?"
                st.rerun()
        with col2:
            if st.button("💼 Skills", use_container_width=True, key="pill2"):
                st.session_state.pending_prompt = "What are your best skills?"
                st.rerun()
        with col3:
               if st.button("🏢 Experience", use_container_width=True, key="pill3"):
                st.session_state.pending_prompt = "What is your work experience?"
                st.rerun()



if prompt:
    agent_prompt=ChatPromptTemplate.from_messages([
    
      ("system", """You are a  personal AI assistant of Kunal. behave like kunal is answring the question
    You have access to Kunal's complete profile and resume via the get_profile_info tool.
    ALWAYS use the get_profile_info tool before answering any question about:
    - Skills, technologies, or expertise
    - Work experience or job history  
    - Education or certifications
    - Projects or achievements
    - Contact information
    Only answer from the retrieved profile data. If something isn't in the profile, say so clearly.""")
    ,
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    formated_history=[]## formated history is used for llm to have previous conversation idea.
    for msg in st.session_state.messages:
        role_type= "human" if msg["role"]=="user" else "ai"
        formated_history.append((role_type,msg["content"]))


    st.session_state.messages.append({"role":"user", "content":prompt})
    st.chat_message("user",avatar="👨‍💻").write(prompt)


    agent=create_tool_calling_agent(llm=llm,tools=tools,prompt=agent_prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    with st.chat_message("assistant",avatar="🤖"):
        status_placeholder = st.empty()
        
        # 2. Put the typing message inside the slot
        status_placeholder.markdown("Typing....")

        assistant_response = ""
        
        # 3. Run your agent executor background logic
        for chunk in agent_executor.stream({
            "input": prompt,
            "chat_history": formated_history
        }):
            if "output" in chunk:
                if not assistant_response:
                    status_placeholder.markdown("Typing......")
                assistant_response=chunk['output']
                
                displayed=""
                words=assistant_response.split(" ")
                for word in words:
                    displayed+=word+" "
                    status_placeholder.markdown(displayed+" ")
                    time.sleep(0.03)
                
    st.session_state.messages.append({"role":"assistant","content":assistant_response})
    st.rerun() 

with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; padding-bottom:16px; border-bottom:1px solid rgba(139,92,246,0.18); margin-bottom:16px;">
    <div style="width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg,#7c3aed,#06b6d4); display:flex; align-items:center; justify-content:center; font-size:18px;">✦</div>
    <div>
    <div style="font-size:14px; font-weight:600; color:#f1f0ff;">Kunal AI</div>
    <div style="font-size:11px; color:#6b678a;">Portfolio Assistant</div>
    </div>
    </div>
    """,unsafe_allow_html=True)
   
    st.markdown("<div style='font-size:16px; color:#6b678a; margin:12px 0 8px;'>QUICK TOPICS</div>", unsafe_allow_html=True)
    if st.button("⚡",use_container_width=True):
        st.session_state.pending_prompt = "What technologies does Kunal work with?"
        st.rerun()
    if st.button("💼 Projects", use_container_width=True):
        st.session_state.pending_prompt = "Tell me about Kunal's best projects"
        st.rerun()
    if st.button("🏢 Experience", use_container_width=True):
        st.session_state.pending_prompt = "What is Kunal's work experience?"
        st.rerun()

    if st.button("📬 Contact", use_container_width=True):
        st.session_state.pending_prompt = "How can I contact Kunal?"
        st.rerun()
    if st.button("🗑 clear chat",use_container_width=True):
        st.session_state.messages=[]
        st.rerun()
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; padding-bottom:16px; border-bottom:1px solid rgba(139,92,246,0.18); margin-bottom:16px;">

    """,unsafe_allow_html=True)
    with open("kunalresume.pdf", "rb") as f:
        pdf_data = f.read()
    
    st.download_button(
        label="📥 Download Resume",
        data=pdf_data,
        file_name="kunalresume.pdf",
        mime="application/pdf",
        use_container_width=True # This keeps your styling consistent
    )