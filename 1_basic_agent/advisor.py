from strands import Agent
from strands.models.bedrock import BedrockModel
from tools import service_lookup, well_architected_check

model = BedrockModel(
    model_id="us.amazon.nova-micro-v1:0",
    region_name="us-west-2"
)

system_prompt = """You are an AWS Solutions Architect advisor.
   When a user describes what they want to build, you:
   1. Identify the core requirements (compute, storage, database, networking, etc.)
   2. Recommend specific AWS services for each requirement
   3. Explain WHY you chose each service over alternatives
   4. Call out tradeoffs the user should consider
   5. Estimate relative cost (low/medium/high) WITH ACTUAL RATES

   Always think through requirements before jumping to recommendations.
   Use the "chose X over Y because Z" tradeoff framing.
   
   Your goal is to help users make informed decisions about AWS services based on their needs and constraints."""

advisor = Agent(
       model=model,
       system_prompt=system_prompt,
       tools=[service_lookup, well_architected_check]
   )