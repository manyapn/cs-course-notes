import asyncio
from dotenv import load_dotenv
load_dotenv()

from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

retry_config=types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504], # Retry on these HTTP errors
)

# <-- basic multi-agent model -->

# # Research Agent: Its job is to use the google_search tool and present findings.
# research_agent = Agent(
#     name="ResearchAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""You are a specialized research agent. Your only job is to use the
#     google_search tool to find 2-3 pieces of relevant information on the given topic and present the findings with citations.""",
#     tools=[google_search],
#     output_key="research_findings",  # The result of this agent will be stored in the session state with this key.
# )

# # Summarizer Agent: Its job is to summarize the text it receives.
# summarizer_agent = Agent(
#     name="SummarizerAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # The instruction is modified to request a bulleted list for a clear output format.
#     instruction="""Read the provided research findings: {research_findings}
# Create a concise summary as a bulleted list with 3-5 key points.""",
#     output_key="final_summary",
# )

# root_agent = Agent(
#     name="ResearchCoordinator",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # This instruction tells the root agent HOW to use its tools (which are the other agents).
#     instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
# 1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
# 2. Next, after receiving the research findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
# 3. Finally, present the final summary clearly to the user as your response.""",
#     # We wrap the sub-agents in `AgentTool` to make them callable tools for the root agent.
#     tools=[AgentTool(research_agent), AgentTool(summarizer_agent)],
# )

# runner = InMemoryRunner(agent=root_agent)


# async def main():
#     response = await runner.run_debug(
#     "What are the latest advancements in quantum computing and what do they mean for AI?"
#     )
#     return response

# if __name__ == "__main__":
#     asyncio.run(main())
    
# <-- assembly line structure -->

# # Outline Agent: Creates the initial blog post outline.
# outline_agent = Agent(
#     name="OutlineAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""Create a blog outline for the given topic with:
#     1. A catchy headline
#     2. An introduction hook
#     3. 3-5 main sections with 2-3 bullet points for each
#     4. A concluding thought""",
#     output_key="blog_outline",  # The result of this agent will be stored in the session state with this key.
# )

# # Writer Agent: Writes the full blog post based on the outline from the previous agent.
# writer_agent = Agent(
#     name="WriterAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # The `{blog_outline}` placeholder automatically injects the state value from the previous agent's output.
#     instruction="""Following this outline strictly: {blog_outline}
#     Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
#     output_key="blog_draft",  # The result of this agent will be stored with this key.
# )

# # Editor Agent: Edits and polishes the draft from the writer agent.
# editor_agent = Agent(
#     name="EditorAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # This agent receives the `{blog_draft}` from the writer agent's output.
#     instruction="""Edit this draft: {blog_draft}
#     Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
#     output_key="final_blog",  # This is the final output of the entire pipeline.
# )

# validator_agent = Agent(
#     name="ValidatorAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""Count the words in {final_blog}. If it exceeds 300 words, rewrite it to be under 300 words. Return only the 
#     final post.""",
#     output_key="revised_final_blog",
# )

# root_agent = SequentialAgent(
#     name="BlogPipeline",
#     sub_agents=[outline_agent, writer_agent, editor_agent, validator_agent],
# )

# runner = InMemoryRunner(agent=root_agent)

# async def main():
#     response = await runner.run_debug(
#     "Write a blog post about the benefits of multi-agent systems for software developers"
#     )
#     return response

# if __name__ == "__main__":
#     asyncio.run(main())
    
# <-- parallel agents -->

# # Tech Researcher: Focuses on AI and ML trends.
# tech_researcher = Agent(
#     name="TechResearcher",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""Research the latest AI/ML trends. Include 3 key developments,
# the main companies involved, and the potential impact IN BULLET POINT FORMAT. Keep the report very concise (100 words).""",
#     tools=[google_search],
#     output_key="tech_research",  # The result of this agent will be stored in the session state with this key.
# )

# # Health Researcher: Focuses on medical breakthroughs.
# health_researcher = Agent(
#     name="HealthResearcher",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""Research recent medical breakthroughs. Include 3 significant advances,
# their practical applications, and estimated timelinesIN BULLET POINT FORMAT. Keep the report concise (100 words).""",
#     tools=[google_search],
#     output_key="health_research",  # The result will be stored with this key.
# )

# # Finance Researcher: Focuses on fintech trends.
# finance_researcher = Agent(
#     name="FinanceResearcher",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     instruction="""Research current fintech trends. Include 3 key trends,
# their market implications, and the future outlook IN BULLET POINT FORMAT. Keep the report concise (100 words).""",
#     tools=[google_search],
#     output_key="finance_research",  # The result will be stored with this key.
# )

# # The AggregatorAgent runs *after* the parallel step to synthesize the results.
# aggregator_agent = Agent(
#     name="AggregatorAgent",
#     model=Gemini(
#         model="gemini-2.5-flash-lite",
#         retry_options=retry_config
#     ),
#     # It uses placeholders to inject the outputs from the parallel agents, which are now in the session state.
#     instruction="""Combine these three research findings into a single executive summary, with each section IN BULLET POINT FORMAT:

#     **Technology Trends:**
#     {tech_research}
    
#     **Health Breakthroughs:**
#     {health_research}
    
#     **Finance Innovations:**
#     {finance_research}
    
#     Your summary should highlight common themes, surprising connections, and the most important key takeaways from all three reports. The final summary should be around 200 words.""",
#     output_key="executive_summary",  # This will be the final output of the entire system.
# )

# # The ParallelAgent runs all its sub-agents simultaneously.
# parallel_research_team = ParallelAgent(
#     name="ParallelResearchTeam",
#     sub_agents=[tech_researcher, health_researcher, finance_researcher],
# )

# # This SequentialAgent defines the high-level workflow: run the parallel team first, then run the aggregator.
# root_agent = SequentialAgent(
#     name="ResearchSystem",
#     sub_agents=[parallel_research_team, aggregator_agent],
# )

# runner = InMemoryRunner(agent=root_agent)

# async def main():
#     response = await runner.run_debug(
#         "Run the daily executive briefing on Tech, Health, and Finance"
#     )
#     return response

# if __name__ == "__main__":
#     asyncio.run(main())    
    
# <-- loop agent for continuous refinement -->

# This agent runs ONCE at the beginning to create the first draft.
initial_writer_agent = Agent(
    name="InitialWriterAgent",
    model=Gemini(
        model="gemini-2.0-flash",
        retry_options=retry_config
    ),
    instruction="""Based on the user's prompt, write the first draft of a short story (around 100-150 words).
    Output only the story text, with no introduction or explanation.""",
    output_key="current_story",  # Stores the first draft in the state.
)

# This agent's only job is to provide feedback or the approval signal. It has no tools.
critic_agent = Agent(
    name="CriticAgent",
    model=Gemini(
        model="gemini-2.0-flash",
        retry_options=retry_config
    ),
    instruction="""You are a constructive story critic. Review the story provided below.
    Story: {current_story}
    
    Evaluate the story's plot, characters, and pacing.
    - If the story is well-written and complete, you MUST respond with the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for improvement.""",
    output_key="critique",  # Stores the feedback in the state.
)

# This is the function that the RefinerAgent will call to exit the loop.
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the story is finished and no more changes are needed."""
    return {"status": "approved", "message": "Story approved. Exiting refinement loop."}

# This agent refines the story based on critique OR calls the exit_loop function.
refiner_agent = Agent(
    name="RefinerAgent",
    model=Gemini(
        model="gemini-2.0-flash",
        retry_options=retry_config
    ),
    instruction="""You are a story refiner. You have a story draft and critique.
    
    Story Draft: {current_story}
    Critique: {critique}
    
    Your task is to analyze the critique.
    - IF the critique is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the story draft to fully incorporate the feedback from the critique.""",
    output_key="current_story",  # It overwrites the story with the new, refined version.
    tools=[
        FunctionTool(exit_loop)
    ],  # The tool is now correctly initialized with the function reference.
)

# The LoopAgent contains the agents that will run repeatedly: Critic -> Refiner.
story_refinement_loop = LoopAgent(
    name="StoryRefinementLoop",
    sub_agents=[critic_agent, refiner_agent],
    max_iterations=2,  # Prevents infinite loops
)

# The root agent is a SequentialAgent that defines the overall workflow: Initial Write -> Refinement Loop.
root_agent = SequentialAgent(
    name="StoryPipeline",
    sub_agents=[initial_writer_agent, story_refinement_loop],
)

runner = InMemoryRunner(agent=root_agent)

async def main():
    response = await runner.run_debug(
        "Write a short story about a lighthouse keeper who discovers a mysterious, glowing map"
    )
    return response

if __name__ == "__main__":
    asyncio.run(main())