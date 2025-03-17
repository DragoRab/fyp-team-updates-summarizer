import streamlit as st

def main():
    # Set page config
    st.set_page_config(page_title="About FYP Project", layout="wide")
    
    # Display project information
    st.title("FYP Project 2025- Summarization for Teams")
    
    # Add team members with some styling
    st.markdown("""
    ### Team Members:
    - **Vanasri Vignesh B**
    - **Sharan Vetrivelan**
    - **Shridhar ShriRam**
    """)
    
    # Optional: Add more project details or links
    st.divider()
    st.write("This project focuses on creating summarization tools for team collaboration.")
    
    # Display chat history from main page
    st.divider()
    st.subheader("Current Chat History")
    
    # Check if messages exist in session state
    if "messages" in st.session_state and st.session_state.messages:
        for msg in st.session_state.messages:
            st.write(f"**{msg['user']}:** {msg['text']}")
    else:
        st.info("No chat messages yet. Go to the main page to start chatting.")

if __name__ == "__main__":
    main() 