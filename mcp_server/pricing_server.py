from fastmcp import FastMCP
import boto3
import json

# ============================================================
# MCP Server: AWS Pricing
# ============================================================
# This server exposes pricing tools via the MCP protocol.
# Any MCP-compatible agent can discover and use these tools.
# Think of it as a "menu" of pricing capabilities that any
# agent can read and call without custom integration code.
# ============================================================

mcp = FastMCP("AWS Pricing Server")

# AWS Pricing API only lives in us-east-1 and ap-south-1
pricing_client = boto3.client("pricing", region_name="us-east-1")

# All pricing tools assume this region rather than taking one as input --
# keeps the tool interface simple. Every response says so explicitly so it's
# never a silent assumption. The Pricing API's "location" filter wants the
# full region name, not the code.
DEFAULT_REGION = "us-east-1"
DEFAULT_REGION_NAME = "US East (N. Virginia)"

# ============================================================
# Service code mapping
# Users say "DynamoDB" but the API wants "AmazonDynamoDB"
# ============================================================

SERVICE_CODE_MAP = {
    "dynamodb": "AmazonDynamoDB",
    "s3": "AmazonS3",
    "lambda": "AWSLambda",
    "ec2": "AmazonEC2",
    "rds": "AmazonRDS",
    "aurora": "AmazonRDS",
    "sqs": "AWSQueueService",
    "sns": "AmazonSNS",
    "api gateway": "AmazonApiGateway",
    "apigateway": "AmazonApiGateway",
    "cloudfront": "AmazonCloudFront",
    "elasticache": "AmazonElastiCache",
    "ecs": "AmazonECS",
    "eks": "AmazonEKS",
    "kinesis": "AmazonKinesis",
    "bedrock": "AmazonBedrock",
}


def resolve_service_code(service_name: str) -> str:
    """Convert a human-friendly service name to the AWS Pricing API service code."""
    key = service_name.lower().strip().replace("amazon", "").replace("aws", "").strip()
    if key in SERVICE_CODE_MAP:
        return SERVICE_CODE_MAP[key]
    # If it looks like it's already a service code (e.g., "AmazonDynamoDB"), use as-is
    return service_name


def extract_pricing_details(price_item: dict) -> dict:
    """Pull the useful bits out of the nested AWS pricing JSON."""
    product = price_item.get("product", {})
    terms = price_item.get("terms", {})
    attributes = product.get("attributes", {})

    # Extract on-demand pricing
    on_demand = terms.get("OnDemand", {})
    price_dimensions = []
    for term_key, term_data in on_demand.items():
        for dim_key, dim_data in term_data.get("priceDimensions", {}).items():
            price_dimensions.append({
                "description": dim_data.get("description", ""),
                "unit": dim_data.get("unit", ""),
                "price_per_unit": dim_data.get("pricePerUnit", {}),
            })

    return {
        "product_family": product.get("productFamily", ""),
        "sku": product.get("sku", ""),
        "attributes": {
            "service_name": attributes.get("servicename", ""),
            "usage_type": attributes.get("usagetype", ""),
            "operation": attributes.get("operation", ""),
            "group": attributes.get("group", ""),
            "group_description": attributes.get("groupDescription", ""),
            "location": attributes.get("location", ""),
        },
        "on_demand_pricing": price_dimensions,
    }


# ============================================================
# Tool 1: Get Service Pricing
# ============================================================

