# Teleco ChatBot your AI powered virtual assistant chat bot

An intelligent conversational assistant for telecom customer support built with FastAPI, LangChain, and Streamlit. This chatbot leverages advanced language models and retrieval-augmented generation (RAG) to handle customer inquiries across multiple domains including policies, billing, packages, and troubleshooting.
**Supported Languages:** English, Urdu, Arabic

## Overview
The Telecom Chatbot is a multi-agent system designed to provide intelligent customer support with the following capabilities:

- **Multi-Language Support:** Seamlessly handles conversations in English, Urdu, and Arabic
- **Language Detection:** Automatically detects and rejects unsupported languages
- **Security:** Implements guardrails to block malicious or outside queries
- **Intelligent Routing:** Uses a Router Agent to direct queries to specialized agents
- **RAG Retrieval:** Integrates retrieval-augmented generation for accurate information lookup
- **Multi-Agent Support:** Specialized agents for policies, packages, general inquiries, troubleshooting, and billing
- **LLM Integration:** Powered by OpenAI's language model (gpt-4o-mini) for natural language understanding and generation

## Architecture
<img width="818" height="1031" alt="Teleco_chat drawio" src="https://github.com/user-attachments/assets/ead2fd80-7e05-42f4-80ca-6e574d4eefbe" />

- **Language Detection:** Filters unsupported languages at entry
- **Guardrails:** Security layer blocking outside queries
- **Router Agent:** Directs queries to appropriate specialized agents
- **RAG Retrieval:** Retrieves relevant information from knowledge base
- **Specialized Agents:** Policies Agent, Package Agent, General Agent, Troubleshooting Agent, Billing Agent
- **LLM:** OpenAI API for response generation

## Prerequisites

### Tech Stack
- **Backend Framework:** FastAPI
- **Frontend Framework:** Streamlit
- **LLM & Orchestration:** LangChain, LangChain Community
- **Vector Database:** Chroma DB
- **Document Processing:** PyPDFLoader
- **LLM API:** OpenAI API
- **Graph-based Workflows:** LangGraph
- **Language:** Python 3.10+

## Installation
**Option 1: Using Docker Compose (Recommended)**

## Prerequisites
- Docker and Docker Compose installed on your system
- OpenAI API key
