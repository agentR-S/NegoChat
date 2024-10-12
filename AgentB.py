import streamlit as st
import requests
import json

# Set up your actual OpenAI API key (from your OpenAI account)
api_key = "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"  # Replace with your actual OpenAI API key

# Headers for authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"  # OpenAI requires Bearer token for auth
}

# Function to send a request to OpenAI API
def get_openai_response(prompt):
    data = {
        "model": "gpt-3.5-turbo",  # Use gpt-3.5-turbo for free tier accounts
        "messages": [
            {"role": "system", "content": system_prompt},  # The system prompt to guide behavior
            {"role": "user", "content": prompt}  # The user's message
        ],
        "max_tokens": 150
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",  # OpenAI's official API endpoint
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Define the system prompt (agent characteristics and cultural contingencies)
system_prompt = """
You are an AI agent acting as a landlord in a rental negotiation. 
You represent European cultural traits like professionalism, fairness, and collaboration. 
You prioritize long-term commitments and ensure timely payments. 
You are firm on rental prices but open to negotiation on lease duration and terms, as long as they don't compromise the financial stability of the landlord.
Communicate in a polite but assertive manner, aiming for a win-win outcome while ensuring the landlord's interests are protected.
"""

# Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Streamlit interface
st.title("AI Landlord Negotiation Chat")

# User input
user_input = st.text_input("You:", "")

# Button to send user input
if st.button("Send") and user_input:
    # Get the AI response
    ai_response = get_openai_response(user_input)
    
    # Add to conversation history
    st.session_state.conversation.append(f"You: {user_input}")
    st.session_state.conversation.append(f"AI: {ai_response}")
    
    # Clear user input after submission
    user_input = ""

# Display conversation history
for message in st.session_state.conversation:
    st.write(message)
