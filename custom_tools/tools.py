from strands import tool


# ============================================================
# Tool 1: Service Lookup
# ============================================================

SERVICES_DB = {
    "dynamodb": {
        "name": "Amazon DynamoDB",
        "category": "Database",
        "description": "Fully managed NoSQL key-value and document database",
        "use_cases": [
            "High-throughput applications",
            "Serverless backends",
            "Session management",
            "Gaming leaderboards",
            "IoT data ingestion"
        ],
        "key_features": [
            "Single-digit millisecond latency at any scale",
            "Auto-scaling with on-demand or provisioned capacity",
            "Global tables for multi-region replication",
            "Built-in backup and point-in-time recovery",
            "DynamoDB Streams for event-driven architectures"
        ],
        "limits": {
            "max_item_size": "400 KB",
            "max_partition_throughput": "3000 RCU / 1000 WCU",
            "max_table_size": "No limit",
            "max_indexes_per_table": "20 GSI, 5 LSI"
        },
        "pricing_model": "On-demand: per read/write request. Provisioned: per RCU/WCU hour.",
        "free_tier": "25 GB storage, 25 RCU, 25 WCU (always free)",
        "best_for": "Key-value lookups, high write throughput, serverless apps",
        "not_ideal_for": "Complex joins, ad-hoc SQL queries, small projects needing relational data",
        "alternatives": ["Aurora", "ElastiCache", "DocumentDB", "Neptune"]
    },
    "s3": {
        "name": "Amazon S3",
        "category": "Storage",
        "description": "Object storage with 99.999999999% (11 nines) durability",
        "use_cases": [
            "Static website hosting",
            "Data lake storage",
            "Backup and disaster recovery",
            "Media and content distribution",
            "Application asset storage"
        ],
        "key_features": [
            "Multiple storage classes (Standard, IA, Glacier, Deep Archive)",
            "Lifecycle policies for automatic tier transitions",
            "Versioning and cross-region replication",
            "Event notifications to Lambda, SQS, SNS",
            "S3 Select for querying data in place"
        ],
        "limits": {
            "max_object_size": "5 TB",
            "max_bucket_count": "100 per account (soft limit)",
            "max_put_size_single": "5 GB (use multipart for larger)",
            "request_rate": "5,500 GET/s, 3,500 PUT/s per prefix"
        },
        "pricing_model": "Per GB stored + per request + data transfer out",
        "free_tier": "5 GB Standard storage, 20,000 GET, 2,000 PUT (12 months)",
        "best_for": "Any unstructured data, static assets, data lakes, backups",
        "not_ideal_for": "Frequently updated files, POSIX file system access, low-latency random reads",
        "alternatives": ["EFS", "EBS", "FSx", "Storage Gateway"]
    },
    "lambda": {
        "name": "AWS Lambda",
        "category": "Compute",
        "description": "Serverless compute that runs code in response to events",
        "use_cases": [
            "API backends with API Gateway",
            "Real-time file processing",
            "Stream processing with Kinesis",
            "Scheduled tasks (cron jobs)",
            "Event-driven microservices"
        ],
        "key_features": [
            "No servers to manage",
            "Scales automatically from 0 to thousands of concurrent executions",
            "Pay only for compute time consumed",
            "Supports Python, Node.js, Java, Go, .NET, Ruby",
            "Built-in integration with 200+ AWS services"
        ],
        "limits": {
            "max_timeout": "15 minutes",
            "max_memory": "10,240 MB",
            "deployment_package": "50 MB zipped, 250 MB unzipped",
            "concurrent_executions": "1,000 (soft limit, can increase)",
            "tmp_storage": "512 MB to 10,240 MB"
        },
        "pricing_model": "Per request + per GB-second of compute",
        "free_tier": "1M requests, 400,000 GB-seconds per month (always free)",
        "best_for": "Event-driven workloads, short-duration tasks, variable traffic",
        "not_ideal_for": "Long-running processes (>15 min), high-performance computing, stateful apps",
        "alternatives": ["ECS Fargate", "EC2", "App Runner", "Step Functions"]
    },
    "ec2": {
        "name": "Amazon EC2",
        "category": "Compute",
        "description": "Virtual servers in the cloud with full OS-level control",
        "use_cases": [
            "Web application hosting",
            "Batch processing",
            "Machine learning training",
            "Development and test environments",
            "High-performance computing"
        ],
        "key_features": [
            "Wide selection of instance types (compute, memory, GPU, storage optimized)",
            "Auto Scaling groups for elasticity",
            "Spot instances for up to 90% cost savings",
            "Placement groups for low-latency networking",
            "EBS volumes for persistent block storage"
        ],
        "limits": {
            "default_instance_limit": "Varies by instance type and region",
            "max_ebs_volumes_per_instance": "28",
            "max_security_groups_per_instance": "5",
            "max_elastic_ips": "5 per region (soft limit)"
        },
        "pricing_model": "Per hour or per second by instance type. On-Demand, Reserved, Spot, Savings Plans.",
        "free_tier": "750 hours/month of t2.micro or t3.micro (12 months)",
        "best_for": "Full control over OS, long-running workloads, GPU needs, legacy apps",
        "not_ideal_for": "Simple APIs (use Lambda), containers (use ECS/EKS), static sites (use S3)",
        "alternatives": ["Lambda", "ECS", "Lightsail", "App Runner"]
    },
    "rds": {
        "name": "Amazon RDS",
        "category": "Database",
        "description": "Managed relational database service supporting multiple engines",
        "use_cases": [
            "Traditional web applications",
            "E-commerce platforms",
            "ERP and CRM systems",
            "Applications requiring complex queries and joins",
            "ACID-compliant transaction processing"
        ],
        "key_features": [
            "Supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server",
            "Automated backups and point-in-time recovery",
            "Multi-AZ deployments for high availability",
            "Read replicas for read scaling",
            "Automated patching and maintenance"
        ],
        "limits": {
            "max_storage": "64 TB (depending on engine)",
            "max_read_replicas": "5 (15 for Aurora)",
            "max_connections": "Varies by instance class",
            "max_databases_per_instance": "Varies by engine"
        },
        "pricing_model": "Per instance hour + storage + I/O + data transfer",
        "free_tier": "750 hours/month of db.t2.micro or db.t3.micro (12 months)",
        "best_for": "Relational data, complex queries, ACID compliance, existing SQL apps",
        "not_ideal_for": "Key-value lookups (use DynamoDB), unstructured data, massive write throughput",
        "alternatives": ["Aurora", "DynamoDB", "Redshift", "DocumentDB"]
    },
    "aurora": {
        "name": "Amazon Aurora",
        "category": "Database",
        "description": "MySQL and PostgreSQL-compatible relational database with up to 5x performance improvement",
        "use_cases": [
            "Enterprise applications",
            "SaaS platforms",
            "High-availability production databases",
            "Applications migrating from commercial databases",
            "Read-heavy workloads"
        ],
        "key_features": [
            "5x throughput of standard MySQL, 3x of PostgreSQL",
            "Up to 15 read replicas with sub-10ms replica lag",
            "Aurora Serverless for variable workloads",
            "Global Database for cross-region disaster recovery",
            "Storage auto-scales up to 128 TB"
        ],
        "limits": {
            "max_storage": "128 TB auto-scaling",
            "max_read_replicas": "15",
            "max_connections": "Varies by instance class",
            "failover_time": "Under 30 seconds"
        },
        "pricing_model": "Per instance hour + I/O + storage. Serverless: per ACU-hour.",
        "free_tier": "None (but Aurora Serverless v2 scales to near-zero)",
        "best_for": "Production relational workloads, high availability, read-heavy apps",
        "not_ideal_for": "Simple key-value data, budget-constrained projects, NoSQL workloads",
        "alternatives": ["RDS", "DynamoDB", "Redshift"]
    },
    "sqs": {
        "name": "Amazon SQS",
        "category": "Application Integration",
        "description": "Fully managed message queuing service for decoupling microservices",
        "use_cases": [
            "Decoupling microservices",
            "Buffering requests for batch processing",
            "Order processing systems",
            "Fan-out with SNS",
            "Handling traffic spikes"
        ],
        "key_features": [
            "Standard queues (nearly unlimited throughput) and FIFO queues (ordering guarantee)",
            "Dead-letter queues for failed message handling",
            "Long polling to reduce empty responses",
            "Message retention up to 14 days",
            "Server-side encryption"
        ],
        "limits": {
            "max_message_size": "256 KB (use S3 for larger)",
            "max_retention": "14 days",
            "fifo_throughput": "300 msg/s (3,000 with batching)",
            "standard_throughput": "Nearly unlimited"
        },
        "pricing_model": "Per million requests. First 1M requests/month free.",
        "free_tier": "1 million requests/month (always free)",
        "best_for": "Async processing, decoupling, buffering, reliable message delivery",
        "not_ideal_for": "Real-time streaming (use Kinesis), pub/sub fan-out (use SNS), complex routing",
        "alternatives": ["SNS", "Kinesis", "EventBridge", "MQ"]
    },
    "apigateway": {
        "name": "Amazon API Gateway",
        "category": "Networking",
        "description": "Fully managed service to create, publish, and manage APIs at any scale",
        "use_cases": [
            "REST API backends",
            "WebSocket APIs for real-time apps",
            "HTTP APIs (simpler, cheaper alternative to REST)",
            "API versioning and stage management",
            "Microservices API facade"
        ],
        "key_features": [
            "Built-in throttling and rate limiting",
            "API key management and usage plans",
            "Request/response transformation",
            "Lambda authorizers and Cognito integration",
            "Caching to reduce backend calls"
        ],
        "limits": {
            "max_timeout": "30 seconds (REST), 30 seconds (HTTP)",
            "max_payload": "10 MB",
            "throttle_limit": "10,000 requests/second (account level)",
            "max_apis": "600 REST APIs per region"
        },
        "pricing_model": "Per million API calls + data transfer + caching",
        "free_tier": "1 million REST API calls/month (12 months)",
        "best_for": "Serverless API backends, managed API lifecycle, rate limiting",
        "not_ideal_for": "Long-running connections (>30s), large payloads, gRPC",
        "alternatives": ["ALB", "AppSync", "CloudFront Functions"]
    },
    "elasticache": {
        "name": "Amazon ElastiCache",
        "category": "Database",
        "description": "Managed in-memory caching service supporting Redis and Memcached",
        "use_cases": [
            "Database query caching",
            "Session stores",
            "Real-time leaderboards",
            "Rate limiting",
            "Pub/sub messaging (Redis)"
        ],
        "key_features": [
            "Sub-millisecond response times",
            "Redis: data structures, persistence, replication, pub/sub",
            "Memcached: simple key-value, multi-threaded",
            "Cluster mode for horizontal scaling (Redis)",
            "Automatic failover with Multi-AZ"
        ],
        "limits": {
            "max_node_types": "Varies (up to 635 GB RAM per node)",
            "max_nodes_per_cluster": "500 (Redis cluster mode)",
            "max_connections": "65,000 per node",
            "max_item_size": "512 MB (Redis)"
        },
        "pricing_model": "Per node hour by instance type + data transfer",
        "free_tier": "750 hours/month of cache.t2.micro or cache.t3.micro (12 months)",
        "best_for": "Caching database queries, session management, sub-millisecond reads",
        "not_ideal_for": "Primary data store, large datasets, persistent-only storage",
        "alternatives": ["DynamoDB DAX", "MemoryDB", "DynamoDB"]
    },
    "cloudfront": {
        "name": "Amazon CloudFront",
        "category": "Networking",
        "description": "Global content delivery network (CDN) for low-latency content distribution",
        "use_cases": [
            "Static website acceleration",
            "API acceleration",
            "Video streaming",
            "Software distribution",
            "DDoS protection with AWS Shield"
        ],
        "key_features": [
            "450+ edge locations worldwide",
            "Lambda@Edge and CloudFront Functions for edge compute",
            "Origin Access Control for S3 security",
            "Real-time logs and metrics",
            "HTTPS with free SSL/TLS certificates"
        ],
        "limits": {
            "max_file_size": "30 GB per file",
            "max_distributions": "200 per account",
            "request_timeout": "30 seconds (to origin)",
            "max_cache_behaviors": "25 per distribution"
        },
        "pricing_model": "Per GB data transfer out + per 10,000 requests",
        "free_tier": "1 TB data transfer out, 10M requests/month (always free)",
        "best_for": "Global content delivery, static site hosting, API acceleration",
        "not_ideal_for": "Dynamic content that can't be cached, internal-only applications",
        "alternatives": ["Global Accelerator", "S3 Transfer Acceleration"]
    },
    "ecs": {
        "name": "Amazon ECS",
        "category": "Containers",
        "description": "Fully managed container orchestration service",
        "use_cases": [
            "Microservices architectures",
            "Batch processing with containers",
            "Application modernization",
            "CI/CD pipelines",
            "Machine learning inference"
        ],
        "key_features": [
            "Two launch types: EC2 (you manage instances) and Fargate (serverless)",
            "Deep AWS integration (ALB, CloudWatch, IAM, Secrets Manager)",
            "Service auto-scaling",
            "Task definitions for container configuration",
            "Support for Docker containers"
        ],
        "limits": {
            "max_tasks_per_service": "5,000",
            "max_containers_per_task": "10",
            "fargate_max_vcpu": "16 vCPU per task",
            "fargate_max_memory": "120 GB per task"
        },
        "pricing_model": "EC2 launch type: pay for EC2 instances. Fargate: per vCPU-hour + per GB-hour.",
        "free_tier": "No ECS charge (pay only for EC2/Fargate resources used)",
        "best_for": "Dockerized apps, microservices, teams already using containers",
        "not_ideal_for": "Simple functions (use Lambda), non-containerized apps, Kubernetes-required (use EKS)",
        "alternatives": ["EKS", "Lambda", "App Runner", "Lightsail Containers"]
    },
    "cognito": {
        "name": "Amazon Cognito",
        "category": "Security",
        "description": "User authentication, authorization, and user management for web and mobile apps",
        "use_cases": [
            "User sign-up and sign-in",
            "Social login (Google, Facebook, Apple)",
            "Enterprise SSO with SAML/OIDC",
            "API authorization with JWT tokens",
            "Multi-factor authentication"
        ],
        "key_features": [
            "User Pools for authentication (sign-up, sign-in, MFA)",
            "Identity Pools for AWS resource access (temporary credentials)",
            "Built-in hosted UI for login pages",
            "Lambda triggers for custom auth flows",
            "Token-based auth with JWT"
        ],
        "limits": {
            "max_user_pools": "1,000 per account",
            "max_users_per_pool": "40 million",
            "max_groups_per_pool": "10,000",
            "token_expiry": "5 min to 1 day (access token)"
        },
        "pricing_model": "Per monthly active user (MAU). Tiered pricing.",
        "free_tier": "50,000 MAUs (always free for User Pools)",
        "best_for": "App authentication, social login, serverless auth, mobile apps",
        "not_ideal_for": "Complex enterprise IAM (use IAM Identity Center), machine-to-machine auth",
        "alternatives": ["IAM Identity Center", "Third-party (Auth0, Okta)"]
    }
}


@tool
def service_lookup(service_name: str) -> dict:
    """Look up detailed information about an AWS service.

    Use this tool when you need accurate, specific details about an AWS service
    including its capabilities, common use cases, limits, pricing model,
    and how it compares to alternatives.

    Args:
        service_name: The AWS service to look up (e.g., "DynamoDB", "S3", "Lambda",
                      "EC2", "RDS", "Aurora", "SQS", "API Gateway", "ElastiCache",
                      "CloudFront", "ECS", "Cognito")

    Returns:
        Dictionary with service details including description, use_cases,
        key_features, limits, pricing_model, and alternatives.
    """
    print(f"\n>>> TOOL CALLED: service_lookup('{service_name}')")
    
    # Normalize the input to match our keys
    key = (
        service_name.lower()
        .strip()
        .replace(" ", "")
        .replace("amazon", "")
        .replace("aws", "")
        .replace("api gateway", "apigateway")
        .replace("api_gateway", "apigateway")
    )

    # Try direct match first
    if key in SERVICES_DB:
        return SERVICES_DB[key]

    # Try partial matching
    for db_key, service_data in SERVICES_DB.items():
        if key in db_key or db_key in key:
            return service_data
        if key in service_data["name"].lower().replace(" ", ""):
            return service_data

    available = [s["name"] for s in SERVICES_DB.values()]
    return {
        "error": f"Service '{service_name}' not found in the database.",
        "available_services": available,
        "suggestion": "Try one of the available services listed above."
    }


