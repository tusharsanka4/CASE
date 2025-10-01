import discord
from discord.ext import commands
import os 
from dotenv import load_dotenv

# Import necessary components from your main file (or copy the setup)
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider
from pydantic_ai.common_tools.tavily import tavily_search_tool
# Assuming 'settings.py' and 'Settings' class are available
from settings import Settings 

# --- Pydantic-AI Agent Setup ---
load_dotenv()
settings = Settings()

# Setup the Model and Agent (Note: you only need this part, not the 'rich' console stuff)
model = GroqModel(
    'deepseek-r1-distill-llama-70b', provider=GroqProvider(api_key=settings.GROQ_API_KEY)
)
agent = Agent(
    model,
    tools=[tavily_search_tool(settings.TAVILY_API_KEY)],
    # The instruction ensures a brief paragraph output, suitable for a chat
    instructions='Explain in one brief paragraph.',
)
# -------------------------------

# --- Discord Bot Setup ---
TOKEN = os.getenv('DISCORD_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Check if the message starts with your desired prefix, e.g., '$ask'
    if message.content.startswith('$ask'):
        # 1. Extract the actual prompt from the user's message
        # We strip the command prefix (e.g., '$ask ')
        user_prompt = message.content[len('$ask'):].strip()
        
        if not user_prompt:
            await message.channel.send("Please provide a question after '$ask'.")
            return

        # Optional: Let the user know the bot is working
        await message.channel.send("Thinking...🤔") 
        
        try:
            # 2. Use the AGENT asynchronously to get the result
            # We use 'run' instead of 'run_sync' since we are in an async environment
            result = await agent.run(user_prompt=user_prompt)
            
            # 3. Get the output string
            agent_output = result.output
            
            # 4. Send the agent's output back to the Discord channel
            await message.channel.send(agent_output)

        except Exception as e:
            # Handle any potential errors during the API call or tool execution
            print(f"An error occurred: {e}")
            await message.channel.send(f"Sorry, an error occurred while processing your request: {e}")

# Run the client
client.run(TOKEN)