from strands import Agent
from strands.models import BedrockModel
from tools import cloudwatch_log_fetcher
from agent.config import load_prompt_config

def create_agent():
    bedrock_model= BedrockModel(
        model_id="anthropic.claude-3-haiku-20240307-v1:0",
        region_name="ap-southeast-2"
    )
    return Agent(model= bedrock_model,
                  tools=[cloudwatch_log_fetcher],
                system_prompt= load_prompt_config())