# ============================================================
# Tool 2: Well-Architected Checker
# ============================================================

WELL_ARCHITECTED = {
    "operational_excellence": {
        "pillar": "Operational Excellence",
        "description": "Run and monitor systems to deliver business value and continually improve",
        "key_questions": [
            "Is infrastructure defined as code (CloudFormation, CDK, Terraform)?",
            "Are there automated deployment pipelines (CI/CD)?",
            "Is logging and monitoring configured (CloudWatch, X-Ray)?",
            "Are there runbooks for common operational procedures?",
            "Are changes made through small, reversible deployments?"
        ],
        "common_gaps": [
            "Manual deployments instead of CI/CD",
            "No centralized logging",
            "Missing CloudWatch alarms for key metrics",
            "No runbooks or playbooks for incident response",
            "Large, infrequent deployments instead of small, frequent ones"
        ],
        "recommendations": [
            "Use CloudFormation or CDK for infrastructure as code",
            "Set up CodePipeline/CodeDeploy for automated deployments",
            "Configure CloudWatch dashboards and alarms",
            "Enable X-Ray for distributed tracing",
            "Implement blue/green or canary deployments"
        ]
    },
    "security": {
        "pillar": "Security",
        "description": "Protect information, systems, and assets through risk assessment and mitigation",
        "key_questions": [
            "Is data encrypted at rest and in transit?",
            "Are IAM roles following least privilege?",
            "Is there a VPC with proper security groups and NACLs?",
            "Are secrets managed through Secrets Manager or Parameter Store?",
            "Is multi-factor authentication enabled for root and IAM users?"
        ],
        "common_gaps": [
            "Hardcoded credentials in code or environment variables",
            "Overly permissive IAM policies (e.g., Action: '*')",
            "Public S3 buckets or security groups open to 0.0.0.0/0",
            "No encryption at rest on databases or storage",
            "Root account used for daily operations"
        ],
        "recommendations": [
            "Use IAM roles instead of access keys wherever possible",
            "Store secrets in Secrets Manager with automatic rotation",
            "Enable encryption at rest on all data stores (S3, RDS, DynamoDB)",
            "Restrict security groups to specific IPs and ports",
            "Enable CloudTrail for API audit logging"
        ]
    },
    "reliability": {
        "pillar": "Reliability",
        "description": "Ensure a system can recover from failures and meet demand",
        "key_questions": [
            "Does the architecture span multiple Availability Zones?",
            "Is there auto-scaling configured for variable load?",
            "Are there health checks and automatic recovery?",
            "Is data backed up with defined RPO/RTO?",
            "Is there a disaster recovery plan?"
        ],
        "common_gaps": [
            "Single AZ deployment (one AZ failure takes everything down)",
            "No auto-scaling policy",
            "No health checks on load balancer targets",
            "No automated backups or undefined recovery objectives",
            "Single points of failure (one NAT Gateway, one database instance)"
        ],
        "recommendations": [
            "Deploy across at least 2 Availability Zones",
            "Use Auto Scaling groups with appropriate scaling policies",
            "Configure ALB health checks on application endpoints",
            "Enable automated backups with defined RPO/RTO",
            "Use Multi-AZ for RDS, DynamoDB Global Tables for multi-region"
        ]
    },
    "performance_efficiency": {
        "pillar": "Performance Efficiency",
        "description": "Use computing resources efficiently to meet requirements and maintain efficiency as demand changes",
        "key_questions": [
            "Is the right compute option selected for the workload (EC2 vs Lambda vs containers)?",
            "Is caching implemented where appropriate (ElastiCache, CloudFront, DAX)?",
            "Is the database engine appropriate for the access patterns?",
            "Are resources right-sized (not over or under-provisioned)?",
            "Is content delivered from edge locations where needed?"
        ],
        "common_gaps": [
            "Using EC2 for simple event-driven tasks (should be Lambda)",
            "No caching layer for repeated database queries",
            "Wrong database type for access patterns (SQL for key-value lookups)",
            "Over-provisioned instances running at low utilization",
            "All traffic routed through a single region with no CDN"
        ],
        "recommendations": [
            "Match compute to workload: Lambda for events, Fargate for containers, EC2 for persistent",
            "Add ElastiCache or DAX for frequently accessed data",
            "Use CloudFront for static assets and API acceleration",
            "Right-size instances using AWS Compute Optimizer",
            "Use read replicas to offload read-heavy database queries"
        ]
    },
    "cost_optimization": {
        "pillar": "Cost Optimization",
        "description": "Avoid unnecessary costs and understand where money is being spent",
        "key_questions": [
            "Are there resources running that are not being used?",
            "Is the right pricing model used (On-Demand vs Reserved vs Spot vs Savings Plans)?",
            "Are S3 lifecycle policies moving infrequent data to cheaper tiers?",
            "Is there visibility into costs (Cost Explorer, Budgets)?",
            "Are development/test environments shut down when not in use?"
        ],
        "common_gaps": [
            "Idle EC2 instances or unattached EBS volumes",
            "All workloads on On-Demand pricing with no commitments",
            "S3 data sitting in Standard tier that is rarely accessed",
            "No AWS Budget alerts for cost anomalies",
            "Dev/test environments running 24/7"
        ],
        "recommendations": [
            "Use AWS Cost Explorer to identify spending patterns",
            "Purchase Savings Plans or Reserved Instances for steady-state workloads",
            "Set up S3 lifecycle policies to transition to IA or Glacier",
            "Create AWS Budget alerts for unexpected cost spikes",
            "Use Spot Instances for fault-tolerant workloads (batch, CI/CD)"
        ]
    },
    "sustainability": {
        "pillar": "Sustainability",
        "description": "Minimize environmental impact of running cloud workloads",
        "key_questions": [
            "Are resources right-sized to avoid waste?",
            "Are managed services used where possible (less idle capacity)?",
            "Is data classified by access frequency for efficient storage?",
            "Are workloads running in regions with lower carbon intensity?",
            "Are asynchronous and scheduled workloads batched efficiently?"
        ],
        "common_gaps": [
            "Over-provisioned resources running at low utilization",
            "Self-managed infrastructure when managed services exist",
            "All data stored in the same tier regardless of access frequency",
            "No consideration of region carbon intensity"
        ],
        "recommendations": [
            "Use Graviton-based instances for better performance per watt",
            "Prefer serverless and managed services over self-managed",
            "Implement data lifecycle policies",
            "Use AWS Customer Carbon Footprint Tool to track impact",
            "Batch asynchronous workloads to maximize utilization"
        ]
    }
}


