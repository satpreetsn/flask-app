flask-app
├── Dockerfile
├── app.py
├── config.py
├── config_loader.py
├── database
│   ├── __init__.py
│   └── db.py
├── db-config.json
├── kubernetes_manifests
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
│   ├── Readme.md
│   ├── __init__.py
│   ├── health_check.py
│   └── user_route.py
├── services
│   ├── __init__.py
│   └── user_service.py
└── tree.md


