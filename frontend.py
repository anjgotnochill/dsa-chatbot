import streamlit as st
import base64
import requests  
# from backend import answer_question

# ✅ Set page config with Saturn icon 🪐
st.set_page_config(page_title="DSAmaiMadad", page_icon="🪐", layout="wide")

# ✅ Apply CSS to set background image

background_image = "https://raw.githubusercontent.com/anjgotnochill/dsa-chatbot/main/img.jpeg"

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 2;
        background-image: url("data:image/jpeg;base64,{base64.b64encode(open(background_image, "rb").read()).decode()}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stApp"] {{
        background: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


st.title("🪐 DSAmaiMadad")  # ✅ Saturn icon in title

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
backend_url = "https://dsa-chatbot.onrender.com"
def get_answer_from_backend(prompt):
    try:
        # Send POST request to the backend with the user prompt
        response = requests.post(f"{backend_url}/ask", json={"question": prompt})
        # Return the answer from the backend response
        return response.text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, there was an issue getting the answer."
# ✅ Display chat history
if prompt := st.chat_input("Batao..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("soch raha hoon..."):
            try:
                # Call the backend for the answer
                answer = get_answer_from_backend(prompt)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Error: {str(e)}")

# ✅ Clear Chat Button with Moon 🌙
if st.button("🌙 Clear Chat"):
    st.session_state.messages = []
    st.rerun()  # ✅ Refreshes the page

# iface = gr.Interface(fn=chatbot, inputs="text", outputs="text")
# iface.launch(server_name="0.0.0.0", server_port=7860)
