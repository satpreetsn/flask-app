# FinOps Strategy

## Overview

This project was designed with FinOps principles in mind to ensure efficient cloud resource utilization while maintaining reliability and scalability.

The following cost optimization strategies can be applied to the EKS-based Flask and PostgreSQL deployment.

---

# Cost Visibility

## Resource Tagging

Apply consistent tags to all AWS resources.

Example:

| Key         | Value         |
| ----------- | ------------- |
| Project     | flask-demo    |
| Environment | dev           |
| Owner       | platform-team |
| CostCenter  | engineering   |

Benefits:

* Cost allocation reporting
* Resource ownership identification
* Budget tracking
* Chargeback and showback

---

## AWS Cost Explorer

Monitor spending by:

* Service
* Region
* Resource Tags
* Daily Spend

Recommended dashboards:

* Amazon EKS
* EC2
* EBS
* Application Load Balancer
* CloudWatch

---

## AWS Budgets

Create monthly budget alerts.

Example:

| Threshold | Action      |
| --------- | ----------- |
| 50%       | Email Alert |
| 80%       | Email Alert |
| 100%      | Email Alert |

This prevents unexpected costs.

---

# Compute Optimization

## Right-Size Worker Nodes

Current Deployment:

```text
2 x t3.medium
```

Evaluate:

```text
t3.small
t3.medium
t4g.medium
```

based on utilization metrics.

Monitor:

* CPU Usage
* Memory Usage
* Pod Density

---

## Cluster Autoscaler

Enable automatic scaling of worker nodes.

Benefits:

* Scale out during traffic spikes
* Scale in during low utilization
* Reduce idle compute costs

---

## Horizontal Pod Autoscaler (HPA)

Scale Flask pods automatically.

Example:

```yaml
minReplicas: 2
maxReplicas: 10
targetCPUUtilizationPercentage: 70
```

Benefits:

* Better resource utilization
* Reduced over-provisioning

---

## Use ARM-Based Instances

Consider Graviton instances:

```text
t4g.small
t4g.medium
```

Benefits:

* Lower cost
* Improved price/performance ratio

---

# Storage Optimization

## Use gp3 Instead of gp2

Recommended:

```text
gp3
```

Benefits:

* Lower cost
* Better baseline performance
* Independent IOPS scaling

---

## Monitor Unused Volumes

Review EBS volumes regularly.

Delete:

* Detached volumes
* Orphaned PVC volumes
* Unused snapshots

---

## Database Storage Monitoring

Track:

* Storage utilization
* Growth trends
* Snapshot usage

Resize volumes only when required.

---

# Networking Optimization

## Avoid NAT Gateway for Development

NAT Gateways are often one of the highest networking costs.

Options:

### Development Environment

```text
Public Worker Nodes
```

or

```text
Private Worker Nodes
+ VPC Endpoints
```

instead of NAT Gateway.

Benefits:

* Reduced networking costs

---

## Use VPC Endpoints

Create endpoints for:

* S3
* STS
* ECR API
* ECR DKR
* CloudWatch Logs

Benefits:

* Reduced NAT traffic
* Improved security

---

# Kubernetes Optimization

## Define Resource Requests and Limits

Example:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

Benefits:

* Improved scheduling
* Reduced resource waste

---

## Monitor Underutilized Pods

Use:

```bash
kubectl top pods
kubectl top nodes
```

Identify:

* Over-provisioned workloads
* Idle applications

---

## Namespace Resource Quotas

Prevent excessive consumption.

Example:

```yaml
apiVersion: v1
kind: ResourceQuota
```

Benefits:

* Controlled resource allocation
* Reduced accidental overspending

---

# Application Optimization

## Database Connection Pooling

Implement SQLAlchemy connection pooling.

Example:

```python
pool_size=10
max_overflow=20
pool_timeout=30
```

Benefits:

* Improved database efficiency
* Reduced connection overhead

---

## Health Checks

Implement:

* Liveness Probes
* Readiness Probes

Benefits:

* Faster recovery
* Reduced operational overhead

---

# Monitoring and Observability

## CloudWatch Monitoring

Track:

* CPU Utilization
* Memory Utilization
* Disk Usage
* Network Traffic

Benefits:

* Early detection of inefficiencies

---

## Log Retention Policies

Avoid indefinite log storage.

Example:

```text
Development: 7 Days
Testing: 14 Days
Production: 30 Days
```

Benefits:

* Reduced CloudWatch costs

---

# Environment Management

## Automatic Shutdown of Non-Production Environments

For development environments:

```text
Start: 08:00
Stop: 20:00
```

Benefits:

* Significant compute savings

Possible implementation:

* EventBridge Scheduler
* Lambda Automation
* Terraform Automation

---

## Delete Resources After Demonstration

Resources to remove:

* EKS Cluster
* Node Groups
* Load Balancers
* EBS Volumes
* IAM Roles
* OIDC Providers

Benefits:

* Prevents unnecessary charges

---

# Future FinOps Enhancements

The following improvements can further optimize cloud costs:

* Karpenter
* Spot Instances
* AWS Compute Optimizer
* Kubecost
* AWS Trusted Advisor
* Savings Plans
* Graviton Adoption
* Cluster Autoscaler
* Vertical Pod Autoscaler
* Reserved Capacity Planning

---

# Summary

The primary cost drivers in this architecture are:

1. Amazon EKS Control Plane
2. EC2 Worker Nodes
3. Application Load Balancer
4. NAT Gateway (if used)
5. Amazon EBS Volumes

Key FinOps recommendations:

* Use Graviton-based instances where possible
* Implement HPA and Cluster Autoscaler
* Define Kubernetes resource limits
* Use gp3 storage
* Avoid unnecessary NAT Gateways
* Monitor costs with AWS Budgets and Cost Explorer
* Remove unused resources promptly
* Automate non-production environment shutdown

These practices help maintain a balance between performance, reliability, and cost efficiency while operating workloads on Amazon EKS.
