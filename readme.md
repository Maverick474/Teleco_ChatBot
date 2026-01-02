# Teleco ChatBot your AI powered virtual assistant chat bot

An intelligent conversational assistant for telecom customer support built with FastAPI, LangChain, and Streamlit. 
This chatbot leverages advanced language models and retrieval-augmented generation (RAG) to handle customer inquiries across multiple domains including policies, billing, 
packages, and troubleshooting.

## Overview
The Telecom Chatbot is a multi-agent system designed to provide intelligent customer support with the following capabilities:

- Language Detection: Automatically detects and rejects unsupported languages
- Security: Implements guardrails to block malicious or outside queries
- Intelligent Routing: Uses a Router Agent to direct queries to specialized agents
- RAG Retrieval: Integrates retrieval-augmented generation for accurate information lookup
- Multi-Agent Support: Specialized agents for policies, packages, general inquiries, troubleshooting, and billing
- LLM Integration: Powered by OpenAI's language model (gpt-4o-mini) for natural language understanding and generation

## Architecture
<img width="818" height="1031" alt="Teleco_chat drawio" src="https://github.com/user-attachments/assets/ead2fd80-7e05-42f4-80ca-6e574d4eefbe" />




