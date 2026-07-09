# 💊 DACM AI – Clinical Decision Support System for Contraceptive Care

> A hybrid AI platform delivering personalized, WHO-guideline-backed contraceptive recommendations with behavioral satisfaction prediction and automated high-risk patient triage for Sub-Saharan Africa.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Go 1.21+](https://img.shields.io/badge/go-1.21+-00ADD8.svg)](https://golang.org/dl/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688.svg)](https://fastapi.tiangolo.com/)

---

## 🎯 Problem Statement

Contraceptive discontinuation rates exceed 40% in Sub-Saharan Africa due to:
- Lack of personalized, guideline-aligned counseling
- Unaddressed behavioral factors (side effects, satisfaction)
- Limited access to trained providers in rural areas
- Privacy concerns preventing open consultation

DACM AI addresses this by combining clinical safety rules, regional prevalence data, and behavioral ML to deliver trustworthy, actionable recommendations.

---

## ✨ Key Features

### 🩺 Clinical Intelligence
- **WHO MEC Guideline Engine**: Rule-based safety checks for 12+ clinical parameters (hypertension, migraines with aura, DVT history, breastfeeding, etc.)
- **RAG-Powered Recommendations**: ChromaDB retrieval of WHO MEC guidelines + Groq LLM synthesis for empathetic, evidence-based advice
- **Critical Risk Flagging**: Auto-blocks contraindicated methods and routes high-risk cases to counselor dashboard

### 🤖 Behavioral Prediction
- **LightGBM Satisfaction Model** (0.919 AUC): Predicts user adherence risk based on historical review patterns
- **Personalized Counseling Prompts**: Recommends "counseling_recommended" when satisfaction probability <50%

### 🌍 Regional Context
- **WHO Africa DHS Integration**: 1,161 prevalence records across 54 African countries for localized counseling
- **Dynamic Country Filtering**: Real-time retrieval of method usage statistics by ISO3 country code

### 🔒 Privacy & Compliance
- **Zero-PII Architecture**: SHA-256 identity hashing ensures patient anonymity in counselor workflows
- **Masked Contact Handling**: Counselors see `em***@gmail.com`, never raw emails/phones
- **Audit Logging**: All case flags, appointments, and admin actions timestamped and traceable

### 🩺 Counselor & Admin Portals
- **Blinded Case Dashboard**: Counselors review flagged cases without accessing patient identity
- **Telehealth Scheduling**: One-click Google Meet link generation with simulated email/SMS dispatch
- **System Health Monitoring**: Real-time status checks for Go backend, Python AI, and database connectivity

---

## 🏗️ Architecture Overview