@tool
def well_architected_check(architecture_description: str, pillar: str = "all") -> dict:
    """Check a proposed architecture against AWS Well-Architected Framework best practices.

    Use this tool when a user proposes an architecture and you need to validate
    it against AWS best practices. Identifies potential gaps and suggests improvements
    across the six pillars of the Well-Architected Framework.

    Args:
        architecture_description: Plain English description of the proposed architecture.
            Example: "EC2 in one AZ, RDS single instance, no load balancer"
        pillar: Which pillar to check. Options: "operational_excellence", "security",
                "reliability", "performance_efficiency", "cost_optimization",
                "sustainability", "all"

    Returns:
        Dictionary with key questions, common gaps, and recommendations per pillar.
    """
    print(f"\n>>> TOOL CALLED: well_architected_check(pillar='{pillar}')")

    if pillar == "all":
        result = {
            "architecture_reviewed": architecture_description,
            "framework_version": "2024",
            "pillars": {}
        }
        for pillar_key, pillar_data in WELL_ARCHITECTED.items():
            result["pillars"][pillar_key] = {
                "pillar_name": pillar_data["pillar"],
                "key_questions": pillar_data["key_questions"],
                "common_gaps": pillar_data["common_gaps"],
                "recommendations": pillar_data["recommendations"]
            }
        return result

    # Normalize pillar name
    normalized = pillar.lower().strip().replace(" ", "_")
    if normalized in WELL_ARCHITECTED:
        pillar_data = WELL_ARCHITECTED[normalized]
        return {
            "architecture_reviewed": architecture_description,
            "pillar_name": pillar_data["pillar"],
            "description": pillar_data["description"],
            "key_questions": pillar_data["key_questions"],
            "common_gaps": pillar_data["common_gaps"],
            "recommendations": pillar_data["recommendations"]
        }

    available = [p["pillar"] for p in WELL_ARCHITECTED.values()]
    return {
        "error": f"Unknown pillar: '{pillar}'",
        "available_pillars": available
    }