@mcp.tool()
def get_service_pricing(service_name: str) -> dict:
    """Get current pricing for an AWS service.

    Retrieves real-time pricing data from the AWS Pricing API for a given service.
    Returns pricing dimensions, tiers, and free tier information where applicable.

    Always looks up pricing for the us-east-1 (N. Virginia) region -- see
    "region_assumed" in the response. That's fixed rather than a parameter to
    keep this tool simple; prices for most services are the same or very close
    across US regions anyway.

    Args:
        service_name: AWS service name (e.g., "DynamoDB", "S3", "Lambda", "EC2")

    Returns:
        Dictionary with pricing tiers, dimensions, and details.
    """
    service_code = resolve_service_code(service_name)

    try:
        response = pricing_client.get_products(
            ServiceCode=service_code,
            Filters=[
                {
                    "Type": "TERM_MATCH",
                    "Field": "location",
                    "Value": DEFAULT_REGION_NAME,
                }
            ],
            MaxResults=10,
        )

        prices = []
        for price_item_str in response.get("PriceList", []):
            item = json.loads(price_item_str)
            prices.append(extract_pricing_details(item))

        return {
            "service": service_code,
            "service_requested": service_name,
            "region_assumed": DEFAULT_REGION,
            "results_count": len(prices),
            "pricing": prices,
        }

    except Exception as e:
        return {
            "error": str(e),
            "service_requested": service_name,
            "service_code_used": service_code,
            "hint": "Check that the service name is correct. Available services: "
                    + ", ".join(SERVICE_CODE_MAP.keys()),
        }


# ============================================================
# Tool 2: Compare Service Costs
# ============================================================

# Simplified cost estimates per month
# These are approximations for quick comparison
COST_ESTIMATES = {
    "AmazonDynamoDB": {
        "per_request": 0.00000125,      # per read/write request unit
        "per_gb_storage": 0.25,          # per GB-month
        "free_tier_requests": 200_000_000,  # 25 RCU * 720 hrs * 3600s / 0.3s
        "free_tier_storage_gb": 25,
        "notes": "On-demand pricing. Provisioned capacity is cheaper for steady workloads.",
    },
    "AmazonS3": {
        "per_request": 0.0000004,        # per GET request (Standard)
        "per_gb_storage": 0.023,          # per GB-month (Standard)
        "free_tier_requests": 20_000,     # 20,000 GET
        "free_tier_storage_gb": 5,
        "notes": "Standard tier. Infrequent Access is $0.0125/GB, Glacier is $0.004/GB.",
    },
    "AWSLambda": {
        "per_request": 0.0000002,        # per request
        "per_gb_storage": 0,             # no storage
        "free_tier_requests": 1_000_000,
        "free_tier_storage_gb": 0,
        "notes": "Plus $0.0000166667 per GB-second of compute. 400,000 GB-seconds free/month.",
    },
    "AmazonEC2": {
        "per_request": 0,
        "per_gb_storage": 0.10,          # EBS gp3 per GB-month
        "hourly_rate": 0.0116,           # t3.micro on-demand
        "monthly_estimate": 8.35,        # t3.micro 720 hrs
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "t3.micro On-Demand. Reserved instances save up to 72%. Spot saves up to 90%.",
    },
    "AmazonRDS": {
        "per_request": 0,
        "per_gb_storage": 0.115,         # gp3 storage
        "hourly_rate": 0.017,            # db.t3.micro on-demand
        "monthly_estimate": 12.24,       # db.t3.micro 720 hrs
        "free_tier_requests": 0,
        "free_tier_storage_gb": 20,
        "notes": "db.t3.micro PostgreSQL On-Demand. Multi-AZ doubles the cost.",
    },
    "AmazonElastiCache": {
        "per_request": 0,
        "per_gb_storage": 0,
        "hourly_rate": 0.017,            # cache.t3.micro
        "monthly_estimate": 12.24,
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "cache.t3.micro Redis On-Demand. No storage charges, data is in-memory.",
    },
    "AmazonCloudFront": {
        "per_request": 0.0000001,        # per request (HTTPS)
        "per_gb_storage": 0,
        "per_gb_transfer": 0.085,        # per GB data transfer out
        "free_tier_requests": 10_000_000,
        "free_tier_storage_gb": 0,
        "notes": "Always-free tier: 1 TB transfer out, 10M requests/month.",
    },
    "AWSQueueService": {
        "per_request": 0.0000004,        # per request (standard)
        "per_gb_storage": 0,
        "free_tier_requests": 1_000_000,
        "free_tier_storage_gb": 0,
        "notes": "Standard queue. FIFO queue is $0.00000050 per request.",
    },
    "AmazonSNS": {
        "per_request": 0.0000005,        # $0.50 per 1M publish requests
        "per_gb_storage": 0,
        "free_tier_requests": 1_000_000,
        "free_tier_storage_gb": 0,
        "notes": "Publish requests only. Delivery to endpoints (SMS, email, mobile "
                 "push) is billed separately and not included here.",
    },
    "AmazonApiGateway": {
        "per_request": 0.0000035,        # REST API, $3.50 per 1M requests
        "per_gb_storage": 0,
        "free_tier_requests": 1_000_000,
        "free_tier_storage_gb": 0,
        "notes": "REST API tier. HTTP APIs are ~70% cheaper ($1.00/million). Free "
                 "tier is 12 months only for new accounts, not always-free.",
    },
    "AmazonECS": {
        "per_request": 0,
        "per_gb_storage": 0,
        "hourly_rate": 0.01234,
        "monthly_estimate": 8.88,        # Fargate 0.25 vCPU / 0.5GB, always-on
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "Fargate launch type, 0.25 vCPU / 0.5GB task running continuously. "
                 "EC2 launch type is billed as regular EC2 instances instead.",
    },
    "AmazonEKS": {
        "per_request": 0,
        "per_gb_storage": 0,
        "hourly_rate": 0.10,
        "monthly_estimate": 73.00,       # cluster management fee only
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "EKS cluster management fee only ($0.10/hr). Worker node compute "
                 "(EC2 or Fargate) is billed separately and not included here.",
    },
    "AmazonKinesis": {
        "per_request": 0.000000014,      # rough provisioned-mode PUT payload unit cost
        "per_gb_storage": 0,
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "Rough provisioned-mode shard estimate per PUT record. On-demand "
                 "mode bills per-GB ingested/retrieved instead and will differ "
                 "significantly.",
    },
    # Not a real AWS service code -- Aurora shares RDS's "AmazonRDS" pricing-API
    # code, but its instance sizes, storage, and I/O pricing are different enough
    # that reusing the standard RDS estimate would be wrong. See
    # resolve_cost_model_key().
    "AuroraMySQL": {
        "per_request": 0.0000002,        # $0.20 per 1M I/O requests
        "per_gb_storage": 0.10,
        "hourly_rate": 0.082,
        "monthly_estimate": 59.04,       # db.t3.medium, Aurora's smallest tier
        "free_tier_requests": 0,
        "free_tier_storage_gb": 0,
        "notes": "Aurora MySQL db.t3.medium On-Demand -- Aurora has no db.t3.micro "
                 "tier and no free tier, unlike standard RDS. Plus $0.20 per "
                 "million I/O requests.",
    },
}

