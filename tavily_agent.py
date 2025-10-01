'''import os
from pydantic_ai.agent import Agent
from pydantic_ai.common_tools.tavily import tavily_search_tool
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment
api_key = os.getenv('TAVILY_API_KEY')
assert api_key is not None

# Initialize the agent with Tavily tools
agent = Agent(
    'groq:deepseek-r1-distill-llama-70b',
    tools=[tavily_search_tool(api_key)],
    system_prompt='Search Tavily for the given query and return the results.'
)

# Example 1: Basic search for news
result = agent.run_sync('Tell me the top news in the GenAI world, give me links.')
print(result.output)'''