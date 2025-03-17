import streamlit as st
import time

def main():
    # Set page config
    st.set_page_config(page_title="Multi-User Chat App", layout="wide")
    
    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "num_users" not in st.session_state:
        st.session_state.num_users = 2  # Default to 2 users
    if "users" not in st.session_state:
        st.session_state.users = ["" for _ in range(6)]  # Max 6 users
    
    st.title("Multi-User Chat Window")
    
    # Select number of users
    st.session_state.num_users = st.slider("Select number of users", min_value=2, max_value=6, value=st.session_state.num_users)
    
    st.divider()
    
    # Collect user names
    for i in range(st.session_state.num_users):
        st.session_state.users[i] = st.text_input(f"Enter Name (User {i+1})", value=st.session_state.users[i], key=f"user_{i}")
    
    if any(not name.strip() for name in st.session_state.users[:st.session_state.num_users]):
        st.warning("All users must enter their names to start chatting.")
        return
    
    st.divider()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            st.write(f"**{msg['user']}:** {msg['text']}")
    
    st.divider()
    
    # Display message input boxes in rows with two columns each
    rows = (st.session_state.num_users + 1) // 2  # Calculate required rows
    for row in range(rows):
        cols = st.columns(2)
        for col_index in range(2):
            user_index = row * 2 + col_index
            if user_index < st.session_state.num_users:
                with cols[col_index]:
                    st.text_area(
                        f"Message ({st.session_state.users[user_index]})", 
                        key=f"user_{user_index}_msg", 
                        height=100,
                        on_change=lambda i=user_index: send_message(i),
                    )
    
    # Function to send messages
    def send_message(user_index):
        message_key = f"user_{user_index}_msg"
        message = st.session_state[message_key].strip().replace('\n','; ')
        if message:
            st.session_state.messages.append({"user": st.session_state.users[user_index], "text": message})
            st.session_state[message_key] = ""  # Clear input field
            st.rerun()
    
    # Clear chat button
    if st.button("Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()