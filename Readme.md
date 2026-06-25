# Flask + PostgreSQL on Amazon EKS

## Overview

This project demonstrates a cloud-native Flask application deployed on Amazon EKS (Elastic Kubernetes Service) with PostgreSQL as the backend database.

The solution showcases:

* Python Flask web application
* PostgreSQL database
* SQLAlchemy ORM
* Docker containerization
* Kubernetes Deployments and StatefulSets
* Persistent storage using Amazon EBS
* Configuration management using ConfigMaps
* Secret management using Kubernetes Secrets
* Application health checks
* AWS Application Load Balancer (ALB) Ingress
* Amazon EKS deployment

---

## Architecture

```text
                    Internet
                        |
                        v
                AWS Application
                 Load Balancer
                        |
                        v
                Flask Service
                        |
                        v
              Flask Deployment
                 (1 Replicas)
                        |
                        v
              PostgreSQL Service
                        |
                        v
           PostgreSQL StatefulSet
                        |
                        v
                 Amazon EBS Volume
```

---

## Prerequisites

### AWS

* AWS Account
* AWS CLI configured
* kubectl installed
* eksctl installed
* Docker installed
* Helm installed

Verify installation:

```bash
aws --version
kubectl version --client
eksctl version
docker version
helm version
```

---

## Project Structure

```text
.
├── Dockerfile
├── app.py
├── config.py
├── config_loader.py
├── database
│   ├── __init__.py
│   └── db.py
├── db-config.json
├── k8s
│   ├── flask-app
│   │   ├── configmap.yaml
│   │   ├── deployment.yaml
│   │   ├── ingress.yaml
│   │   ├── namespace.yaml
│   │   ├── secrets.yaml
│   │   └── service.yaml
│   └── postgres
│       ├── namespace.yaml
│       ├── pv.yaml
│       ├── pvc.yaml
│       ├── secrets.yaml
│       ├── service.yaml
│       └── statefulset.yaml
├── models
│   ├── __init__.py
│   └── user.py
├── requirements.txt
├── routes
│   ├── __init__.py
│   ├── health_check.py
│   └── user_route.py
├── services
│   ├── __init__.py
│   └── user_service.py
└── Readme.md
└── FinOps.md
```

---

## Build Docker Image

Build the application image.

```bash
docker build -t user-app:latest .
```

Run locally:

```bash
docker run --name user-app --network user-network --env-file .env.docker -p 5000:5000 -d user-app:latest
```

---

## Push Docker Image to Docker Hub Repository

```bash
docker login
```

Tag image:

```bash
docker tag user-app:latest <dockerhub-username>/user-app:latest
```

Push image:

```bash
docker push <dockerhub-username>/user-app:latest
```

---

# Create Amazon EKS Cluster

The EKS cluster and node group were created using the AWS Management Console.

## EKS Configuration

| Setting            | Value           |
| ------------------ | --------------- |
| Cluster Name       | cluster-1     |
| Kubernetes Version | 1.35            |
| Node Group         | managed-workers |
| Instance Type      | t3.small       |
| Desired Nodes      | 2               |
| Capacity Type      | On-Demand       |

---

## Networking

The cluster was deployed into an existing VPC containing:

```text
VPC
├── Public Subnet A
├── Public Subnet B
├── Private Subnet A
└── Private Subnet B
```

### Public Subnets

Used for:

* Application Load Balancer (ALB)

### Private Subnets

Used for:

* EKS Worker Nodes
* Kubernetes Workloads

---

## Configure kubectl Access

After cluster creation, update the local kubeconfig:

```bash
aws eks update-kubeconfig \
  --region <region> \
  --name <cluster-name>
```

Verify connectivity:

```bash
kubectl get nodes
```

Expected output:

```text
NAME                                           STATUS   ROLES    AGE
ip-10-0-1-10.ec2.internal                      Ready    <none>   10m
ip-10-0-2-10.ec2.internal                      Ready    <none>   10m
```

---

# Configure OIDC Provider

