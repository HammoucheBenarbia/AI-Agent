import os
import requests
import streamlit as st
from dotenv import load_dotenv

#Load environment variables
load_dotenv()

# Variables input 
API_BASE_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "your ID"
FLOW_ID = "your flow ID"
APP_TOKEN = os.getenv("APP_TOKEN")
FLOW_ENDPOINT = "Flow endpoint"  

def invoke_flow(user_message: str) -> dict:
    """
    Send a user message to the flow endpoint and return the JSON response.
    """
    target_url = f"{API_BASE_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ENDPOINT}"
    headers = {
        "Authorization": f"Bearer {APP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "input_value": user_message,
        "output_type": "chat",
        "input_type": "chat"
    }
    response = requests.post(target_url, json=payload, headers=headers)
    response.raise_for_status()  
    return response.json()

def main():
    st.title("I'M YOUR AI ASSISTANT")

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    #Display conversation 
    for msg in st.session_state["messages"]:
        role = msg["type"]  
        text = msg["text"]
        with st.chat_message(role):
            st.write(text)

    # Chat input
    if user_input := st.chat_input("Type your message..."):
        #Display and save the user message
        with st.chat_message("user"):
            st.write(user_input)
        st.session_state["messages"].append({"type": "user", "text": user_input})

        #Display a placeholder for the assistant's response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    #Invoke the bot flow
                    response = invoke_flow(user_input)

                    #Extract the relevant part of the bot's reply
                    bot_reply = response["outputs"][0]["outputs"][0]["results"]["message"]["text"]
                except Exception as e:
                    bot_reply = f"Error: {e}"

            #Display and save the assistant's reply
            st.write(bot_reply)
            st.session_state["messages"].append({"type": "assistant", "text": bot_reply})

if __name__ == "__main__":
    main()

