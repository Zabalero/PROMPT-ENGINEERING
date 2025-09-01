---
description: MCP Services Configuration for CursorRIPER.sigma
globs: 
alwaysApply: true
---

# CursorRIPER♦Σ MCP Services Configuration

## 🛠️ MCP Services Selection
# Uncomment the services you want to use and ensure the corresponding MCP server is installed
# All services will follow the CursorRIPER♦Σ permission model and symbolic notation

## 📁 Filesystem Services
@file ".roo/rules/mcp_filesystem.mdc" # Local filesystem operations

## 🔍 Web Search Services
# @file ".roo/rules/mcp_websearch.mdc" # Web search capabilities

## 💻 GitHub Integration
# @file ".roo/rules/mcp_github.mdc" # GitHub repository operations

## 🗄️ Database Operations
# @file ".roo/rules/mcp_database.mdc" # Database query operations

## 🤖 AI Model Operations
# @file ".roo/rules/mcp_aimodel.mdc" # External AI model integration

## 📊 Data Visualization
# @file ".roo/rules/mcp_dataviz.mdc" # Data visualization capabilities

## 🔄 API Integration
# @file ".roo/rules/mcp_apitools.mdc" # API testing and integration

## 🔗 Available MCP Services

# This file serves as a central configuration point for all MCP services in CursorRIPER♦Σ.
# To enable a service, uncomment its @file line above.
# To disable a service, comment out its @file line above.
# Each service follows the CursorRIPER♦Σ permission model and respects RIPER modes.

## ⚙️ Setup Instructions

# 1. Ensure you have the desired MCP servers installed
# 2. Configure .roo/mcp.json with appropriate server settings
# 3. Uncomment the @file lines for the services you want to use
# 4. Restart IDE to apply changes

## 📋 MCP Server Requirements

# Filesystem: npm install -g @modelcontextprotocol/server-filesystem
# Web Search: npm install -g @modelcontextprotocol/server-websearch
# GitHub: npm install -g @modelcontextprotocol/server-github
# Database: npm install -g @modelcontextprotocol/server-database
# AI Model: npm install -g @modelcontextprotocol/server-aimodel
# Data Viz: npm install -g @modelcontextprotocol/server-dataviz
# API Tools: npm install -g @modelcontextprotocol/server-apitools

# See full MCP documentation at: https://modelcontextprotocol.github.io/
