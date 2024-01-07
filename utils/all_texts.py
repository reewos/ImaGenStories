texts = {
"about": """
:blue[**ImaGenStories**]: :blue[**I'm a Gen**]erator of :blue[**Stories**]

Welcome to :blue[**ImaGenStories**], where image-ination meets storytelling 😁! :blue[**ImaGenStories**] is not just an app; it's a creative companion that transforms ordinary images into extraordinary tales.

## Unleash Your Creativity:
:blue[**ImaGenStories**] is more than a mere story generator—it's a platform that empowers you to unleash your creativity in a unique way. By providing one or more images as a creative spark, :blue[**ImaGenStories**] invites you to embark on a journey of imagination, turning static visuals into vibrant narratives.

## How It Works:
Simply choose an image or a combination of images that resonate with you, and let :blue[**ImaGenStories**] weave a narrative tapestry around them. The app intelligently interprets visual elements, sparking the birth of characters, settings, and plots. It's an innovative way to break through creative blocks and discover new story ideas.

## Versatility at Your Fingertips:
Whether you're a seasoned writer seeking inspiration or someone who simply loves to explore the realms of storytelling, :blue[**ImaGenStories**] adapts to your needs. Use it for short stories, novel concepts, screenplay ideas, or even as a tool for collaborative storytelling with friends.

## Features:
* Image-driven Story Generation: Turn images into the foundation of your stories.
* Diverse Genres: Explore various genres, from adventure and science fiction to mystery and romance.
* Customization: Tailor the generated stories by adjusting parameters and preferences.
* Save and Share: Save your favorite story ideas or share them with fellow storytellers. (Coming soon).

## Why ImaGenStories?
:blue[**ImaGenStories**] goes beyond the ordinary, offering a dynamic and interactive storytelling experience. It's not just about generating stories; it's about cultivating your creativity and bringing your unique narratives to life.

Embark on a storytelling adventure like never before with :blue[**ImaGenStories**]—where every image has a story to tell, and you're the author of the tale.

*Start exploring and let your imagination run wild!*

---

Author: [Reewos Talla](https://github.com/reewos)

Repository: [ImaGenStories](https://github.com/reewos/ImaGenStories)

Last updated: January 07, 2024

---
""",

"prompt_story" : """
Generate a compelling and coherent story given the images.
The story must be {genre} genre.
The story must have a {narrative} narrative.
The story must be {size} in size.

Please use the following instructions:
* First, try to understand the images and get the possible scenarios based on the given images.
* Find the possible characters or invent them according to the scenario of the image. Defines their appearance, behavior, and motivations.
* Generates a situation or possible conflict where one or more characters are involved.
* Maintain a logical sequence of events that lead toward resolution of the conflict.
* Provides a conclusion that resolves the conflict satisfactorily. It can be a happy ending or leave room for reflection, but it must be consistent with the story.
* Please ensure the story is engaging and well-structured.
* Use these keywords as an integral part of the story: {tags}
* Returns the answer in the {language} language.
"""
}