# Services with a real AWS service code but a pricing model too variable for a
# flat per-request/per-GB estimate to be meaningful.
UNSUPPORTED_COST_MODEL_REASONS = {
    "AmazonBedrock": "Bedrock is billed per input/output token, and rates vary by "
                     "an order of magnitude between models (e.g. Claude vs Titan) "
                     "and between on-demand vs provisioned throughput. A single "
                     "request/storage estimate would be misleading -- use "
                     "get_service_pricing or the Bedrock pricing page for the "
                     "specific model.",
}


# Services actually priced per-instance, where a bigger instance costs more.
# Excludes flat fees (EKS's cluster management charge doesn't change with
# node size) and serverless/request-based services (DynamoDB, S3, Lambda,
# etc. -- "instance size" isn't a concept for them, so a size_hint is a no-op).
SIZE_SCALABLE_SERVICES = {"AmazonEC2", "AmazonRDS", "AmazonElastiCache", "AuroraMySQL", "AmazonECS"}

# Rough multiplier on the curated "small" instance cost per size tier --
# roughly matches how cost scales across a family (e.g. t3.micro -> t3.medium
# -> t3.xlarge). Deliberately approximate, same as the rest of COST_ESTIMATES,
# rather than hand-typing a new absolute dollar figure per tier per service.
SIZE_TIER_MULTIPLIERS = {
    "small": 1,
    "medium": 4,
    "large": 16,
}


