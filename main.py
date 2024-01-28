import streamlit as st
import os
import google.generativeai as genai
from text_ext import extract_text_from_pdf
import base64
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro") 
chat = model.start_chat(history=[]) # start chat seassion

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

##initialize our streamlit app
st.set_page_config(page_title="Gemini ChatPDF Application", page_icon=":shark:", layout="wide")

image_path = "resources\icon.png"
image_base64 = base64.b64encode(open(image_path, 'rb').read()).decode()
image_width = 70
image_height = 70
image_html = f"""
    <div style='display: flex; justify-content: center; align-items: center; height: 1vh;'>
        <img src='data:image/png;base64,{image_base64}' alt='Your Image' width='{image_width}' height='{image_height}'>
    </div>
"""
st.markdown(image_html, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: white;'>ChatPDF</h1>", unsafe_allow_html=True)

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


# Create a two-column layout
col1, col2 = st.columns([0.5, 0.5], gap="small")

col1.header("Upload a PDF")
uploaded_file = col1.file_uploader("Click to upload PDF", type=["pdf"])

if uploaded_file is None:
    st.stop()
else:
    
    file_path = os.path.join("Uploaded", "1.pdf")
    with open(file_path, "wb") as file:
        file.write(uploaded_file.getvalue())
    

base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")
pdf_display = ( f'<embed src="data:application/pdf;base64,{base64_pdf}" ''width="100%" height="1000" type="application/pdf"></embed>')
#pdf_display = (f'<iframe src="data:application/pdf;base64,{base64_pdf}" ''width="100%" height="1000" type="application/pdf"></iframe>')
    
col1.markdown(pdf_display, unsafe_allow_html=True)

col2.header("Ask Question")
input=col2.text_input("Question: ",key="input", placeholder="Ask your question")
submit=col2.button("Ask")

initial_prompt = """you are an expert in understanding artificial intelligence, computer vision, robotics, embedded systems, power electronics, and power systems research domain. 
You will be given research paper full text, and from that research paper text you will have to answer any of my questions what I will give you each at a time, """


pdf_file_path = "Uploaded\\1.pdf"
if uploaded_file:
    pdf_text = extract_text_from_pdf(pdf_file_path)
else:
    pdf_text = ""


if submit and input:
    joined_text = initial_prompt + pdf_text + input
    response=get_gemini_response(joined_text)
    
    # Add user query and response to session state chat history
    st.session_state['chat_history'].append(("You", input))
    col2.subheader("Response:")
    for chunk in response:
        col2.write(chunk.text)
        