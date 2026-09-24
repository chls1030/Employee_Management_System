<div align="center">

# 🚀 ActiveHR: AI-Driven Standalone HRM System

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Eel](https://img.shields.io/badge/Framework-Eel-success.svg)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid_Desktop-orange.svg)

> **Transforming "Data Entry" into "Data Utilization."**  
> A modern, algorithmic human resource management system that shifts from passive record-keeping to an active, thinking talent brain.

</div>

---

## 📌 Executive Summary

Traditional HRM systems often function merely as digital filing cabinets, leading to data silos, reliance on manual calculations, and subjective human bias in salary leveling and promotions. 

This project aims to solve these enterprise challenges by introducing a **"Full-Lifecycle Talent Closed Loop."** Built as a secure, standalone desktop application, it integrates an automated **Smart Talent Engine** that drives objective, data-driven decisions at every stage of an employee's career—from Day 1 onboarding to senior promotions.

---

## 🌟 Core Innovations & Algorithmic Logic

Unlike standard CRUD applications, this system implements complex, real-world corporate governance rules via code:

* **🤖 AI Smart Onboarding & Leveling**  
  Eliminates human bias during hiring. The algorithm takes *Education* and *Experience* constraints to automatically calculate the appropriate starting level and standardize salary brackets across the company.

* **📈 Continuous Performance Tracking**  
  Replaces isolated annual reviews with a continuous timeline of ratings (S, A, B, C, D). This continuous data serves as the "fuel" for the promotion engine.

* **⚙️ Smart Promotion Engine (Batch Scanning)**  
  An automated engine that scans all eligible employees simultaneously. It evaluates candidates through strict logic filters: **Tenure + Performance History + Compliance**. It generates human-readable "Engine Reasons" for full transparency and auditability.

* **🛡️ Advanced Safeguards (Edge Case Intelligence)**
  * **Education Acceleration:** Master's degree holders algorithmically receive a 'Tenure Discount' for basic levels.
  * **Executive Decoupling:** Senior promotions (P4+ levels) automatically deactivate degree accelerators, strictly enforcing merit-only evaluations.
  * **Hard Rule Interception:** Strict UI/Backend policy overrides prevent internal manipulation (e.g., blocking unauthorized salary adjustments).

---

## 📸 System Walkthrough

> 💡 **Placeholder for Screenshots:** Replace the links below with your actual image paths to showcase the UI.

<div align="center">

![Global Dashboard](link_to_dashboard_screenshot)
*Figure 1: Modern Global Dashboard with Real-time Metrics and i18n Support.*

<br>

![Smart Promotion Engine](link_to_promotion_engine_screenshot)
*Figure 2: The Smart Promotion Engine automatically evaluating candidate eligibility based on continuous performance data.*

</div>

---

## 🏗️ System Architecture & Tech Stack

The system operates on a hybrid architecture, designed specifically for standalone, secure desktop environments without relying on external cloud servers, ensuring strict data privacy.

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | `Python 3` | Core engine handling complex algorithms (Smart Talent) and database interactions. |
| **Frontend** | `HTML5 / CSS3 / JS` | Provides a highly responsive, modern dashboard interface. |
| **Bridge** | `Eel` | Chromium-based UI framework connecting JS frontend to Python backend via asynchronous API calls. |
| **Database** | `SQLite3` | Lightweight, reliable data persistence with built-in local backup functionalities. |
| **I18n** | `JSON Locales` | Seamless UI localization supporting English, Chinese, and scalable to other languages. |

---

## 🔐 Security & Access Control

Enterprise-grade data segregation is enforced via **Role-Based Access Control (RBAC)**:

* **Standard Employees:** Limited view strictly restricted to their own personal records.
* **HR Admins:** Full organizational access with automated audit trails for sensitive compensation changes.

---

## 🚀 Reproducibility: How to Run Locally

This project is built with reproducibility in mind. Follow these steps to set up and run the application on your local machine:

**1. Clone the repository & Install dependencies:**
```bash
git clone https://github.com/chls1030/Employee_Management_System.git
cd Employee_Management_System
pip install -r requirements.txt
``` 
**2. Initialize database & Seed data:**
```bash
python database_setup.py
python seed_data.py
```
**3. Launch the application:**
```bash
python main_eel.py
``` 
## 🔮 Future Roadmap (Research & Extension)
As part of continuous improvement, the following architectural upgrades are considered for future releases:
* 🧠 Machine Learning Integration: Replacing static programmatic leveling logic with a lightweight ML model to predict appropriate levels based on historical promotion data.
* ☁️ Cloud Synchronization: Transitioning from local SQLite to AWS RDS or Firebase to support multi-HR concurrent collaboration while preserving the desktop client's speed.
* 📜 Advanced Audit Logging: Implementing a dedicated blockchain-inspired immutable ledger for salary and promotion overrides to guarantee 100% auditability.
<div align="center">
<br>
<i>Designed & Developed by <b>Gao Chengcheng</b></i>
</div>
```
