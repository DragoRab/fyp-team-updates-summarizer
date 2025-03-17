import streamlit as st
import requests
import json
import time

def main():
    # Set page config
    st.set_page_config(
        page_title="Team Updates Summarizer",
        layout="centered"
    )
    
    # Initialize session state variables if they don't exist
    if 'debug_info' not in st.session_state:
        st.session_state.debug_info = []
    
    if 'base_url' not in st.session_state:
        st.session_state.base_url = "https://7ce9-34-32-128-37.ngrok-free.app"
    
    # Check for messages first, then set team_updates
    if 'team_updates' not in st.session_state:
        if "messages" in st.session_state and st.session_state.messages:
            # Format the messages into the desired format
            formatted_messages = []
            for msg in st.session_state.messages:
                formatted_messages.append(f"{msg['user']}: {msg['text']}")
            st.session_state.team_updates = "\n".join(formatted_messages)
        else:
            st.session_state.team_updates = """Person1: Im so frustrated
Person2: whats wrong Jim
Person1: I called the electronics shop to find out what time they close and it took me twenty minutes to get what I wanted
Person2: Twenty minutes just to find out what their business hours are
Person1: yes They have some sort of digital receptionist So when I called in a machine told me to push a button for the department I wanted to be transferred to
Person2: Oh I hate getting voicemail instead of a person What did you do
Person1: I just kept pushing buttons I was transferred to customer service but there a machine told me to choose between technical help warranty information or price information
Person2: Couldn't you choose to be transferred to a real person 
Person1: Eventually I did get to a real person I found out the closing time but by then the store had already closed"""
    
    # Later in the code, update team_updates if messages change
    if "messages" in st.session_state and st.session_state.messages:
        formatted_messages = []
        for msg in st.session_state.messages:
            formatted_messages.append(f"{msg['user']}: {msg['text']}")
        st.session_state.team_updates = "\n".join(formatted_messages)
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .summary-container {
        background-color: #1E1E1E;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
    }
    .summary-text {
        color: #00FFFF;
        font-family: 'Courier New', monospace;
        font-size: 16px;
        line-height: 1.5;
    }
    .summary-header {
        color: #FFFFFF;
        font-size: 18px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Top section for API configuration
    with st.expander("API Configuration", expanded=True):
        with st.form(key="url_form", clear_on_submit=False):
            new_base_url = st.text_input(
                "Base URL",
                value=st.session_state.base_url,
                help="Enter the base URL for the API (without /summarize)"
            )
            
            submit = st.form_submit_button("Save URL", type="primary", use_container_width=False)
            if submit:
                st.session_state.base_url = new_base_url.strip()
                #st.success(f"Base URL updated to: {new_base_url}")
        
        # Display the full endpoint that will be used
        st.info(f"API Endpoint: {st.session_state.base_url}/summarize")
    
    # Main container with styling
    with st.container():
        # Title
        st.title("Team Updates Summarizer")
        
        # Text input area
        team_updates = st.text_area(
            "Team Updates:",
            height=350,
            placeholder="Enter your team updates here...",
            value=st.session_state.team_updates
        )
        
        # Update session state whenever text changes
        st.session_state.team_updates = team_updates
        
        # Create a container for the summary
        summary_container = st.container()
        
        # Button to trigger summarization
        if st.button("Summarize", key="summarize_button", type="primary"):
            # Prepare timestamp for logging
            timestamp = time.strftime("%H:%M:%S")
            
            # Show a spinner while making the API request
            with st.spinner("Generating summary..."):
                try:
                    # Construct full API URL using the base URL from session state
                    api_url = f"{st.session_state.base_url}/summarize"
                    
                    # Prepare the payload with the correct key 'dialogue'
                    payload = {
                        "dialogue": team_updates.replace('\n',' ')
                    }
                    
                    # Log the request details
                    request_log = {
                        "timestamp": timestamp,
                        "url": api_url,
                        "payload": payload
                    }
                    
                    # Make the POST request
                    headers = {
                        "Content-Type": "application/json"
                    }
                    response = requests.post(api_url, json=payload, headers=headers)
                    
                    # Log the response
                    response_log = {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "content": response.text[:500] + ("..." if len(response.text) > 500 else "")
                    }
                    
                    # Add to debug info
                    st.session_state.debug_info.append({
                        "request": request_log,
                        "response": response_log
                    })
                    
                    # Check if the request was successful
                    if response.status_code == 200:
                        try:
                            # Parse the JSON response
                            result = response.json()
                            # Extract the summary from the response
                            summary = result.get("summary", "No summary field found in API response")
                            # Display the summary with custom styling
                            with summary_container:
                                st.markdown("<div class='summary-container'><p class='summary-header'>Summary:</p><p class='summary-text'>" + 
                                           summary + "</p></div>", unsafe_allow_html=True)
                        except json.JSONDecodeError:
                            with summary_container:
                                st.error("Error: API returned non-JSON response with status 200")
                    else:
                        error_message = f"Error: API returned status code {response.status_code}"
                        if response.text:
                            try:
                                error_details = response.json()
                                error_message += f"\nDetails: {json.dumps(error_details, indent=2)}"
                            except:
                                error_message += f"\nResponse: {response.text[:200]}"
                        with summary_container:
                            st.error(error_message)
                
                except requests.exceptions.RequestException as e:
                    # Handle any request exceptions
                    with summary_container:
                        st.error(f"Error connecting to API: {str(e)}")
                    # Add to debug info
                    st.session_state.debug_info.append({
                        "request": request_log,
                        "error": str(e)
                    })
                except Exception as e:
                    with summary_container:
                        st.error(f"Unexpected error: {str(e)}")
        
        # Debug section
        with st.expander("API Debug Information"):
            if st.session_state.debug_info:
                # Display the most recent API call first
                for i, debug_entry in enumerate(reversed(st.session_state.debug_info)):
                    st.subheader(f"API Call {len(st.session_state.debug_info) - i}")
                    
                    # Request information
                    st.write("Request:")
                    st.code(f"URL: {debug_entry['request']['url']}")
                    st.code(f"Timestamp: {debug_entry['request']['timestamp']}")
                    st.code(f"Payload: {json.dumps(debug_entry['request']['payload'], indent=2)}")
                    
                    # Response information if available
                    if 'response' in debug_entry:
                        st.write("Response:")
                        st.code(f"Status Code: {debug_entry['response']['status_code']}")
                        st.code(f"Headers: {json.dumps(debug_entry['response']['headers'], indent=2)[:500]}...")
                        st.code(f"Content: {debug_entry['response']['content']}")
                    
                    # Error information if available
                    if 'error' in debug_entry:
                        st.write("Error:")
                        st.code(debug_entry['error'])
                    
                    st.divider()
                
                if st.button("Clear Debug History"):
                    st.session_state.debug_info = []
                    st.experimental_rerun()
            else:
                st.write("No API calls made yet.")
                
        # About this app
        with st.expander("About this app"):
            st.write("""
            This app summarizes team updates by analyzing conversation text.
            It connects to an external API for text summarization.
            The debug panel shows details about API requests and responses.
            """)

if __name__ == "__main__":
    main()