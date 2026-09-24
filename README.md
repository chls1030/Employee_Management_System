# 🚀 ActiveHR: AI-Driven Standalone HRM System

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey.svg)
![Eel](https://img.shields.io/badge/Framework-Eel-success.svg)
![Architecture](https://img.shields.io/badge/Architecture-Hybrid_Desktop-orange.svg)

> **Transforming "Data Entry" into "Data Utilization."**  
> A modern, algorithmic human resource management system that shifts from passive record-keeping to an active, thinking talent brain. 

## 📌 Executive Summary
Traditional HRM systems often function merely as digital filing cabinets, leading to data silos, reliance on manual calculations, and subjective human bias in salary leveling and promotions. 

This project aims to solve these enterprise challenges by introducing a **"Full-Lifecycle Talent Closed Loop."** Built as a secure, standalone desktop application, it integrates an automated **Smart Talent Engine** that drives objective, data-driven decisions at every stage of an employee's career—from Day 1 onboarding to senior promotions.

---

## 🌟 Core Innovations & Algorithmic Logic

Unlike standard CRUD applications, this system implements complex, real-world corporate governance rules via code:

*   **🤖 AI Smart Onboarding & Leveling:** 
    Eliminates human bias during hiring. The algorithm takes *Education* and *Experience* constraints to automatically calculate the appropriate starting level and standardize salary brackets across the company.
*   **📈 Continuous Performance Tracking:** 
    Replaces isolated annual reviews with a continuous timeline of ratings (S, A, B, C, D). This continuous data serves as the "fuel" for the promotion engine.
*   **⚙️ Smart Promotion Engine (Batch Scanning):** 
    An automated engine that scans all eligible employees simultaneously. It evaluates candidates through strict logic filters: **Tenure + Performance History + Compliance**. It generates human-readable "Engine Reasons" for full transparency and auditability.
*   **🛡️ Advanced Safeguards (Edge Case Intelligence):**
    *   **Education Acceleration:** Master's degree holders algorithmically receive a 'Tenure Discount' for basic levels.
    *   **Executive Decoupling:** Senior promotions (P4+ levels) automatically deactivate degree accelerators, strictly enforcing merit-only evaluations.
    *   **Hard Rule Interception:** Strict UI/Backend policy overrides prevent internal manipulation (e.g., blocking unauthorized salary adjustments).

---

## 📸 System Walkthrough
*(⚠️ Note to applicant: Please upload 2-3 high-quality screenshots from your slides here. Delete this text and use the format below)*

![Global Dashboard](link_to_dashboard_screenshot)
*Figure 1: Modern Global Dashboard with Real-time Metrics and i18n Support.*

![Smart Promotion Engine](link_to_promotion_engine_screenshot)
*Figure 2: The Smart Promotion Engine automatically evaluating candidate eligibility based on continuous performance data.*

---

## 🏗️ System Architecture & Tech Stack

The system operates on a hybrid architecture, designed specifically for standalone, secure desktop environments without relying on external cloud servers (ensuring data privacy).

*   **Backend (Core Engine):** `Python 3` handles the complex algorithms (Smart Talent Engine, AI Leveling) and secure database interactions.
*   **Frontend (UI/UX):** `HTML5 / CSS3 / JavaScript` provides a highly responsive, modern dashboard interface.
*   **Bridge Framework:** `Eel` (Chromium-based UI) connects the JS frontend to the Python backend via asynchronous API calls (`@eel.expose`).
*   **Database:** `SQLite3` provides lightweight, reliable data persistence with built-in one-click local backup functionalities.
*   **Localization:** `JSON-based i18n Locales` enabling seamless switching between languages (English, Chinese, etc.).

---

## 🔐 Security & Access Control
Enterprise-grade data segregation is enforced via **Role-Based Access Control (RBAC)**. 
*   **Standard Employees:** Limited view restricted to their own personal records.
*   **HR Admins:** Full organizational access with automated audit trails for sensitive compensation changes.

---

## 🚀 Reproducibility: How to Run Locally

This project is built with reproducibility in mind. Follow these steps to run the application on your local machine:

**1. Clone the repository:**
```bash
git clone https://github.com/chls1030/Employee_Management_System.git
cd Employee_Management_System
2. Install dependencies:
code
Bash
pip install -r requirements.txt
3. Initialize the Database & Seed Mock Data:
(This will create company.db and populate it with test employees and historical performance data).
code
Bash
python database_setup.py
python seed_data.py
4. Launch the Application:
code
Bash
python main_eel.py
🔮 Future Roadmap (Research & Extension)
As part of continuous improvement, the following architectural upgrades are considered:
Machine Learning Integration: Replacing static programmatic leveling logic (e.g., experience / 2.5) with a lightweight ML model to predict levels based on historical promotion data.
Cloud Synchronization: Transitioning from local SQLite to AWS RDS/Firebase to support multi-HR concurrent collaboration while preserving the desktop client's speed.
Advanced Audit Logging: Implementing a dedicated blockchain-inspired immutable ledger for salary and promotion overrides.
Designed & Developed by Gao Chengcheng
code
Code
### 💡 为什么这样写能打动博士面试官？

1.  **开篇定调高**：用 `Executive Summary`（摘要）替代了普通的简介，直接点出**行业痛点**（数据孤岛、主观偏见）和你的**解决方案**（全生命周期闭环），证明你有很强的发现问题和定义问题的能力（Research Proposal 的核心）。
2.  **突出逻辑而非语法**：在 `Core Innovations` 部分，没有去罗列“增删改查”这种初级功能，而是强调了**算法（Algorithmic Logic）**和**防御性编程（Safeguards/Edge Cases）**。比如 *Education Acceleration* 和 *Executive Decoupling*，这向教授展示了你具备将复杂现实业务抽象成代码逻辑的**建模能力**。
3.  **学术界最看重的 Reproducibility（可复现性）**：`How to Run Locally` 部分指令极其清晰，任何教授或博士后只需复制粘贴这 4 行代码，就能完美跑起你的程序，这在学术界是非常受人尊敬的素养。
4.  **Future Roadmap（画龙点睛）**：这一段直接拔高了项目的科研属性，提到了引入 ML 模型和不可篡改日志，告诉教授：“我不只是个码农，我还有进一步做科研探索的 Vision”。

**最后一步提醒**：
一定要记得把 Markdown 里的 `![Global Dashboard](link_to_dashboard_screenshot)` 换成你**系统真实的截图链接**！图文并茂是第一生产力！祝你欧陆博士申请顺利！
