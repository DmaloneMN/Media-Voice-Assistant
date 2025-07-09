# Media Voice Assistant

AI-powered voice assistant for movie and TV show recommendations.

## Features
- Voice-controlled interface
- Personalized recommendations
- Azure-based infrastructure
- CI/CD pipeline

## Setup

1. Clone the repository
2. Set up environment variables (see .env.example)
3. Run `terraform init` in infrastructure directory
4. Deploy with `terraform apply`

## Deployment

The CI/CD pipeline will automatically:
- Validate infrastructure changes
- Deploy to Azure
- Build and push container images
- Update Kubernetes deployments
