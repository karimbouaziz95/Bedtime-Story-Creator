from story_manager import StoryManager, UserInput

import asyncio
from dotenv import load_dotenv

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
        intrests=interests,
        special_character=special_character,
        moral_lesson=moral_lesson,
        topics_to_avoid=topics_to_avoid,
        include_fun_fact=include_fun_fact,
        story_language=story_language,
    )

    await StoryManager().run(user_input)


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
    asyncio.run(main())
