from custom_tools.tools import service_lookup, well_architected_check
from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(model_id="us.amazon.nova-micro-v1:0", region_name="us-west-2")

advisor = Agent(
    model=model,
    system_prompt="You are an AWS Solutions Architect advisor...",
    tools=[service_lookup, well_architected_check]
)

# Test 1: Should call service_lookup
print("\n===== TEST 1: SERVICE LOOKUP =====")
advisor("Tell me about DynamoDB for a gaming leaderboard")

# Test 2: Should call well_architected_check
print("\n===== TEST 2: WELL-ARCHITECTED CHECK =====")
advisor("Review this: EC2 in one AZ, RDS single instance, no ALB")

# Test 3: Should use NO tools
print("\n===== TEST 3: NO TOOLS =====")
advisor("What is the difference between ALB and NLB?")