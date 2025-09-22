from pydantic_ai import Agent
from pydantic_ai.tools.tavily import tavily_search_tool
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from settings import Settings

settings = Settings()


console = Console()

model = GroqModel(
    'deepseek-r1-distill-llama-70b', provider=GroqProvider(api_key=settings.GROQ_API_KEY)
)
agent = Agent(
    model,
    tools=[tavily_search_tool(settings.TAVILY_API_KEY)],
    instructions='Explain in one brief paragraph.',
    )
...

console.print(Panel(
    Text("Hello There!", style="bold yellow"),
    title="Agent Chat",
    title_align="center"
))

while True:
    user_prompt = console.input("[bold green]You: [/]")
    
    if user_prompt.lower() == 'exit':
        console.print(Panel("Goodbye!", title="Agent", style="bold red"))
        break

    try:
        console.print(Panel(
            Text("Thinking...", style="italic dim"), 
            border_style="dim"
        ))

        result = agent.run_sync(user_prompt=user_prompt)
        
        agent_output = result.output
        console.print(Panel(
            Text(f"{agent_output}", style="cyan"), 
            title="Agent", 
            border_style="cyan"
        ))
    except Exception as e:
        console.print(Panel(
            Text(f"An error occurred: {e}", style="bold red"), 
            title="Error",
            border_style="red"
        ))