def resolve_cost_model_key(service_name: str, service_code: str) -> str:
    """Pick which COST_ESTIMATES entry to price against.

    Usually this is just the real AWS service code, but Aurora shares RDS's
    "AmazonRDS" pricing-API code even though its cost profile is different, so
    it needs its own lookup key.
    """
    if "aurora" in service_name.lower():
        return "AuroraMySQL"
    return service_code


# Unit -> cost-model field, used by the generic live-pricing fallback below.
UNIT_FIELD_MAP = {
    "Hrs": "hourly_rate",
    "GB-Mo": "per_gb_storage",
    "Requests": "per_request",
}


def fetch_live_price_estimate(service_code: str) -> dict:
    """Best-effort price fetch for a service with no hand-curated COST_ESTIMATES
    entry, so coverage isn't capped at the curated list.

    Uses only a location filter (same as get_service_pricing) -- no
    instance-type/engine narrowing -- so it may land on an arbitrary SKU among
    many for multi-SKU services. Lower confidence than the curated table by
    design; that's the tradeoff for covering any AWS service code. Returns {}
    on any failure (no credentials, no network, no matching data) so callers
    can report "no data" cleanly instead of crashing.
    """
    try:
        response = pricing_client.get_products(
            ServiceCode=service_code,
            Filters=[{"Type": "TERM_MATCH", "Field": "location", "Value": DEFAULT_REGION_NAME}],
            MaxResults=20,
        )
    except Exception:
        return {}

    live_prices = {}
    for price_item_str in response.get("PriceList", []):
        try:
            item = json.loads(price_item_str)
        except (json.JSONDecodeError, TypeError):
            continue
        for dim in extract_pricing_details(item).get("on_demand_pricing", []):
            field = UNIT_FIELD_MAP.get(dim.get("unit"))
            usd = dim.get("price_per_unit", {}).get("USD")
            if not field or usd is None or field in live_prices:
                continue
            try:
                live_prices[field] = float(usd)
            except ValueError:
                continue
    return live_prices


