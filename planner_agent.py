from pydantic import BaseModel, Field
from agents import Agent


N_OF_SEARCHES = 6

class StorySearchItem(BaseModel):
    query: str = Field(description="The search item to use for web search.")
    purpose: str = Field(
        description="why this search item will help create a better story."
    )

class StorySearchPlan(BaseModel):
    story_theme: str = Field(
        description="The theme of the story derived from the user's preferences"
    )
    searches: list[StorySearchItem] = Field(
        description=f"A list of web searches to find story inspiration."
    )

INSTRUCTIONS = f"""
You are a children's story planner. 
Create {N_OF_SEARCHES} web search queries to find inspiration for a 
children's bedtime story.

YOU WILL RECEIVE THESE PARAMETERS IN THE PROMPT:
- Child's Name - the hero of the story
- Age - determines content complexity (CRITICAL - see below)
- Story Length - short/medium/long
- Interests - themes to include in the story
- Special Character - pet/friend/toy to include
- Moral Lesson - life lesson to weave in
- Topics to Avoid - what NOT to include
- Include Fun Fact - whether to find educational facts
- Story Language - German, English or Arabic

USE ALL THESE PARAMETERS to create targeted searches.
Your searches must help find:
1. Story ideas that match the child's interests
2. Content appropriate for the child's age (CRITICAL)
3. Ideas related to the special character if provided
4. Inspiration for the moral lesson
5. Fun facts if requested
6. Search queries in the requested story language

AGE-BASED SEARCH COMPLEXITY (CRITICAL - match search terms to age):

Age 2-3 (Toddler):
- Search terms: "toddler stories", "simple bedtime", "baby board book"
- Look for: repetitive patterns, familiar objects, basic emotions

Age 4-5 (Preschool):
- Search terms: "preschool stories", "picture book adventures"
- Look for: simple adventures, friendship, basic problem-solving

Age 6-7 (Early Reader):
- Search terms: "early chapter book", "first grade stories", "beginner novels"
- Look for: multi-step adventures, fairness themes, simple mysteries

Age 8-10 (Middle Grade) - MUST BE SOPHISTICATED:
- Search terms: "middle grade fantasy", "chapter book adventure", "tween fiction", "complex children's literature"
- Look for: multi-layered plots, character development arcs, plot twists, mysteries with clues, quests with multiple challenges, clever wordplay, rich world-building, nuanced emotions like doubt/hope/determination
- Search for sophisticated narrative techniques and story structures
- Include searches for "coming of age themes for kids" or "hero's journey children"

Avoid searching for any topics listed in "Topics to Avoid".
"""

planner_agent = Agent(
    name="Story Planner",
    instructions=INSTRUCTIONS,
    model="gpt-5-mini",
    output_type=StorySearchPlan
)