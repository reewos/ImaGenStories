import os
import tempfile
from PIL import Image
import numpy as np
import streamlit as st
from llama_index.prompts import PromptTemplate
from llama_index.llms import Gemini
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.schema import ImageDocument
from llama_index.multi_modal_llms.generic_utils import (
    load_image_urls,
)

####
st.set_page_config(
    page_title="ImaGenStories",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'About': """# ImaGenStories. 
"ImaGenStories: **I'm** **a** **Gen**erator of **Stories**"

Welcome to ImaGenStories, where image-ination meets storytelling! ImaGenStories is not just an app; it's a creative companion that transforms ordinary images into extraordinary tales.

## Unleash Your Creativity:
ImaGenStories is more than a mere story generator—it's a platform that empowers you to unleash your creativity in a unique way. By providing one or more images as a creative spark, ImaGenStories invites you to embark on a journey of imagination, turning static visuals into vibrant narratives.

## How It Works:
Simply choose an image or a combination of images that resonate with you, and let ImaGenStories weave a narrative tapestry around them. The app intelligently interprets visual elements, sparking the birth of characters, settings, and plots. It's an innovative way to break through creative blocks and discover new story ideas.

## Versatility at Your Fingertips:
Whether you're a seasoned writer seeking inspiration or someone who simply loves to explore the realms of storytelling, ImaGenStories adapts to your needs. Use it for short stories, novel concepts, screenplay ideas, or even as a tool for collaborative storytelling with friends.

## Features:
* Image-driven Story Generation: Turn images into the foundation of your stories.
* Diverse Genres: Explore various genres, from fantasy and science fiction to mystery and romance.
* Customization: Tailor the generated stories by adjusting parameters and preferences.
* Save and Share: Save your favorite story ideas or share them with fellow storytellers.

## Why ImaGenStories?
ImaGenStories goes beyond the ordinary, offering a dynamic and interactive storytelling experience. It's not just about generating stories; it's about cultivating your creativity and bringing your unique narratives to life.

Embark on a storytelling adventure like never before with ImaGenStories—where every image has a story to tell, and you're the author of the tale.

Start exploring and let your imagination run wild!"""
    }
    
#**I'm* *a* *Gen*erator of *Stories*, is an app that aims to create stories using one or more images as a premise.
    
)
st.title("ImaGenStories")
st.write("I'm a Generator of Stories")

try:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except:
    st.write("Error: Secrets")

#Models
llm = Gemini()
gemini_vision = GeminiMultiModal(model_name="models/gemini-pro-vision")


image = None
path = None
prompt_story = """
Generate a story with the given image. The story must be {genre} genre. The story must have a {narrative} narrative.
Please use the following prompts:
* Describe the scenario based on the given image.
* Find the possible characters or invent them according to the scenario of the image. Defines their appearance, behavior, and motivations.
* Generates a situation or possible conflict where one or more characters are involved.
* Maintain a logical sequence of events that lead toward resolution of the conflict.
* Provides a conclusion that resolves the conflict satisfactorily. It can be a happy ending or leave room for reflection, but it must be consistent with the story.
* Returns the answer in the {language} language.
"""
story_template = PromptTemplate(prompt_story)

# Using "with" notation
with st.sidebar:
    st.markdown("### Parameters")
    genre_radio = st.radio(
        "Choose a genre",
        ("Adventure", "Terror", "Mystery", "Police", "Romantic", "Science fiction")
    )
    narrative_radio = st.radio(
        "Choose a narrative type",
        ("Descriptive", "Linear", "Nonlinear", "Viewpoint")
    )
    language_radio = st.radio(
        "Choose a language",
        ("English", "Spanish")
    )
    
left_column, right_column = st.columns(2)

with left_column:
    uploaded_file = st.file_uploader("Choose a image file", type = (["jpg", "jpeg", "png"]))
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image)#,caption='Enter any caption here')
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
                #print(response.text, end="")
                full_response += (response.text or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            
 