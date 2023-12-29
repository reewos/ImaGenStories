### Import libraries ###
import os
import tempfile
from PIL import Image
import numpy as np
import streamlit as st
from llama_index.prompts import PromptTemplate
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.schema import ImageDocument
from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)
from utils.all_texts import *

### Set config ###
st.set_page_config(
    page_title="ImaGenStories",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': texts["about"]
    }    
)

st.markdown(
    """
    <style>
    [aria-label="dialog"]{
        width: 90vw;
    }
    </style>
    """, unsafe_allow_html=True
)
st.title("📝 ImaGenStories")

### Keys ###
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    st.write("Error: Secrets")

### Models ###
gemini_vision = GeminiMultiModal(model_name="models/gemini-pro-vision")

### Global Variables ###
image = None
path = None
prompt_story = texts["prompt_story"]
story_template = PromptTemplate(prompt_story)


st.sidebar.title("Parameters")
with st.sidebar:
    #st.radio(
    #    "Choose a genre",
    #    ("Adventure", "Mystery", "Police", "Romantic", "Science fiction", "Terror")
    #)
    genre_radio = st.selectbox(
        "Choose a genre",
        ("Adventure", "Mystery", "Police", "Romantic", "Science fiction", "Terror")
    )
    narrative_radio = st.selectbox(
        "Choose a narrative type",
        ("Descriptive", "Linear", "Nonlinear", "Viewpoint")
    )
#    language_radio = st.selectbox(
#        "Choose a language",
#        ("English","Spanish")
#    ) 

#######

tab_main, tab_info = st.tabs(["Main", "Info"])

with tab_main:
    left_column, right_column = st.columns(2)
    with left_column:
        uploaded_file = st.file_uploader("Choose a image file", type = (["jpg", "jpeg", "png"]))
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image)
            temp_dir = tempfile.mkdtemp()
            path = os.path.join(temp_dir, uploaded_file.name)
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())

    with right_column:
        st.write("Upload some image, and press the button")
        if st.button('Generate a story!'):
            if path is None:
                st.write("Error: Path not found")
            else:
                image_documents = [ImageDocument(image_path=path)]
                message_placeholder = st.empty()
                full_response = ""
                prompt_final = story_template.format(genre=genre_radio,narrative=narrative_radio,language=language_radio)
                for response in gemini_vision.stream_complete(prompt = prompt_final, image_documents=image_documents):
                    full_response += (response.text or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
with tab_info:
    st.markdown(texts["about"])