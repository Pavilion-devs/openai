# Irawo AI Project - AI Documentation

## Overview

Welcome to the AI documentation for the Irawo project. This document provides an overview of the artificial intelligence components, models, and services used in the project.

## Table of Contents

1. [Introduction](#introduction)
2. [AI Services](#ai-services)
    1. [Azure OpenAI Service](#azure-openai-service)
    2. [Langchain](#langchain)

3. [Integration with Frontend and Backend](#integration-with-frontend-and-backend)
4. [Deployment](#deployment)
5. [Monitoring and Evaluation](#monitoring-and-evaluation)
6. [References](#references)

## Introduction

The Irawo project aims to revolutionize social skills development through AI-driven realistic conversations. Leveraging Azure OpenAI Service and Langchain, our platform provides users with a virtual social coach for interactive learning.

## AI Services

### Azure OpenAI Service

Azure OpenAI Service serves as the backbone of our conversation generation. We utilize its chat-based language models to provide users with dynamic and context-aware responses. The service is integrated into our backend for seamless communication.

### Langchain

Langchain plays a crucial role in enhancing the interactive capabilities of our virtual social coach. It contributes to the conversation flow, ensuring realistic dialogues and dynamic user interactions.


## Integration with Frontend and Backend

The AI components seamlessly integrate into both frontend and backend systems. The frontend communicates user inputs to the backend, which, in turn, interacts with Azure OpenAI Service and Langchain to generate appropriate responses.

## Deployment

AI components are deployed using Azure services, ensuring scalability and reliability. Continuous integration and deployment pipelines guarantee efficient updates and improvements.

## Monitoring and Evaluation

We implement monitoring systems to track model performance and user interactions. Regular evaluations help refine models and enhance the overall user experience.

**Getting Started:**

1. **Prerequisites:**
   * Python 3.7 or higher
   * An OpenAI API key ([https://platform.openai.com/account/api-keys](
https://platform.openai.com/account/api-keys))
   * A LUIS subscription ([https://azure.microsoft.com/en-us/products/cognitive-services/language-understanding](https://azure.microsoft.com/en-us/products/cognitive-services/language-understanding))

2. **Setup:**
   * Install the required packages:
      ```bash
      pip install -r requirements.txt
      ```
   * Create a `.env` file in the root directory with the following environment variables:
      ```
      OPENAI_API_KEY=[YOUR_OPEN
AI_API_KEY]
      MODEL_NAME=[YOUR_OPENAI_MODEL_NAME]
      luis_endpoint=[YOUR_LUIS_ENDPOINT]
      luis_key=[YOUR_LUIS_API_KEY]
      deployment_name_luis=[YOUR_LUIS_DEPLOYMENT_
NAME]
      POSITIVE_THRESHOLD=0.05
      NEGATIVE_THRESHOLD=-0.05
      speechkey=[YOUR_SPEECH_API_KEY]
      speechregion=[YOUR_SPEECH_REGION]
      ```
## References

- [Azure OpenAI Documentation](https://docs.microsoft.com/en-us/azure/openai/)
- [Langchain GitHub Repository](https://github.com/langchain)
