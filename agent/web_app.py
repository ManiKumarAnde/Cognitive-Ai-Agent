import streamlit as st
from agent.agent import Agent

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Agent",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# INIT AGENT (SESSION SAFE)
# -------------------------------
if "agent" not in st.session_state:
    st.session_state.agent = Agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

agent = st.session_state.agent

# -------------------------------
# UI HEADER
# -------------------------------
st.title("🤖 AI Agent from Scratch")
st.caption("Local AI Agent with Memory, Tools, and Reasoning")

# -------------------------------
# CHAT DISPLAY
# -------------------------------
for role, message in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").markdown(message)
    else:
        st.chat_message("assistant").markdown(message)

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.chat_history.append(("user", user_input))

    # Agent response
    with st.spinner("Thinking..."):
        response = agent.think_and_act(user_input)

    st.chat_message("assistant").markdown(response)
    st.session_state.chat_history.append(("assistant", response))
