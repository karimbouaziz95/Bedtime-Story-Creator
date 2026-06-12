from story_manager import StoryManager, UserInput

import asyncio
from dotenv import load_dotenv
import gradio as gr

load_dotenv(override=True)

async def generate_story(
    child_name: str,
    age: int,
    story_length: str,
    interests: list[str],
    special_character: str,
    moral_lesson: str,
    topics_to_avoid: list[str],
    include_fun_fact: bool,
    story_language: str,
):
    user_input = UserInput(
        child_name=child_name,
        age=age,
        story_length=story_length,
        interests=interests,
        special_character=special_character,
        moral_lesson=moral_lesson,
        topics_to_avoid=topics_to_avoid,
        include_fun_fact=include_fun_fact,
        story_language=story_language,
    )
    await StoryManager().run(user_input)

with gr.Blocks(
    #theme= gr.themes.Soft(primary_hue="blue", secondary_hue="blue"),
    title="Bedtime Story Creator"
) as ui:
    gr.Markdown("# 🌙 Bedtime Stories Creator")

    # Child's Name
    with gr.Group():
        child_name = gr.Textbox(
            label="Child's Name", placeholder="Enter a name..."
        )
        
    # Child's Age
    with gr.Group():
        age = gr.Dropdown(
            label="Child's Age",
            choices = [str(i) for i in range(2, 11)],
            value="6",
            interactive=True
        )

    # Interests
    with gr.Group():
        interests = gr.Dropdown(
            label="Interests",
            interactive=True,
            choices=[
                # Animals & Nature
                "Animals",
                "Dinosaurs",
                "Ocean",
                "Nature",
                "Butterflies",
                "Birds",
                "Rabbits",
                # Fantasy
                "Dragons",
                "Unicorns",
                "Fairies",
                "Magic",
                "Wizards",
                # Adventure
                "Pirates",
                "Space",
                "Superheroes",
                "Ninjas",
                "Knights",
                "Explorers",
                # Toys & Brands
                "LEGO",
                "Playmobil",
                "Hot Wheels",
                "Barbie",
                "Paw Patrol",
                "Peppa Pig",
                # Gaming
                "Minecraft",
                "Fortnite",
                "Roblox",
                "Pokemon",
                "Mario",
                "Gaming",
                "Brawlstar",
                # Vehicles
                "Trains",
                "Cars",
                "Airplanes",
                "Rockets",
                "Trucks",
                "Motorcycles",
                # Creative
                "Art",
                "Music",
                "Dancing",
                "Cooking",
                "Building",
                "Crafts",
                # Sports
                "Sports",
                "Soccer",
                "Basketball",
                "Swimming",
                "Martial Arts",
                # Characters
                "Princesses",
                "Robots",
                "Kings",
                "Queens",
            ],
            value=["Animals"],
            multiselect=True,
        )

    with gr.Group():

        # Story Length and Language
        story_length = gr.Dropdown(
            label="Story Length",
            choices=["short", "medium", "long"],
            value="medium",
            interactive=True
        )
        story_language = gr.Dropdown(
            label="Story Language",
            choices=["English", "German", "Arabic"],
            value="English",
            interactive=True
        )

        # Moral lesson
        moral_lesson = gr.Dropdown(
            label="Moral Lesson",
            interactive=True,
            choices=[
                "None",
                # Core values
                "Kindness",
                "Courage",
                "Honesty",
                "Patience",
                "Gratitude",
                # Social
                "Friendship",
                "Sharing",
                "Teamwork",
                "Helping Others",
                "Forgiveness",
                # Personal growth
                "Being Yourself",
                "Believing in Yourself",
                "Never Give Up",
                # Responsibility
                "Responsibility",
                "Hard Work",
                "Taking Care of Others",
                "Respecting Nature",
                # Emotional
                "Overcoming Fear",
                "Dealing with Change",
            ],
            value="Kindness",
        )

        # Other options
        with gr.Accordion("More options", open=False):
            special_character = gr.Textbox(
                label="Special Character (pet/friend/toy)", 
                placeholder="Mickey the mouse"
            )
            topics_to_avoid = gr.Textbox(
                label="Topics to Avoid (comma separated)", 
                placeholder="e.g. scary monsters, darkness"
            )
            include_fun_fact = gr.Checkbox(
                label="Include a fun fact?", value=True
            )

        # Button
        generate_btn = gr.Button(
            "✨ Create Story", variant="primary", size="lg"
        )

        # Status
        status_output = gr.Markdown(value="")

        # Story output
        story_output = gr.Markdown(value="", rtl=True)

        gr.Markdown("🛡️ *Stories reviewed for child safety. AI can make mistakes.*")

async def main():


        
    await generate_story(
        child_name="Alice",
        age=6,
        story_length="short",
        interests=["dragons", "magic"],
        special_character="teddy bear",
        moral_lesson="friendship",
        topics_to_avoid=["scary monsters"],
        include_fun_fact=True,
        story_language="English",
    )


if __name__ == "__main__":
    ui.launch(inbrowser=True)
    #asyncio.run(main())
