from pydantic import BaseModel, Field
from agents import Runner, trace, gen_trace_id
import asyncio

from planner_agent import planner_agent, StorySearchPlan, StorySearchItem
from research_agent import research_agent
from writer_agent import writer_agent, BedTimestory
from guardian_agent import guardian_agent, StoryEvaluation


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
    topics_to_avoid: str | None = Field(
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
    MAX_REVISIONS_ATTEMPTS = 3

    async def run(self, user_input: UserInput):
        """Run the story generation process, yielding status updates and the final story"""
        trace_id = gen_trace_id()
        with trace("Bedtime Story Creation", trace_id=trace_id):
            print(
                f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            )
            yield f"🔗 [View trace](https://platform.openai.com/traces/trace?trace_id={trace_id})"


            # Step 1: Plan searches
            yield "🎨 Planning your magical story..."
            search_plan = await self.plan_searches(user_input)
            yield f"📋 Theme: {search_plan.story_theme}"

            # Step 2: Perform searches
            yield "🔍 Researching inspiration..."
            research_results = await self.perform_searches(search_plan)
            yield f"✨ Found {len(research_results)} sources of inspiration"

            # Step 3: Write the story
            yield "✍️ Writing your bedtime story..."
            story = await self.write_story(user_input, research_results)
            yield f'📖 Draft complete: "{story.title}"'

            # Step 4: Evaluate the story
            yield "🛡️ Guardian is checking the story..."
            evaluation = await self.evaluate_story(story, user_input)

            attempts = 0
            while not evaluation.is_approved and attempts < self.MAX_REVISIONS_ATTEMPTS:
                attempts += 1
                print(f"Revising Story - Attempt {attempts}/{self.MAX_REVISIONS_ATTEMPTS}")
                story = await self.revise_story(story, user_input, evaluation)
                evaluation = await self.evaluate_story(story, user_input)

            # Final result
            if evaluation.is_approved:
                yield "✅ Story approved by Guardian!"
                yield f"⏱️ Reading time: ~{story.reading_time_in_minutes} minutes"
                yield f"💝 Moral: {story.moral_lesson}"
                if story.fun_fact_included:
                    yield f"🧠 Fun fact: {story.fun_fact_included}"
                yield "---"
                yield f"# {story.title}\n\n{story.story}"
            else:
                yield "❌ Could not create a safe story after multiple attempts."
                yield "Please try different inputs or avoid certain topics."
            

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
    

    async def evaluate_story(
            self, story: BedTimestory, user_input: UserInput
    ) -> StoryEvaluation:
        """Evaluate the story for quality, safety and appropriateness"""
        print("Evaluating story...")
        user_input_text = f"Evaluate this story based on these parameters:\
             story = {story}, \
             user's input = {user_input}"
        result = await Runner.run(guardian_agent, user_input_text)
        evaluation = result.final_output_as(StoryEvaluation)
        print("Story evaluation completed.")
        print(
            f"Evaluation: {'APPROVED' if evaluation.is_approved else 'REJECTED'}"
        )
        return evaluation
    
    async def revise_story(
            self,
            story: BedTimestory,
            evaluation: StoryEvaluation,
            user_input: UserInput,
            research_results: list[str]
    ) -> BedTimestory:
        """Revise the story based on the guardian's feedback"""
        print("Revising story...")
        user_input_text = f"Revise this bedtime story based on the following parameters:\
            user's input = {user_input}, \
            search results = {research_results}, \
            previous_story = {story}, \
            issues_to_fix = {evaluation.issues_found}\
            fix_instructions = {evaluation.fix_instructions}"
        
        result = await Runner.run(writer_agent, user_input_text)
        print("Story revision completed.")

        return result.final_output_as(BedTimestory)