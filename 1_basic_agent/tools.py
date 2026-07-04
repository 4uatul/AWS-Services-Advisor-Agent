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
    },
    "sns": {
        "name": "Amazon SNS",
        "category": "Application Integration",
        "description": "Fully managed pub/sub messaging service for fan-out and application-to-application/person notifications",
        "use_cases": [
            "Fan-out to multiple SQS queues/Lambda functions",
            "Mobile push notifications",
            "SMS and email alerts",
            "Application alerting and monitoring",
            "Event-driven microservices"
        ],
        "key_features": [
            "Pub/sub topics with multiple subscriber types (SQS, Lambda, HTTP, email, SMS)",
            "Message filtering policies to route only relevant messages",
            "FIFO topics for ordered, deduplicated delivery",
            "Dead-letter queues for failed deliveries",
            "Message encryption at rest and in transit"
        ],
        "limits": {
            "max_message_size": "256 KB",
            "max_subscriptions_per_topic": "12.5 million",
            "fifo_throughput": "300 msg/s (3,000 with batching)",
            "max_topics": "100,000 per account"
        },
        "pricing_model": "Per million publish requests + per delivery (varies by protocol: SQS/Lambda cheap, SMS/email priced separately)",
        "free_tier": "1 million publishes/month (always free), plus 1,000 email and 100 SMS deliveries",
        "best_for": "Fan-out messaging, pub/sub patterns, decoupled notifications to multiple subscribers",
        "not_ideal_for": "Simple point-to-point queuing (use SQS), real-time streaming (use Kinesis)",
        "alternatives": ["SQS", "EventBridge", "Kinesis"]
    },
    "eks": {
        "name": "Amazon EKS",
        "category": "Containers",
        "description": "Managed Kubernetes service for running containerized applications without operating your own control plane",
        "use_cases": [
            "Running existing Kubernetes workloads on AWS",
            "Multi-cloud/hybrid Kubernetes strategies",
            "Complex microservices needing Kubernetes-native tooling",
            "ML training/inference pipelines (Kubeflow)",
            "Teams standardized on Kubernetes APIs"
        ],
        "key_features": [
            "Fully managed, highly available Kubernetes control plane",
            "Supports EC2 and Fargate node types",
            "Deep integration with IAM for pod-level permissions (IRSA)",
            "Native support for Helm, kubectl, and the broader K8s ecosystem",
            "EKS Add-ons for managing common cluster software"
        ],
        "limits": {
            "max_nodes_per_cluster": "Varies by instance type, thousands supported",
            "control_plane_fee": "$0.10/hour per cluster",
            "max_pods_per_node": "Varies by instance ENI limits",
            "supported_k8s_versions": "Typically last 4 minor versions"
        },
        "pricing_model": "Flat $0.10/hour cluster management fee + cost of underlying EC2/Fargate worker nodes",
        "free_tier": "None (no free tier for the cluster fee)",
        "best_for": "Teams already using Kubernetes, complex orchestration needs, portability across clouds",
        "not_ideal_for": "Simple containerized apps (use ECS, simpler and no cluster fee), small teams without K8s expertise",
        "alternatives": ["ECS", "Fargate", "App Runner"]
    },
    "kinesis": {
        "name": "Amazon Kinesis",
        "category": "Analytics",
        "description": "Real-time data streaming service for ingesting and processing large streams of data",
        "use_cases": [
            "Real-time analytics dashboards",
            "Log and clickstream aggregation",
            "IoT telemetry ingestion",
            "Real-time ETL pipelines",
            "Streaming machine learning inference"
        ],
        "key_features": [
            "Kinesis Data Streams for custom stream processing",
            "Kinesis Data Firehose for near-real-time delivery to S3/Redshift/OpenSearch",
            "On-demand or provisioned (shard-based) capacity modes",
            "Integrates with Lambda and Kinesis Data Analytics for SQL/Flink processing",
            "Data retention up to 365 days"
        ],
        "limits": {
            "max_record_size": "1 MB",
            "default_retention": "24 hours (up to 365 days)",
            "shard_write_throughput": "1,000 records/s or 1 MB/s per shard",
            "shard_read_throughput": "2 MB/s per shard"
        },
        "pricing_model": "Provisioned: per shard-hour + per PUT payload unit. On-demand: per GB ingested/retrieved.",
        "free_tier": "None",
        "best_for": "Real-time streaming ingestion, ordered processing, custom stream consumers",
        "not_ideal_for": "Simple pub/sub (use SNS/SQS), batch processing (use S3 + Glue), long-term storage of raw data",
        "alternatives": ["MSK", "SQS", "Firehose"]
    },
    "bedrock": {
        "name": "Amazon Bedrock",
        "category": "Machine Learning",
        "description": "Fully managed service to access foundation models (Claude, Titan, Llama, etc.) via a single API, without managing infrastructure",
        "use_cases": [
            "Building generative AI chat applications",
            "Document summarization and extraction",
            "Retrieval-augmented generation (RAG) pipelines",
            "AI agents with tool use",
            "Code generation and analysis"
        ],
        "key_features": [
            "Access to multiple foundation model providers through one API",
            "Knowledge Bases for RAG without managing a vector store separately",
            "Guardrails for content filtering and safety",
            "Agents for orchestrating multi-step tool-using workflows",
            "Provisioned Throughput for predictable latency at scale"
        ],
        "limits": {
            "context_window": "Varies by model (up to 200K+ tokens for some Claude models)",
            "max_output_tokens": "Varies by model",
            "rate_limits": "Per-model, per-account request/token quotas",
            "regions_available": "Growing subset of AWS regions"
        },
        "pricing_model": "Per input/output token (on-demand) or fixed hourly rate (Provisioned Throughput). Varies significantly by model.",
        "free_tier": "None (some models offer limited free trial credits)",
        "best_for": "Generative AI features, RAG applications, agentic workflows without managing model infrastructure",
        "not_ideal_for": "Simple deterministic logic better solved by regular code, ultra-low-latency needs below model response times",
        "alternatives": ["SageMaker (self-hosted models)", "Third-party APIs (OpenAI, Anthropic direct)"]
    },
    "redshift": {
        "name": "Amazon Redshift",
        "category": "Analytics",
        "description": "Fully managed, petabyte-scale data warehouse for analytics and business intelligence",
        "use_cases": [
            "Business intelligence and reporting",
            "Large-scale data warehousing",
            "Ad-hoc SQL analytics over historical data",
            "Data lake querying via Redshift Spectrum",
            "ETL and data transformation pipelines"
        ],
        "key_features": [
            "Columnar storage optimized for analytical queries",
            "Massively parallel processing (MPP) architecture",
            "Redshift Serverless for auto-scaling without managing clusters",
            "Redshift Spectrum to query data directly in S3",
            "Materialized views and result caching for fast repeated queries"
        ],
        "limits": {
            "max_databases_per_cluster": "Varies by node type",
            "max_table_columns": "1,600",
            "max_concurrent_queries": "Varies by workload management config",
            "max_cluster_size": "Up to 128 nodes (RA3)"
        },
        "pricing_model": "Per node-hour (provisioned) or per RPU-hour (Serverless), plus storage for RA3 nodes",
        "free_tier": "2 months free trial of a dc2.large node (750 hours total)",
        "best_for": "Large-scale analytical queries, BI dashboards, data warehousing over structured historical data",
        "not_ideal_for": "OLTP/transactional workloads, small datasets, low-latency single-row lookups",
        "alternatives": ["Athena", "EMR", "RDS"]
    },
    "documentdb": {
        "name": "Amazon DocumentDB",
        "category": "Database",
        "description": "Fully managed document database service compatible with MongoDB APIs",
        "use_cases": [
            "Content management systems",
            "Catalogs and user profile stores",
            "Mobile and web app backends using document models",
            "Migrating existing MongoDB workloads to AWS",
            "Applications needing flexible schema"
        ],
        "key_features": [
            "MongoDB 3.6/4.0/5.0 API compatibility",
            "Storage auto-scales up to 64 TB",
            "Up to 15 read replicas for read scaling",
            "Automated backups and point-in-time recovery",
            "Elastic Clusters for horizontal sharding"
        ],
        "limits": {
            "max_storage": "64 TB",
            "max_read_replicas": "15",
            "max_document_size": "16 MB (MongoDB-compatible limit)",
            "max_connections": "Varies by instance class"
        },
        "pricing_model": "Per instance hour + storage + I/O, similar to Aurora's model",
        "free_tier": "None",
        "best_for": "MongoDB-compatible document workloads, teams migrating existing MongoDB apps",
        "not_ideal_for": "Relational data with complex joins, budget-constrained small projects, non-MongoDB document needs (consider DynamoDB)",
        "alternatives": ["DynamoDB", "MongoDB Atlas", "RDS"]
    },
    "neptune": {
        "name": "Amazon Neptune",
        "category": "Database",
        "description": "Fully managed graph database service for highly connected data",
        "use_cases": [
            "Social networking and recommendation engines",
            "Fraud detection graphs",
            "Knowledge graphs and semantic search",
            "Network and IT infrastructure mapping",
            "Identity and access relationship graphs"
        ],
        "key_features": [
            "Supports both property graph (Gremlin, openCypher) and RDF (SPARQL) models",
            "Up to 15 read replicas with sub-second lag",
            "Storage auto-scales up to 128 TB",
            "Neptune ML for graph neural network predictions",
            "Full ACID transaction support"
        ],
        "limits": {
            "max_storage": "128 TB auto-scaling",
            "max_read_replicas": "15",
            "max_connections": "Varies by instance class",
            "supported_query_languages": "Gremlin, openCypher, SPARQL"
        },
        "pricing_model": "Per instance hour + storage + I/O, similar structure to Aurora",
        "free_tier": "None",
        "best_for": "Highly connected data, relationship-heavy queries, graph traversal use cases",
        "not_ideal_for": "Simple tabular data, high-throughput key-value lookups, small datasets without relationship complexity",
        "alternatives": ["DynamoDB (adjacency list pattern)", "Self-hosted Neo4j on EC2"]
    },
    "memorydb": {
        "name": "Amazon MemoryDB",
        "category": "Database",
        "description": "Redis-compatible, durable in-memory database for microservices needing both speed and durability",
        "use_cases": [
            "Primary database for microservices needing sub-millisecond latency",
            "Session stores requiring durability",
            "Real-time leaderboards and counters with persistence",
            "Message brokering with Redis pub/sub",
            "Caching layer that also needs to survive restarts"
        ],
        "key_features": [
            "Redis-compatible API with Multi-AZ durability via a distributed transactional log",
            "Data is always persisted, unlike ElastiCache's optional persistence",
            "Sub-millisecond read/write latency",
            "Automatic failover and recovery",
            "Snapshotting for backup/restore"
        ],
        "limits": {
            "max_shards_per_cluster": "500",
            "max_nodes_per_shard": "6 (1 primary + 5 replicas)",
            "max_item_size": "Similar to Redis, up to 1 GB for some types",
            "max_connections": "Varies by node type"
        },
        "pricing_model": "Per node hour by instance type",
        "free_tier": "None",
        "best_for": "Use as a primary database needing Redis speed with durability guarantees",
        "not_ideal_for": "Pure caching where durability doesn't matter (use ElastiCache, cheaper)",
        "alternatives": ["ElastiCache", "DynamoDB"]
    },
    "timestream": {
        "name": "Amazon Timestream",
        "category": "Database",
        "description": "Purpose-built, serverless time series database for IoT and operational data",
        "use_cases": [
            "IoT sensor data ingestion and analysis",
            "Application and infrastructure monitoring metrics",
            "Real-time analytics on time-stamped data",
            "DevOps monitoring dashboards",
            "Industrial equipment telemetry"
        ],
        "key_features": [
            "Automatically scales to ingest millions of events per second",
            "Built-in time series analytics functions (smoothing, interpolation)",
            "Tiered storage: recent data in memory, historical in cost-optimized storage",
            "Serverless -- no infrastructure to manage",
            "SQL-compatible query interface"
        ],
        "limits": {
            "max_record_size": "~2 KB per record",
            "retention": "Configurable per memory/magnetic store tier",
            "max_databases_per_account": "Varies, soft limit",
            "query_timeout": "60 seconds default"
        },
        "pricing_model": "Per GB ingested + per GB stored (tiered by memory/magnetic) + per GB scanned in queries",
        "free_tier": "None",
        "best_for": "Time-stamped IoT/metrics data at scale, automatic hot/cold data tiering",
        "not_ideal_for": "General-purpose relational or document data, non-time-series workloads",
        "alternatives": ["DynamoDB", "InfluxDB (self-managed)", "CloudWatch Metrics"]
    },
    "efs": {
        "name": "Amazon EFS",
        "category": "Storage",
        "description": "Fully managed, elastic NFS file system for use with EC2 and containers",
        "use_cases": [
            "Shared file storage across multiple EC2 instances",
            "Content management systems and web serving",
            "Big data and analytics workloads needing shared access",
            "Container storage for ECS/EKS pods",
            "Home directories and dev environments"
        ],
        "key_features": [
            "POSIX-compliant file system accessible over NFS",
            "Automatically scales storage up and down as files are added/removed",
            "Multiple storage classes (Standard, Infrequent Access, Archive)",
            "Regional (Multi-AZ) or One Zone availability options",
            "Lifecycle management to move files to cheaper tiers automatically"
        ],
        "limits": {
            "max_file_size": "47.9 TB",
            "max_filesystem_size": "No limit (petabyte scale)",
            "throughput_modes": "Bursting, Provisioned, Elastic",
            "max_mount_targets": "1 per AZ per file system"
        },
        "pricing_model": "Per GB stored per month (varies by storage class) + optional provisioned throughput",
        "free_tier": "5 GB Standard storage (12 months)",
        "best_for": "Shared POSIX file access across multiple compute instances, container-shared storage",
        "not_ideal_for": "Single-instance block storage (use EBS), object storage patterns (use S3), low-latency small reads at massive scale",
        "alternatives": ["EBS", "FSx", "S3"]
    },
    "fsx": {
        "name": "Amazon FSx",
        "category": "Storage",
        "description": "Fully managed file storage built on popular file systems (Windows File Server, Lustre, NetApp ONTAP, OpenZFS)",
        "use_cases": [
            "Windows-based application file shares",
            "High-performance computing and ML training (Lustre)",
            "Lift-and-shift of on-premises NetApp workloads",
            "Media processing pipelines needing high throughput",
            "Enterprise file shares needing Active Directory integration"
        ],
        "key_features": [
            "Choice of four file system engines depending on the workload",
            "FSx for Lustre integrates directly with S3 for HPC data processing",
            "FSx for Windows File Server supports SMB and Active Directory",
            "Automatic backups and Multi-AZ deployment options",
            "Scales to hundreds of GB/s throughput (Lustre)"
        ],
        "limits": {
            "max_storage": "Varies by engine, up to petabytes",
            "max_throughput": "Up to hundreds of GB/s (Lustre)",
            "supported_protocols": "SMB, NFS depending on engine",
            "backup_retention": "Configurable, up to 90 days"
        },
        "pricing_model": "Per GB-month provisioned storage + throughput capacity, varies by file system engine",
        "free_tier": "None",
        "best_for": "Workloads needing a specific file system (Windows shares, HPC/Lustre, ONTAP migrations)",
        "not_ideal_for": "Simple object storage needs (use S3), generic Linux shared storage (EFS is simpler)",
        "alternatives": ["EFS", "S3", "EBS"]
    },
    "glacier": {
        "name": "Amazon S3 Glacier",
        "category": "Storage",
        "description": "Low-cost archival storage classes within S3 for long-term data retention",
        "use_cases": [
            "Regulatory/compliance data archives",
            "Media asset long-term backup",
            "Disaster recovery cold storage",
            "Scientific/research data retention",
            "Infrequently accessed logs and historical records"
        ],
        "key_features": [
            "Multiple tiers: Instant Retrieval, Flexible Retrieval, Deep Archive",
            "Retrieval times from milliseconds to 12+ hours depending on tier",
            "S3 Lifecycle policies to automatically transition objects",
            "Vault Lock for WORM compliance requirements",
            "99.999999999% (11 nines) durability, same as S3 Standard"
        ],
        "limits": {
            "min_storage_duration": "90 to 180 days depending on tier (early deletion fee applies)",
            "retrieval_time_deep_archive": "12-48 hours",
            "max_object_size": "5 TB (same as S3)",
            "retrieval_time_flexible": "Minutes to 12 hours"
        },
        "pricing_model": "Per GB stored per month (cheapest S3 tiers) + per-request and retrieval fees",
        "free_tier": "None specific to Glacier (S3 free tier applies to Standard only)",
        "best_for": "Rarely-accessed data with long retention requirements, compliance archives",
        "not_ideal_for": "Frequently accessed data, data needing millisecond retrieval at low cost, short retention periods",
        "alternatives": ["S3 Standard-IA", "S3 Intelligent-Tiering"]
    },
    "mq": {
        "name": "Amazon MQ",
        "category": "Application Integration",
        "description": "Managed message broker service for Apache ActiveMQ and RabbitMQ",
        "use_cases": [
            "Migrating existing applications built on JMS/AMQP/MQTT/STOMP protocols",
            "Enterprise integration needing standard messaging protocols",
            "Replacing self-managed ActiveMQ/RabbitMQ brokers",
            "Hybrid architectures bridging on-prem and cloud messaging",
            "Applications requiring message ordering and protocol compliance"
        ],
        "key_features": [
            "Supports industry-standard APIs and protocols (JMS, AMQP 0-9-1, MQTT, STOMP, WebSocket)",
            "Active/standby or cluster deployment for high availability",
            "Automatic failover for Multi-AZ brokers",
            "Compatible with existing ActiveMQ/RabbitMQ client libraries with no code changes",
            "CloudWatch integration for broker metrics"
        ],
        "limits": {
            "max_message_size": "Varies by engine, typically up to a few MB",
            "max_brokers_per_account": "Soft limit, can request increase",
            "storage": "Up to hundreds of GB per broker",
            "supported_engines": "ActiveMQ, RabbitMQ"
        },
        "pricing_model": "Per broker instance hour + storage",
        "free_tier": "750 hours/month of a single-instance mq.t3.micro broker (12 months)",
        "best_for": "Migrating existing protocol-dependent messaging apps without rewriting code",
        "not_ideal_for": "New cloud-native apps (SQS/SNS are simpler and cheaper), extreme throughput needs (use Kinesis/MSK)",
        "alternatives": ["SQS", "SNS", "MSK"]
    },
    "eventbridge": {
        "name": "Amazon EventBridge",
        "category": "Application Integration",
        "description": "Serverless event bus for building event-driven applications at scale",
        "use_cases": [
            "Decoupling microservices via event-driven architecture",
            "Routing events from 200+ AWS services and SaaS partners",
            "Scheduled/cron-based automation",
            "Building an audit trail of application state changes",
            "Cross-account and cross-region event routing"
        ],
        "key_features": [
            "Rule-based routing with content filtering on event payloads",
            "Schema Registry to discover and manage event structures",
            "Built-in integrations with SaaS partners (Datadog, Zendesk, etc.)",
            "Archive and replay of past events",
            "EventBridge Pipes for point-to-point integrations with filtering/transformation"
        ],
        "limits": {
            "max_event_size": "256 KB",
            "max_rules_per_bus": "300 (soft limit)",
            "invocations_per_second": "Varies by target, soft limits apply",
            "max_targets_per_rule": "5"
        },
        "pricing_model": "Per million events published (custom/partner buses); AWS service events are free",
        "free_tier": "Events from AWS services to the default bus are always free",
        "best_for": "Event-driven architectures, routing/filtering events from many AWS and SaaS sources",
        "not_ideal_for": "Simple point-to-point queuing (use SQS), guaranteed strict ordering at very high throughput (use Kinesis)",
        "alternatives": ["SNS", "SQS", "Kinesis"]
    },
    "route53": {
        "name": "Amazon Route 53",
        "category": "Networking",
        "description": "Highly available and scalable DNS web service, also offering domain registration and health checking",
        "use_cases": [
            "DNS hosting for websites and applications",
            "Domain name registration and management",
            "Traffic routing policies (latency, geo, weighted, failover)",
            "Health checking and automatic failover between endpoints",
            "Private DNS for VPC-internal resource resolution"
        ],
        "key_features": [
            "100% availability SLA for DNS",
            "Multiple routing policies: simple, weighted, latency, failover, geolocation, multi-value",
            "Health checks with automatic DNS failover",
            "Private hosted zones for internal VPC name resolution",
            "Integrates natively with ELB, CloudFront, S3 for alias records"
        ],
        "limits": {
            "max_records_per_hosted_zone": "10,000 (soft limit)",
            "max_health_checks": "200 per account (soft limit)",
            "min_ttl": "0 seconds",
            "max_hosted_zones": "500 per account (soft limit)"
        },
        "pricing_model": "Per hosted zone per month + per million queries + domain registration fees",
        "free_tier": "None (no permanently free tier for hosted zones)",
        "best_for": "DNS management, domain registration, sophisticated traffic routing and failover",
        "not_ideal_for": "N/A -- DNS is typically a required component alongside other services, not an alternative choice",
        "alternatives": ["Cloudflare DNS", "Google Cloud DNS", "Third-party registrars"]
    },
    "globalaccelerator": {
        "name": "AWS Global Accelerator",
        "category": "Networking",
        "description": "Improves availability and performance of applications by routing traffic through AWS's global network via static anycast IPs",
        "use_cases": [
            "Improving latency for globally distributed users",
            "Fast regional failover for disaster recovery",
            "Gaming and voice/video applications needing low, consistent latency",
            "Applications requiring fixed IP addresses for allowlisting",
            "Multi-region active-active architectures"
        ],
        "key_features": [
            "Two static anycast IP addresses that don't change",
            "Routes traffic over AWS's private global network backbone instead of the public internet",
            "Automatic failover to healthy endpoints in seconds",
            "Traffic dials to control percentage of traffic per region",
            "Works with ALB, NLB, EC2, and Elastic IPs as endpoints"
        ],
        "limits": {
            "max_endpoint_groups": "10 per accelerator (soft limit)",
            "max_listeners": "10 per accelerator",
            "failover_time": "Typically under 30 seconds",
            "max_accelerators_per_account": "Soft limit, can request increase"
        },
        "pricing_model": "Fixed hourly fee per accelerator + per GB data transfer premium",
        "free_tier": "None",
        "best_for": "Global latency-sensitive apps, fast multi-region failover, fixed IP requirements",
        "not_ideal_for": "Single-region applications (CloudFront or ALB alone is cheaper), static content delivery (use CloudFront instead)",
        "alternatives": ["CloudFront", "Route 53 latency routing"]
    },
    "msk": {
        "name": "Amazon MSK",
        "category": "Analytics",
        "description": "Fully managed Apache Kafka service for building real-time streaming data pipelines",
        "use_cases": [
            "Event sourcing and CQRS architectures",
            "Log aggregation at very high throughput",
            "Real-time stream processing with Kafka Streams/Flink",
            "Migrating existing self-managed Kafka clusters to AWS",
            "Change data capture (CDC) pipelines"
        ],
        "key_features": [
            "Fully compatible with open-source Apache Kafka APIs and tooling",
            "MSK Serverless for automatic capacity management",
            "Multi-AZ replication for durability",
            "Integrates with IAM for authentication and encryption in transit/at rest",
            "MSK Connect for managed Kafka Connect connectors"
        ],
        "limits": {
            "max_message_size": "Configurable, default 1 MB",
            "max_partitions_per_cluster": "Varies by broker size and count",
            "retention": "Configurable, limited by storage",
            "supported_kafka_versions": "Multiple recent versions supported"
        },
        "pricing_model": "Provisioned: per broker-hour + storage. Serverless: per cluster-hour + throughput + storage.",
        "free_tier": "None",
        "best_for": "Teams standardized on Kafka, very high-throughput event streaming, existing Kafka migrations",
        "not_ideal_for": "Simple pub/sub needs (SNS/SQS simpler and cheaper), teams without Kafka operational experience",
        "alternatives": ["Kinesis", "SQS", "SNS"]
    },
    "appsync": {
        "name": "AWS AppSync",
        "category": "Networking",
        "description": "Managed service for building GraphQL and Pub/Sub APIs that connect to multiple data sources",
        "use_cases": [
            "Mobile and web app backends needing flexible data fetching",
            "Real-time apps with live data subscriptions (chat, collaboration tools)",
            "Aggregating multiple data sources (DynamoDB, RDS, Lambda, HTTP) behind one GraphQL API",
            "Offline-first mobile apps with data sync",
            "Reducing over-fetching/under-fetching compared to REST"
        ],
        "key_features": [
            "Managed GraphQL API with built-in resolvers to AWS data sources",
            "Real-time subscriptions over WebSockets",
            "Offline data synchronization for mobile clients",
            "Fine-grained authorization via Cognito, IAM, API keys, or OIDC",
            "Built-in caching to reduce backend load"
        ],
        "limits": {
            "max_query_depth": "Configurable, default reasonable limits apply",
            "max_payload_size": "Varies, typically a few MB",
            "request_timeout": "30 seconds",
            "max_resolvers": "Practically high, soft limits apply"
        },
        "pricing_model": "Per million query/data modification operations + per real-time subscription minute",
        "free_tier": "250,000 query/data operations and 250,000 real-time minutes (12 months)",
        "best_for": "GraphQL APIs, real-time subscriptions, aggregating multiple backend data sources",
        "not_ideal_for": "Simple single-resource REST APIs (API Gateway is simpler), teams unfamiliar with GraphQL",
        "alternatives": ["API Gateway"]
    },
    "lightsail": {
        "name": "Amazon Lightsail",
        "category": "Compute",
        "description": "Simplified virtual private server (VPS) offering with predictable pricing, aimed at simpler workloads",
        "use_cases": [
            "Simple websites and blogs",
            "Small business applications",
            "Development and testing environments",
            "Learning cloud computing without complex AWS concepts",
            "Simple e-commerce sites"
        ],
        "key_features": [
            "Predictable, bundled monthly pricing (compute + storage + transfer included)",
            "One-click app and OS blueprints (WordPress, LAMP, Node.js, etc.)",
            "Simplified console compared to full EC2/VPC complexity",
            "Built-in load balancing, CDN, and managed databases available",
            "Easy upgrade path to full EC2 if needed"
        ],
        "limits": {
            "instance_sizes": "512 MB to 32 GB RAM plans",
            "data_transfer": "Included allowance per plan, overage billed separately",
            "max_instances": "20 per region (soft limit)",
            "storage": "SSD-based, bundled per plan"
        },
        "pricing_model": "Flat monthly rate per bundle (compute + storage + data transfer included)",
        "free_tier": "First 3 months free on select bundles (promotional, not guaranteed ongoing)",
        "best_for": "Simple workloads wanting predictable pricing without learning full AWS networking/IAM complexity",
        "not_ideal_for": "Complex, scalable production architectures, workloads needing fine-grained AWS service integration",
        "alternatives": ["EC2", "App Runner", "Elastic Beanstalk"]
    },
    "batch": {
        "name": "AWS Batch",
        "category": "Compute",
        "description": "Fully managed batch computing service that dynamically provisions compute resources for batch jobs",
        "use_cases": [
            "Large-scale scientific simulations",
            "Financial risk modeling and overnight batch runs",
            "Media transcoding at scale",
            "Genomics and bioinformatics pipelines",
            "ETL jobs that run periodically at large scale"
        ],
        "key_features": [
            "Automatically provisions the optimal compute type and quantity based on job requirements",
            "Supports EC2, Spot, and Fargate as underlying compute",
            "Job queues and priority-based scheduling",
            "Integrates with Step Functions for complex workflow orchestration",
            "Docker container-based job definitions"
        ],
        "limits": {
            "max_vcpus_per_job": "Varies by compute environment configuration",
            "job_timeout": "Configurable, no hard cap by default",
            "max_job_queues": "Soft limit, can request increase",
            "compute_environment_types": "EC2 On-Demand, EC2 Spot, Fargate, Fargate Spot"
        },
        "pricing_model": "No additional Batch charge -- pay only for underlying EC2/Fargate/Spot compute consumed",
        "free_tier": "No Batch-specific charge (pay only for compute resources used)",
        "best_for": "Large-scale parallel batch jobs, cost-optimized with Spot, scientific/HPC workloads",
        "not_ideal_for": "Real-time/interactive workloads, simple scheduled tasks (use EventBridge Scheduler + Lambda instead)",
        "alternatives": ["ECS", "Lambda (for smaller jobs)", "EC2 with custom scripts"]
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
                      "EC2", "RDS", "Aurora", "SQS", "SNS", "API Gateway",
                      "ElastiCache", "CloudFront", "ECS", "EKS", "Cognito",
                      "Kinesis", "Bedrock", "Redshift", "DocumentDB", "Neptune",
                      "MemoryDB", "Timestream", "EFS", "FSx", "Glacier", "MQ",
                      "EventBridge", "Route 53", "Global Accelerator", "MSK",
                      "AppSync", "Lightsail", "Batch" -- an unrecognized name
                      returns the full current list in "available_services")

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