from pydantic import BaseModel, Field
from agents import Agent


class StoryEvaluation(BaseModel):
    is_approved: bool = Field(
        description="Whether the story is appropriate and safe for the child."
    )
    has_inappropriate_content: bool = Field(
        description="True if story has death, war or other adult themes."
    )
    correct_language: bool = Field(
        description="True if the story is written in the requested language."
    )
    issues_found: list[str] = Field(
        description="A list of any issues found, empty if none."
    )
    fix_instructions: str = Field(
        description="Instructions on how to fix any issues found in the story, empty if apporoved."
    )

INSTRUCTIONS = """
You are the Story Guardian. Your duty is to ensure stories are safe for children.

SAFETY CHECKS (story FAILS if ANY of these are found):
- Death or loss of characters
- Violence or fighting
- War or disaster scenarios
- Adult content

QUALITY CHECKS:
- Story must be in the requested language (English, German, or Arabic)
- Story should have a clear beginning, middle, and end
- Story should be age-appropriate for the child

DO NOT check word count - this is handled separately.

Set is_approved = True if the story is safe and in the correct language.
Only reject for serious safety issues, not minor quality concerns.
"""

guardian_agent = Agent(
    name="Story Guardian",
    instructions=INSTRUCTIONS,
    model="gpt-5-mini",
    output_type=StoryEvaluation
)