def estimate_monthly_cost(
    service_code: str,
    monthly_requests: int,
    storage_gb: float,
    cost_model_key: str = None,
    size_hint: str = None,
) -> dict:
    """Estimate monthly cost for a service given usage parameters.

    Deliberately rough -- a ballpark for comparing options, not a precise
    bill. cost_model_key lets the COST_ESTIMATES lookup differ from the real
    AWS service_code (see resolve_cost_model_key) -- it defaults to
    service_code.

    Services in the hand-curated COST_ESTIMATES table get a "curated"
    estimate. Anything else falls back to a live, best-effort AWS Pricing API
    fetch (see fetch_live_price_estimate), always against DEFAULT_REGION, so
    this isn't capped at ~15 services -- that fallback is tagged
    "live_estimate" (lower confidence) since it isn't pinned to one specific
    instance type/tier.

    size_hint ("small"/"medium"/"large") scales the instance cost for
    per-instance services (see SIZE_SCALABLE_SERVICES) -- e.g. pass "small"
    for a project with a handful of users, "large" for one with heavy load.
    It's a no-op everywhere else (flat fees, serverless/request-based
    services); check "size_hint_applied" in the response to see whether it
    actually mattered for this service.
    """
    lookup_key = cost_model_key or service_code

    if lookup_key in UNSUPPORTED_COST_MODEL_REASONS:
        return {
            "estimated_monthly_cost": None,
            "error": UNSUPPORTED_COST_MODEL_REASONS[lookup_key],
        }

    if lookup_key in COST_ESTIMATES:
        pricing = COST_ESTIMATES[lookup_key]
        confidence = "curated"
    else:
        pricing = fetch_live_price_estimate(service_code)
        if not pricing:
            return {
                "estimated_monthly_cost": None,
                "error": f"No pricing data found for {service_code}",
            }
        confidence = "live_estimate"

    size_hint_applied = size_hint is not None and lookup_key in SIZE_SCALABLE_SERVICES
    size_multiplier = SIZE_TIER_MULTIPLIERS.get(size_hint, 1) if size_hint_applied else 1

    # Request costs
    billable_requests = max(0, monthly_requests - pricing.get("free_tier_requests", 0))
    request_cost = billable_requests * pricing.get("per_request", 0)

    # Storage costs
    billable_storage = max(0, storage_gb - pricing.get("free_tier_storage_gb", 0))
    storage_cost = billable_storage * pricing.get("per_gb_storage", 0)

    # Hourly instance costs (EC2, RDS, ElastiCache): curated entries carry a
    # precomputed monthly_estimate; live-fetched ones only have hourly_rate.
    # size_multiplier scales this up/down for a bigger/smaller instance tier.
    if "monthly_estimate" in pricing:
        instance_cost = pricing["monthly_estimate"] * size_multiplier
    else:
        instance_cost = pricing.get("hourly_rate", 0) * 720 * size_multiplier

    # Data transfer costs
    transfer_cost = storage_gb * pricing.get("per_gb_transfer", 0)

    total = request_cost + storage_cost + instance_cost + transfer_cost

    notes = pricing.get("notes", "")
    if confidence == "live_estimate" and not notes:
        notes = ("Derived from a live AWS Pricing API lookup with no specific "
                  "instance type/tier pinned down -- treat as a rough "
                  "order-of-magnitude figure, not a precise bill.")

    return {
        "service": service_code,
        "monthly_requests": monthly_requests,
        "storage_gb": storage_gb,
        "size_hint": size_hint,
        "size_hint_applied": size_hint_applied,
        "cost_breakdown": {
            "request_cost": round(request_cost, 4),
            "storage_cost": round(storage_cost, 4),
            "instance_cost": round(instance_cost, 4),
            "transfer_cost": round(transfer_cost, 4),
        },
        "estimated_monthly_cost": round(total, 2),
        "confidence": confidence,
        "notes": notes,
    }


DEFAULT_MONTHLY_REQUESTS = 1_000_000
DEFAULT_STORAGE_GB = 10.0