The IAM OIDC provider was associated with the EKS cluster using the AWS Management Console.

Steps:

1. Open Amazon EKS Console.
2. Select the cluster.
3. Navigate to the **Overview** tab.
4. Under **OpenID Connect provider URL**, choose **Associate IAM OIDC provider**.
5. Complete the association.

Verify:

```bash
aws eks describe-cluster \
  --name <cluster-name> \
  --query "cluster.identity.oidc.issuer"
```

---

# Install AWS Load Balancer Controller

The AWS Load Balancer Controller enables Kubernetes Ingress resources to automatically provision AWS Application Load Balancers.

## Create IAM Policy

Download the AWS Load Balancer Controller IAM policy:

```bash
curl -O https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/v3.4.0/docs/install/iam_policy.json
```

Create the policy:

```bash
aws iam create-policy \
  --policy-name AWSLoadBalancerControllerIAMPolicy \
  --policy-document file://iam_policy.json
```

---

## Create IAM Role

1. Open IAM Console.
2. Create a new IAM Role.
3. Select **Web Identity**.
4. Choose the EKS OIDC Provider.
5. Set Audience to:

```text
sts.amazonaws.com
```

6. Attach:

```text
AWSLoadBalancerControllerIAMPolicy
```

7. Create the role.

---

## Create Kubernetes Service Account

Update the service account manifest with the IAM role ARN:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: aws-load-balancer-controller
  namespace: kube-system
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<ACCOUNT_ID>:role/AWSLoadBalancerControllerRole
```

Apply:

```bash
kubectl apply -f aws-load-balancer-controller-service-account.yaml
```

---

## Install Controller using Helm

Add Helm repository:

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```

Install:

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=<cluster-name> \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=<region> \
  --set vpcId=<vpc-id>
```

Verify:

```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
```

Expected output:

```text
NAME                           READY
aws-load-balancer-controller   2/2
```

---

# Verify Cluster Components

```bash
kubectl get nodes
kubectl get pods -A
kubectl get svc -A
```

Ensure all worker nodes are in Ready state before deploying the application.

```

---

# Deploy PostgreSQL

## Create Namespace

```bash
kubectl apply -f k8s/postgres/namespace.yaml
```

## Create Secret

```bash
kubectl apply -f k8s/postgres/secret.yaml
```

## Deploy PostgreSQL

```bash
kubectl apply -f k8s/postgres/pv.yaml
kubectl apply -f k8s/postgres/pvc.yaml
kubectl apply -f k8s/postgres/service.yaml
kubectl apply -f k8s/postgres/statefulset.yaml
```

Verify:

```bash
kubectl get pods
kubectl get pvc
```

Expected:

```text
postgres-0   Running
```

---

# PostgreSQL Connectivity

PostgreSQL is exposed through a headless service.

DNS:

```text
postgres.postgres.svc.cluster.local
```

Example connection string:

```text
postgresql://postgres:<password>@postgres.pgsql.svc.cluster.local:5432/appdb
```

---

# Deploy Flask Application

## Create ConfigMap

```bash
kubectl apply -f k8s/flask-app/configmap.yaml
```

## Deploy Application

```bash
kubectl apply -f k8s/flask-app/deployment.yaml
kubectl apply -f k8s/flask-app/service.yaml
```

Verify:

```bash
kubectl get pods
kubectl get svc
```

---

# Deploy Ingress

```bash
kubectl apply -f k8s/flask-app/ingress.yaml
```

Check ingress:

```bash
kubectl get ingress
```

Retrieve ALB hostname:

```bash
kubectl get ingress
```

Example:

```text
user-app-lb-xxxxxxxxx.ap-south-1.elb.amazonaws.com
```

---

# Health Endpoints

## Application Health

```http
GET /health/live
```

Response:

```json
{
  "status": "UP"
}
```

HTTP Status:

```text
200 OK
```

## Readiness Check

```http
GET /health/ready
```

This endpoint validates database connectivity before marking the pod as ready.

Response:

```json
{
  "status": "READY"
}
```

---

# Verify Application

Port-forward service:

```bash
kubectl port-forward svc/user-app 5000:5000
```

Open:

```text
http://localhost:5000
```

Health:

```text
http://localhost:5000/health/live
http://localhost:5000/health/ready
```

---

# Useful Commands

View pods:

```bash
kubectl get pods -A
```

View logs:

```bash
kubectl logs deployment/flask-app
```

Describe pod:

```bash
kubectl describe pod <pod-name>
```

Connect to PostgreSQL pod:

```bash
kubectl exec -it postgres-0 -- bash
```

Connect using psql:

```bash
psql -U postgres -d appdb
```

---

# Cleanup

To avoid ongoing AWS charges, delete all resources after testing.

## Step 1: Delete Kubernetes Resources

Delete application resources:

```bash
kubectl delete -f k8s/
```

Verify:

```bash
kubectl get all -A
kubectl get pvc -A
kubectl get ingress -A
```

---

## Step 2: Delete Load Balancer Controller

```bash
helm uninstall aws-load-balancer-controller -n kube-system
```

Verify:

```bash
kubectl get deployment -n kube-system
```

---

## Step 3: Delete Remaining AWS Load Balancers

Open:

AWS Console → EC2 → Load Balancers

Delete any ALBs created by Kubernetes.

Example:

```text
k8s-flask-demo-xxxxxxxx
```

Wait until deletion completes.

---

## Step 4: Delete EBS Volumes

Open:

AWS Console → EC2 → Volumes

Delete any EBS volumes created for PostgreSQL PVCs.

Example:

```text
pvc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

Verify no unused volumes remain.

---

## Step 5: Delete EKS Node Group

Open:

AWS Console → EKS → Clusters → Compute

Select:

```text
managed-workers
```

Choose:

```text
Delete Node Group
```

Wait until status becomes deleted.

---

## Step 6: Delete EKS Cluster

Open:

AWS Console → EKS → Clusters

Select:

```text
flask-demo
```

Choose:

```text
Delete Cluster
```

Wait for deletion to complete.

---

## Step 7: Delete IAM Resources

Open:

AWS Console → IAM

Delete:

### IAM Role

```text
AWSLoadBalancerControllerRole
```

### IAM Policy

```text
AWSLoadBalancerControllerIAMPolicy
```

---

## Step 8: Delete OIDC Provider

Open:

AWS Console → IAM → Identity Providers

Delete:

```text
oidc.eks.<region>.amazonaws.com/id/XXXXXXXXXXXX
```

---

## Step 9: Delete Docker Images (Optional)

Docker Hub:

1. Open Docker Hub.
2. Navigate to Repositories.
3. Select:

```text
user-app
```

4. Delete the repository.

---

## Step 10: Verify No Billable Resources Remain

Check the following AWS services:

### EKS

```text
No Clusters
```

### EC2

```text
No Running Instances
```

### Load Balancers

```text
No Application Load Balancers
```

### EBS

```text
No Unused Volumes
```

### IAM

```text
No Load Balancer Controller Roles/Policies
```

### VPC (Optional)

If the VPC was created specifically for this project:

```text
Delete VPC
Delete Subnets
Delete Route Tables
Delete Internet Gateway
Delete NAT Gateway
```

---

# Estimated Cost Savings

Deleting the resources above prevents ongoing charges from:

* Amazon EKS Control Plane
* EC2 Worker Nodes
* Application Load Balancers
* EBS Volumes
* NAT Gateway
* Elastic IP Addresses
* CloudWatch Logs

```
```


---

# Features Demonstrated

* Kubernetes Deployments
* StatefulSets
* Persistent Volumes
* Amazon EBS Integration
* Kubernetes Secrets
* ConfigMaps
* Service Discovery
* Internal DNS Resolution
* Health Checks
* ALB Ingress
* Amazon ECR
* Amazon EKS
* PostgreSQL Database Integration
* Containerized Flask Application

```
```
