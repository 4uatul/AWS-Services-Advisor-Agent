# AWS Service Advisor Agent

A multi-agent system I built on AWS that acts as an architecture advisor. I describe what I want to build in plain English, things like "I need a database that handles 10,000 reads per second with low latency" or "compare S3 vs EFS for storing user uploads," and the system reasons through the options, pulls live pricing, checks best practices, and hands back a recommendation with tradeoffs.

I built this as a single project that covers the full agentic AI stack on AWS: Strands Agents SDK for writing agents, MCP for connecting agents to external tools, and Bedrock AgentCore for deploying and running them in production.

## Why I built this

This mirrors what Solutions Architects do for customers every day: take a vague requirement, reason through service tradeoffs, and back it up with real numbers. I wanted a project that walked through the entire agentic AI stack in one build instead of learning each piece in isolation, and I wanted it to double as strong SA interview material.

It also lines up directly with the AWS Summer in SLU GameDay (June 25, 2026), which covers Bedrock, AgentCore, Strands, and MCP.

## Architecture

```
User Query (plain English)
        |
        v
+---------------------------+
|   Orchestrator Agent      |  <-- Strands Agent (main entry point)
|   (AWS Service Advisor)   |
+---------------------------+
        |
        |--- Tool 1: AWS Service Lookup (built-in Strands tool)
        |--- Tool 2: MCP Pricing Server (custom MCP server)
        |--- Tool 3: Cost Analyzer Agent (agent-as-tool pattern)
        |--- Tool 4: Well-Architected Checker (built-in Strands tool)
        |
        v
+---------------------------+
|   AgentCore Runtime       |  <-- Deployment layer
|   + Gateway (MCP bridge)  |
|   + Managed Harness       |
|   + Observability         |
+---------------------------+
```

## How it works

### Strands Agents SDK

I used Strands to actually write the agent. The core idea is that an agent has three parts: a model, a system prompt, and a set of tools. The model decides when to use a tool, what order to do things in, and when it's done. There's no hardcoded control flow like you'd write in something like LangChain, the model itself is the control flow.

What I built with Strands:
- A single Service Advisor agent with multiple tools attached
- Custom tools for service lookup and Well-Architected best practices checking
- An agent-as-tool pattern, where a "Cost Analyzer" agent gets called as a tool by the main agent
- Multi-agent collaboration, where the orchestrator routes to specialist agents depending on the query

```python
from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(model_id="us.amazon.nova-micro-v1:0")

agent = Agent(
    model=model,
    system_prompt="You are an AWS Solutions Architect advisor...",
    tools=[service_lookup, pricing_tool, well_architected_check]
)

response = agent("I need a database for my app with low latency reads")
```

### MCP (Model Context Protocol)

MCP is what connects my agent to external tools without writing custom integration code for each one. I built a custom MCP server that wraps the AWS Pricing API and exposes two tools: `get_service_pricing` and `compare_service_costs`. I then connected that server through AgentCore Gateway so the deployed agent can use it.

```python
from fastmcp import FastMCP

mcp = FastMCP("AWS Pricing Server")

@mcp.tool()
def get_service_pricing(service_name: str, region: str = "us-west-2") -> dict:
    """Get current pricing for an AWS service."""
    ...

@mcp.tool()
def compare_service_costs(service_a: str, service_b: str, usage_params: dict) -> dict:
    """Compare costs between two AWS services for given usage parameters."""
    ...
```

### Bedrock AgentCore

AgentCore is where I deployed the agent once it worked locally. If Strands is where I wrote the code, AgentCore is where I shipped it.

What I used from AgentCore:
- **Managed Harness**: define the agent through config (model, prompt, tools) and run it immediately with no orchestration code, each session gets its own isolated microVM
- **Gateway**: bridges my custom MCP pricing server so the deployed agent can reach it securely
- **Observability**: lets me watch traces of the agent's reasoning in real time, which tools it called and why
- **AgentCore CLI**: one command-line workflow from prototype to deployment

## AWS services used

| Service | Purpose |
|---------|---------|
| Amazon Bedrock (Nova Micro) | Foundation model for agent reasoning |
| Bedrock AgentCore Runtime | Managed compute for the deployed agent |
| AgentCore Managed Harness | Config-based agent deployment |
| AgentCore Gateway | MCP bridge for tools |
| AgentCore Observability | Agent tracing and monitoring |
| AWS Lambda | Hosts the MCP server and custom tools |
| Amazon S3 | Stores service data and knowledge base docs |
| Amazon DynamoDB | Caches pricing data and session history |
| API Gateway | REST API for the frontend |
| CloudFront | CDN for the frontend |
| AWS Pricing API | Pulls real-time pricing data |

Total cost to run this end to end came out to a few dollars, mostly on Bedrock inference and AgentCore compute time. Everything else stays inside free tier limits.

Region: **us-west-2 (Oregon)**, for full access to all AgentCore capabilities including Runtime, Gateway, Identity, Memory, Observability, Evaluations, and Policy.

## Build phases

1. **Basic Strands agent** — got a single agent working with two custom tools (service lookup, Well-Architected check) and watched it reason through the agent loop
2. **Custom MCP server** — built and tested a standalone MCP pricing server, then wired it into the agent
3. **Multi-agent pattern** — added a Cost Analyzer agent and registered it as a tool the main agent can call
4. **AgentCore deployment** — deployed the full system through the managed harness, connected the MCP server via Gateway, and turned on Observability to review traces

## What I learned

- **Strands Agents SDK**: agent loop, tool use, system prompting, model-driven orchestration
- **MCP**: server creation, tool exposure, client-server architecture
- **Bedrock AgentCore**: managed harness deployment, Gateway MCP bridge, observability tracing, CLI workflow
- **Agent-as-tool pattern**: multi-agent collaboration, routing, specialist agents
- **Amazon Nova Micro**: working with a cost-optimized foundation model
- **AWS Pricing API**: pulling real-time AWS pricing programmatically

## Setup

```bash
# Install dependencies
pip install strands-agents strands-agents-tools
pip install fastmcp
pip install agentcore-cli

# Configure AWS credentials and confirm Bedrock access for Nova Micro
aws configure
```

Requires Python 3.11+ and an AWS account with Bedrock model access enabled for Nova Micro in your target region.

## References

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
- [Strands Tools](https://github.com/strands-agents/tools-python)
- [Amazon Bedrock AgentCore Docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/)
- [AgentCore Managed Harness](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/harness.html)
- [AgentCore Pricing](https://aws.amazon.com/bedrock/agentcore/pricing/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Amazon Bedrock Pricing](https://aws.amazon.com/bedrock/pricing/)
- [AWS Pricing API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/price-changes.html)