@mcp.tool()
def compare_service_costs(
    service_a: str,
    service_b: str,
    monthly_requests: int = None,
    storage_gb: float = None,
    size_hint: str = None,
) -> dict:
    """Compare estimated monthly costs between two AWS services.

    Takes two service names and usage parameters, then calculates and compares
    estimated monthly costs for each. Useful for deciding between alternatives
    like DynamoDB vs RDS, or S3 vs CloudFront for content delivery. Works for
    any AWS service, not just the hand-curated ones -- see estimate_monthly_cost.

    This is a rough ballpark for comparing options, not a precise bill -- it's
    meant to help someone exploring choices, not to replace the AWS Pricing
    Calculator. If usage isn't given, it falls back to reasonable defaults and
    says so in "assumptions_used" -- pass real numbers for a tighter estimate.
    Always assumes the us-east-1 region -- see "region_assumed" in the response.

    Args:
        service_a: First AWS service (e.g., "DynamoDB", "S3", "Lambda")
        service_b: Second AWS service (e.g., "RDS", "EFS", "EC2")
        monthly_requests: Expected number of API/read/write requests per month.
            Defaults to 1,000,000 if not given.
        storage_gb: Expected storage needed in GB. Defaults to 10.0 if not given.
        size_hint: "small", "medium", or "large" -- your judgment of how much
            compute the workload needs (e.g. a handful of users vs. heavy
            load). Only affects per-instance services (EC2, RDS, ElastiCache,
            Aurora, ECS); see each result's "size_hint_applied".

    Returns:
        Dictionary with cost breakdown for each service, savings, and a recommendation.
    """
    used_default_requests = monthly_requests is None
    used_default_storage = storage_gb is None
    monthly_requests = DEFAULT_MONTHLY_REQUESTS if used_default_requests else monthly_requests
    storage_gb = DEFAULT_STORAGE_GB if used_default_storage else storage_gb

    code_a = resolve_service_code(service_a)
    code_b = resolve_service_code(service_b)

    cost_a = estimate_monthly_cost(
        code_a, monthly_requests, storage_gb,
        cost_model_key=resolve_cost_model_key(service_a, code_a),
        size_hint=size_hint,
    )
    cost_b = estimate_monthly_cost(
        code_b, monthly_requests, storage_gb,
        cost_model_key=resolve_cost_model_key(service_b, code_b),
        size_hint=size_hint,
    )

    # Determine recommendation
    total_a = cost_a.get("estimated_monthly_cost")
    total_b = cost_b.get("estimated_monthly_cost")

    if total_a is not None and total_b is not None:
        if total_a < total_b:
            recommendation = service_a
            savings = round(total_b - total_a, 2)
            savings_pct = round((savings / total_b) * 100, 1) if total_b > 0 else 0
        elif total_b < total_a:
            recommendation = service_b
            savings = round(total_a - total_b, 2)
            savings_pct = round((savings / total_a) * 100, 1) if total_a > 0 else 0
        else:
            recommendation = "Either (same cost)"
            savings = 0
            savings_pct = 0
    else:
        recommendation = "Unable to compare (missing cost data)"
        savings = 0
        savings_pct = 0

    return {
        "comparison": {
            "service_a": {
                "name": service_a,
                "service_code": code_a,
                **cost_a,
            },
            "service_b": {
                "name": service_b,
                "service_code": code_b,
                **cost_b,
            },
        },
        "usage_params": {
            "monthly_requests": monthly_requests,
            "storage_gb": storage_gb,
        },
        "assumptions_used": {
            "monthly_requests": "default" if used_default_requests else "user-provided",
            "storage_gb": "default" if used_default_storage else "user-provided",
        },
        "region_assumed": DEFAULT_REGION,
        "recommendation": recommendation,
        "monthly_savings": savings,
        "savings_percentage": savings_pct,
        "disclaimer": "Rough, simplified estimates meant for comparing options, "
                      "not a precise bill. Actual costs vary by usage pattern, "
                      "instance type, and commitment level. Use AWS Pricing "
                      "Calculator for precise estimates.",
    }


# ============================================================
# Tool 3: Suggest Services Within Budget
# ============================================================

# Which service codes count as an option for a given kind of need. Only a
# handful of these (see COST_ESTIMATES) have a hand-curated cost model --
# the rest are priced via the live-fetch fallback in estimate_monthly_cost,
# which is what lets this list cover far more than the curated ~15 without
# hand-typing a pricing model for each one. The advisor agent is expected to
# map the user's freeform description to one of these categories -- this
# tool doesn't do that interpretation itself.
SERVICE_CATEGORIES = {
    "database": [
        "AmazonDynamoDB", "AmazonRDS", "AuroraMySQL", "AmazonElastiCache",
        "AmazonDocDB", "AmazonNeptune", "AmazonRedshift", "AmazonMemoryDB",
        "AmazonTimestream",
    ],
    "compute": [
        "AmazonEC2", "AmazonECS", "AmazonEKS", "AWSLambda",
        "AmazonLightsail", "AWSBatch",
    ],
    "storage": ["AmazonS3", "AmazonEFS", "AmazonFSx", "AmazonGlacier"],
    "messaging": ["AWSQueueService", "AmazonSNS", "AmazonMQ", "AmazonEventBridge"],
    "cdn": ["AmazonCloudFront", "AmazonRoute53", "AWSGlobalAccelerator"],
    "streaming": ["AmazonKinesis", "AmazonMSK"],
    "api": ["AmazonApiGateway", "AWSAppSync"],
}

