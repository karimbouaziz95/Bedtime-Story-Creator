from pydantic import BaseModel, Field
from agents import Runner, trace, gen_trace_id
import asyncio

from planner_agent import planner_agent, StorySearchPlan, StorySearchItem
from research_agent import research_agent
from writer_agent import writer_agent, BedTimestory

class UserInput(BaseModel):
    child_name: str = Field(
        description="The name of the child the story is for. They will be the hero of the story!"
    )
    age: int = Field(description="The age of the child (2-10 years).")
    story_length: str = Field(
        description="The desired length of the story: short (5-7 min), medium (10-15 min), or long (20-30 min)."
    )
    interests: list[str] = Field(description="What the child is interested in")
    special_character: str | None = Field(
        description="Pet, friend, or toy to include in the story"
    )
    moral_lesson: str = Field(description="The life lesson to weave into the story")
    topics_to_avoid: list[str] | None = Field(
        description="Topics to avoid in the story"
    )
    include_fun_fact: bool = Field(
        description="Whether to include an educational fun fact in the story"
    )
    story_language: str = Field(
        description="The language to write the story in (German, English or Arabic)"
    )

class StoryResult(BaseModel):
    story: BedTimestory


class StoryManager:

    async def run(self, user_input: UserInput):
        """Run the story generation process, yielding status updates and the final story"""
        trace_id = gen_trace_id()
        with trace("Bedtime Story Creation", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )

            # Step 1: Plan searches
            search_plan = await self.plan_searches(user_input)

            # Step 2: Perform searches
            search_results = await self.perform_searches(search_plan)

            # Step 3: Write the story
            story = await self.write_story(user_input, search_results)

            # Final result
            print("Story creation completed.")
            print(f"Title: {story.title}")
            print(f"Story: {story.story}")
            


    async def plan_searches(self, user_input: UserInput) -> StorySearchPlan:
        """Create search queries based on user input."""
        print("Planning searches...")
        input_text = f"""
        Create search queries for a children's bedtime story based on these parameters:
        user's input = {user_input}     
        """
        result = await Runner.run(planner_agent, input_text)
        print(f"Will perform {len(result.final_output.searches)} searches.")
        return result.final_output_as(StorySearchPlan)
    
    async def perform_searches(self, search_plan: StorySearchPlan) -> list[str]:
        """Perform all planned searches in parallel"""
        print("Performing searches...")
        tasks = [
            asyncio.create_task(self.search(item)) for item in search_plan.searches
        ]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result:
                results.append(result)
        print(f"Completed {len(results)} searches.")
        return results
    
    async def search(self, item: StorySearchItem) -> str | None:
        """Perform a single web search"""
        input_text = f"""Search term: {item.query}\nPurpose: {item.purpose}"""
        try:
            result = await Runner.run(research_agent, input_text)
            return result.final_output
        except Exception as e:
            print(f"Error during search for query '{item.query}': {e}")
            return None

    async def write_story(
            self,
            user_input: UserInput,
            search_results: list[str]
    ) -> BedTimestory:
        """Write the bedtime story"""
        print("Writing story...")
        user_input_text = f"Write a single bedtime story based on these parameters:\
             user's input = {user_input}, \
             search results = {search_results}"
        result = await Runner.run(writer_agent, user_input_text)
        print("Story writing completed.")
        return result.final_output_as(BedTimestory)