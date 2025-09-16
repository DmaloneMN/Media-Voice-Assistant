# Media Voice Assistant

[![Azure DevOps CI](https://img.shields.io/azure-devops/build/media-voice-assistant/main?color=0078D4)](https://dev.azure.com/your-org/media-voice-assistant/_build/latest?definitionId=1) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered voice assistant for movie and TV show recommendations, enhanced with Retrieval-Augmented Generation (RAG) for factual, personalized responses. Built on Azure infrastructure with CI/CD support.

## Overview

This repository implements a voice-controlled assistant that provides personalized movie and TV recommendations. It uses RAG to ground responses in external data sources (e.g., TMDb API for media details, SQL for user preferences), reducing hallucinations and improving accuracy. Key enhancements include:
- **RAG Pipeline**: Retrieves relevant chunks from movie/TV knowledge bases (KBs) for grounded recommendations.
- **Chunking**: Splits media data (e.g., synopses, reviews) into semantic units for efficient retrieval.
- **Query Routing**: Classifies voice queries (e.g., "sci-fi movie" → movie KB) using semantic or LLM-based routing.
- **LangChain Agents**: Orchestrates routing, retrieval, and generation with multi-turn support.
- **Hallucination Mitigation**: LLM-as-a-Judge checks ensure factual responses (e.g., no invented plots).
- **Monitoring**: Tracks latency, faithfulness, and routing accuracy with Azure Application Insights.
- **Azure Integration**: Leverages Azure OpenAI for embeddings/LLM, Speech SDK for voice-to-text, and Cosmos DB for vector storage.

The system processes voice inputs, routes queries to the appropriate KB, retrieves context, generates responses, and monitors performance—all deployed via Terraform and Kubernetes.

## Features
- **Voice-Controlled Interface**: Real-time speech-to-text using Azure Speech SDK for natural interactions.
- **Personalized Recommendations**: Integrates user preferences from SQL (e.g., favorite genres) for tailored suggestions.
- **RAG-Enhanced Search**: Semantic retrieval from multi-KB vector stores (movies, TV, users) for accurate, factual recs.
- **Query Routing**: Semantic/LLM-based classification to direct queries to the right KB (e.g., movie vs. TV).
- **Hallucination Checks**: Post-generation verification to flag inaccurate responses.
- **Azure-Based Infrastructure**: Scalable deployment with Azure OpenAI, Cosmos DB (vector store), and Application Insights (monitoring).
- **CI/CD Pipeline**: Automated validation, builds, container pushes, and Kubernetes updates.
- **Data Pipeline**: Bronze/silver/gold layers for ingesting TMDb data, chunking, embedding, and curation.

## Prerequisites
- Azure subscription with permissions for OpenAI, Speech Services, Cosmos DB, and Kubernetes (AKS).
- Terraform CLI (v1.0+), kubectl, and Docker installed.
- Python 3.10+ with pip.
- TMDb API key (free at [themoviedb.org](https://www.themoviedb.org/documentation/api)).
- GitHub Actions or Azure DevOps for CI/CD (optional but recommended).

## Setup

1. **Clone the Repository**:
