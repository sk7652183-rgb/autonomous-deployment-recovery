# 🚀 AI-Powered Autonomous Deployment Recovery Platform

An AI-powered DevOps platform designed to automatically detect deployment failures, analyse logs, identify probable root causes, recommend remediation actions, and help recover failed deployments with minimal manual intervention.

> 🚧 This project is currently being developed as part of a hackathon.

---

## 🎯 Problem Statement

When a production deployment fails, DevOps engineers often need to manually:

- Analyse deployment logs
- Check application logs
- Identify the root cause
- Determine the appropriate fix
- Redeploy the application
- Verify whether the issue has been resolved

This manual troubleshooting process can increase **Mean Time To Recovery (MTTR)** and delay application recovery.

---

## 💡 Proposed Solution

The **Autonomous Deployment Recovery Platform** aims to automate this workflow using AI and DevOps tools.

The platform will:

- 🔍 Detect deployment failures
- 📋 Analyse GitHub Actions and AWS CloudWatch logs
- 🤖 Identify probable root causes using AI
- 💡 Recommend remediation actions
- 🔧 Create fixes and GitHub Pull Requests
- 👤 Allow human approval before applying changes
- 🚀 Automatically redeploy or roll back
- ❤️ Verify application health after recovery

---

## 🏗️ Current Architecture

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
Docker
    │
    ▼
AWS Elastic Beanstalk
    │
    ▼
FastAPI Application
    │
    ▼
/health Endpoint
