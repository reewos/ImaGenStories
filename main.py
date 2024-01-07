### Import libraries ###
import os
import tempfile
from PIL import Image
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from streamlit_tags import st_tags, st_tags_sidebar

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
st.title("🎨📝 ImaGenStories")

### Keys ###
try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    st.error("Error: Secrets")

### Models ###
gemini_vision = GeminiMultiModal(model_name="models/gemini-pro-vision")

### Global Variables ###
image = None
path = None
full_response = ""
message_placeholder = st.empty()
temp_dir = tempfile.mkdtemp()

prompt_story = texts["prompt_story"]
story_template = PromptTemplate(prompt_story)


st.sidebar.title("Parameters")
with st.sidebar:
    genre_select = st.selectbox(
        "Choose a genre",
        ("Adventure", "Mystery", "Police", "Romantic", "Science fiction", "Terror")
    )
    narrative_select = st.selectbox(
        "Choose a narrative type",
        ("Descriptive", "Linear", "Nonlinear", "Viewpoint")
    )
    # language_select = "English"
    language_select = st.selectbox(
        "Choose a language",
        ("English","Spanish")
    )
    size_select = st.selectbox(
        "Size of story",
        ("Short","Medium","Large")
    )

    keywords = st_tags_sidebar(
        label='Enter Keywords:',
        text='Press enter to add more',
        value=[],
        suggestions=['Other'],
        maxtags = 5,
        key='1')

#######

tab_main, tab_info = st.tabs(["Main", "Info"])

with tab_main:
    left_column, right_column = st.columns(2)
    with left_column:
        uploaded_files = st.file_uploader("Choose a image file", type = (["jpg", "jpeg", "png"]),accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            # st.write("filename:", uploaded_file.name)
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                with st.spinner('Loading...'):
                    st.image(image)
                path = os.path.join(temp_dir, uploaded_file.name)
                with open(path, "wb") as f:
                    f.write(uploaded_file.getvalue())
        # st.write([name for name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, name))])
        # st.write(len([name for name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, name))]))

    with right_column:
        st.write("Upload some image, and press the button")
        if st.button('Generate a story!'):
            if path is None:
                st.warning("Error: Path not found")
            else:
                image_documents = [ImageDocument(image_path=os.path.join(temp_dir, name)) for name in os.listdir(temp_dir) if os.path.isfile(os.path.join(temp_dir, name))]
                message_placeholder = st.empty()
                full_response = ""
                prompt_final = story_template.format(genre=genre_select,narrative=narrative_select,language=language_select,size=size_select,tags=keywords)
                try:
                    with st.spinner('Loading...'):
                        for response in gemini_vision.stream_complete(prompt = prompt_final, image_documents=image_documents):
                            full_response += (response.text or "")
                            message_placeholder.markdown(full_response + "▌")
                        message_placeholder.markdown(full_response)
                        st.session_state.full_response = full_response
                except Exception as e:
                    st.error(e)
                components.html('''
    <button class="button-13" onclick="copyContent()">📝 Copy</button>

    <script>
    let text = `'''+full_response.strip()+'''`;
    const copyContent = async () => {
        try {
            await navigator.clipboard.writeText(text);
            alert("Text copied successfully!");
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
    }
    </script>
        
        <style>
.button-13 {
  background-color: #fff;
  border: 1px solid #d5d9d9;
  border-radius: 8px;
  box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
  box-sizing: border-box;
  color: #0f1111;
  cursor: pointer;
  display: inline-block;
  font-family: "Amazon Ember",sans-serif;
  font-size: 13px;
  line-height: 29px;
  padding: 0 10px 0 11px;
  position: relative;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
  width: 100px;
}

.button-13:hover {
  background-color: #f7fafa;
}

.button-13:focus {
  border-color: #008296;
  box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
  outline: 0;
}
        </style>
    ''')
        
        # st.success('Text copied successfully!')

with tab_info:
    st.markdown(texts["about"])