# Overrides for service codes whose display name reads badly after a naive
# "strip Amazon/AWS" (e.g. "AWSQueueService" -> "QueueService").
FRIENDLY_NAME_OVERRIDES = {
    "AuroraMySQL": "Aurora (MySQL)",
    "AWSQueueService": "SQS",
}


def friendly_service_name(cost_model_key: str) -> str:
    """Human-readable label for a service code, for display in suggestions."""
    if cost_model_key in FRIENDLY_NAME_OVERRIDES:
        return FRIENDLY_NAME_OVERRIDES[cost_model_key]
    return cost_model_key.replace("Amazon", "").replace("AWS", "") or cost_model_key


@mcp.tool()
def suggest_services_within_budget(
    category: str,
    monthly_budget: float,
    monthly_requests: int = None,
    storage_gb: float = None,
    size_hint: str = None,
) -> dict:
    """Suggest AWS services in a category, ranked against a monthly budget.

    Give this a category of need (e.g. "database", "compute") and a monthly
    budget. It estimates the monthly cost of every service in that category
    (same rough ballpark model as compare_service_costs, not a precise bill --
    a mix of hand-curated and live-fetched estimates, see each result's
    "confidence") and returns them sorted cheapest to priciest, each flagged
    as fitting the budget or not -- so a too-low budget still returns useful
    options instead of nothing. Always assumes the us-east-1 region -- see
    "region_assumed" in the response.

    Args:
        category: One of: database, compute, storage, messaging, cdn, streaming, api
        monthly_budget: Target monthly budget in USD
        monthly_requests: Expected requests/month. Defaults to 1,000,000 if not given.
        storage_gb: Expected storage in GB. Defaults to 10.0 if not given.
        size_hint: "small", "medium", or "large" -- your judgment of how much
            compute the workload needs (e.g. a handful of users vs. heavy
            load). Only affects per-instance services (EC2, RDS, ElastiCache,
            Aurora, ECS); see each suggestion's "size_hint_applied".

    Returns:
        Dictionary with ranked service suggestions, each with estimated
        monthly cost and whether it fits the budget.
    """
    category_key = category.lower().strip()
    if category_key not in SERVICE_CATEGORIES:
        return {
            "error": f"Unknown category '{category}'",
            "available_categories": list(SERVICE_CATEGORIES.keys()),
        }

    used_default_requests = monthly_requests is None
    used_default_storage = storage_gb is None
    monthly_requests = DEFAULT_MONTHLY_REQUESTS if used_default_requests else monthly_requests
    storage_gb = DEFAULT_STORAGE_GB if used_default_storage else storage_gb

    suggestions = []
    for cost_model_key in SERVICE_CATEGORIES[category_key]:
        cost = estimate_monthly_cost(cost_model_key, monthly_requests, storage_gb, size_hint=size_hint)
        estimated = cost.get("estimated_monthly_cost")
        if estimated is None:
            continue  # no pricing data available for this service -- skip rather than error out
        suggestions.append({
            "service": friendly_service_name(cost_model_key),
            "service_code": cost_model_key,
            "estimated_monthly_cost": estimated,
            "fits_budget": estimated <= monthly_budget,
            "size_hint_applied": cost.get("size_hint_applied"),
            "confidence": cost.get("confidence"),
            "notes": cost.get("notes", ""),
        })

    suggestions.sort(key=lambda s: s["estimated_monthly_cost"])

    return {
        "category": category_key,
        "monthly_budget": monthly_budget,
        "usage_params": {
            "monthly_requests": monthly_requests,
            "storage_gb": storage_gb,
        },
        "assumptions_used": {
            "monthly_requests": "default" if used_default_requests else "user-provided",
            "storage_gb": "default" if used_default_storage else "user-provided",
        },
        "region_assumed": DEFAULT_REGION,
        "suggestions": suggestions,
        "disclaimer": "Rough, simplified estimates meant for comparing options, "
                      "not a precise bill. Actual costs vary by usage pattern, "
                      "instance type, and commitment level.",
    }


# ============================================================
# Run the server
# ============================================================

if __name__ == "__main__":
    mcp.run()