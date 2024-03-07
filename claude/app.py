import streamlit as st
import anthropic

# Set the title of the Streamlit app
st.title("Welcome to the Streamlit App")

# Create a sidebar for navigation
with st.sidebar:
    selected_option = st.radio("Choose an option:", ["Home", "About", "Contact"])

# Display content based on the selected navigation option
if selected_option == "Home":
    st.header("Home")
    st.write("Welcome to the home page of our Streamlit app. Explore the features and functionalities we offer.")

    if st.button("Click me"): 
        client = anthropic.Client(api_key=st.secrets["CLAUDE_API_KEY"], base_url="https://anthropic.langcore.org/")
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            temperature=0,
            max_tokens=1000,
            system="",
            messages=[
                {
                    "role": "user",
                    "content": "{{EMBEDDINGS_CONTEXT}} 好きな食べ物は？"
                }
            ],
            extra_body={
                "query":"好きな食べ物は？" ,
                "groupName" :"test",
            },
            extra_headers = {
                "Content-Type": "application/json",
                "LangCore-Embeddings": "on",
                "LangCore-Embeddings-Match-Threshold": "0",
                "LangCore-Embeddings-Match-Count": "3",
            },
        )
        print(message)
        st.markdown(message.content[0].text)


elif selected_option == "About":
    st.header("About")
    st.write("This Streamlit app is designed to showcase the integration of various APIs and functionalities in a seamless user interface.")
elif selected_option == "Contact":
    st.header("Contact")
    st.write("For inquiries and further information, please contact us at info@example.com.")
