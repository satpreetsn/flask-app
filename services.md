# API Documentation

## Overview

This Flask application exposes REST API endpoints for managing users stored in a PostgreSQL database.

The application demonstrates:

* Flask REST APIs
* PostgreSQL Integration
* SQLAlchemy ORM
* Kubernetes Health Checks
* JSON-based API Responses

---

# Base URL

## Local Development

```text id="yomfgx"
http://localhost:5000
```

## Amazon EKS

```text id="f5edng"
http://<ALB-DNS-NAME>
```

Example:

```text id="s1f4pb"
http://k8s-flask-demo-123456.us-east-1.elb.amazonaws.com
```

---

# Health Check Endpoints

These endpoints are used by Kubernetes probes and monitoring tools.

---

## Health Check

### Endpoint

```http id="x7rz9q"
GET /health/live
```

### Purpose

Verifies that the Flask application is running.

### Response

```json id="i63wjq"
{
  "status": "UP"
}
```

### HTTP Status

```text id="fj76v8"
200 OK
```

---

## Readiness Check

### Endpoint

```http id="psghoz"
GET /health/ready
```

### Purpose

Verifies:

* Flask application is operational
* PostgreSQL database is reachable
* Application is ready to receive traffic

### Response

```json id="n2vtcn"
{
  "status": "READY"
}
```

### HTTP Status

```text id="7j6sp9"
200 OK
```

If the database is unavailable:

```json id="mz6dwg"
{
  "status": "NOT_READY"
}
```

```text id="nngc6y"
503 Service Unavailable
```

---

# User Management APIs

---

## Get All Users

### Endpoint

```http id="ujkbhh"
GET /users
```

### Purpose

Returns all users stored in PostgreSQL.

### Example Request

```bash id="34hlzg"
curl http://localhost:5000/users
```

### Example Response

```json id="88ezt4"
[
  {
    "uid": "john",
    "name": "John Doe",
    "email": "john@example.com"
  },
  {
    "uid": "jane",
    "name": "Jane Doe",
    "email": "jane@example.com"
  }
]
```

### HTTP Status

```text id="vc8v9w"
200 OK
```

---

## Get User By ID

### Endpoint

```http id="0vjlwm"
GET /users/<uid>
```

### Example Request

```bash id="pnzfru"
curl http://localhost:5000/users/john
```

### Example Response

```json id="11ah1s"
{
  "uid": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

### HTTP Status

```text id="6g1p2c"
200 OK
```

### Not Found

```json id="uwuv7o"
{
  "message": "User not found"
}
```

```text id="4v5lw7"
404 Not Found
```

---

## Create User

### Endpoint

```http id="s2rcrd"
POST /users
```

### Purpose

Creates a new user in PostgreSQL.

### Request Body

```json id="zhc8gw"
{
  "uid" : "john",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### Example Request

```bash id="4m2b3v"
curl -X POST \
-H "Content-Type: application/json" \
-d '{"uid":"john","name":"John Doe","email":"john@example.com"}' \
http://localhost:5000/users
```

### Response

```json id="6s7v74"
{
  "uid" : "john",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### HTTP Status

```text id="dfyc4k"
201 Created
```

---

## Update User

### Endpoint

```http id="r4mpxj"
PUT /users/<uid>
```

### Request Body

```json id="ucq1oz"
{
  "uid": "<uid>",
  "name": "Updated User",
  "email": "updated@example.com"
}
```

### Example Request

```bash id="qwr8tt"
curl -X PUT \
-H "Content-Type: application/json" \
-d '{"name":"Updated User"}' \
http://localhost:5000/users/john
```

### Response

```json id="o0gm0r"
{
  "uid": "<uid>",
  "name": "Updated User",
  "email": "updated@example.com"
}
```

### HTTP Status

```text id="ee4hvt"
200 OK
```

---

## Delete User

### Endpoint

```http id="rv4phw"
DELETE /users/<id>
```

### Example Request

```bash id="ewq6p5"
curl -X DELETE \
http://localhost:5000/users/john
```

### Response

```json id="j9q3lo"
{
  "uid" : "john",
  "name": "John Doe",
  "email": "john@example.com"
}
```

### HTTP Status

```text id="1epv0y"
200 OK
```

---

# Database Connectivity

The application connects to PostgreSQL using SQLAlchemy.

Example configuration:

```text id="1rfd0g"
postgresql://postgres:<password>@postgres.pgsql.svc.cluster.local:5432/appdb
```

Connection pooling is enabled to improve performance and reduce database connection overhead.

---

# Kubernetes Integration

## Liveness Probe

Uses:

```http id="qvyr4k"
GET /health/live
```

Purpose:

* Detect application failures
* Automatically restart unhealthy containers

---

## Readiness Probe

Uses:

```http id="w54h6t"
GET /health/ready
```

Purpose:

* Verify database connectivity
* Prevent traffic to unhealthy pods

---

# Response Codes

| Status Code | Meaning               |
| ----------- | --------------------- |
| 200         | Successful Request    |
| 201         | Resource Created      |
| 400         | Invalid Request       |
| 404         | Resource Not Found    |
| 500         | Internal Server Error |
| 503         | Service Not Ready     |

---


---

# Future Enhancements

Potential improvements:

* Swagger/OpenAPI Documentation
* Authentication and Authorization
* JWT Support
* Pagination
* Search and Filtering
* Rate Limiting
* Audit Logging
* Prometheus Metrics Endpoint

```
```
