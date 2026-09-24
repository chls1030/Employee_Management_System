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

<div align="center">

**1. Modern Global Dashboard & i18n Support**
<br>
<img src="./assets/dashboard.png" alt="Global Dashboard" width="800"/>
<br>
<i>Providing instant workforce insights at a glance, with seamless multi-language (English/Chinese) support.</i>
<br><br><br>

**2. AI Smart Onboarding & Leveling**
<br>
<img src="./assets/ai_leveling.png" alt="AI Leveling" width="800"/>
<br>
<i>The AI auto-fill button triggers algorithmic base-leveling using Education + Experience constraints, standardizing salary brackets from Day 1.</i>
<br><br><br>

**3. The Smart Promotion Engine**
<br>
<img src="./assets/promotion_engine.png" alt="Promotion Engine" width="800"/>
<br>
<i>Automated batch scanning of all eligible employees. Generates human-readable "Engine Reasons" ensuring transparent, data-driven promotion decisions.</i>

</div>

<br>
<h3>🧩 Comprehensive HR Modules</h3>
<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <img src="./assets/recruitment.png" alt="Recruitment" width="100%">
      <br>
      <b>Recruitment Kanban</b><br>
      <i>Drag-and-drop candidate management tracking hires from sourcing to formal offers.</i>
    </td>
    <td width="50%" valign="top">
      <img src="./assets/performance.png" alt="Performance" width="100%">
      <br>
      <b>Performance Reviews</b><br>
      <i>Continuous tracking of quarterly and annual ratings, feeding directly into the Smart Talent Engine.</i>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <img src="./assets/invoices.png" alt="Financial Invoices" width="100%">
      <br>
      <b>Financial Invoices</b><br>
      <i>Integrated employee reimbursement tracking with a clear approval workflow and status indicators.</i>
    </td>
    <td width="50%" valign="top">
      <img src="./assets/employees.png" alt="Employee List" width="100%">
      <br>
      <b>Employee Directory</b><br>
      <i>Centralized personnel management with quick actions for adjusting roles, levels, and status.</i>
    </td>
  </tr>
</table>
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

<details>
  <summary><b>🌍 Click to view: Multi-language (i18n) Support in Action</b></summary>
  <br>
  <img src="./assets/i18n_menu.png" alt="i18n Menu" width="400">
  <br><i>Seamlessly switch between English, Chinese, Japanese, French, and more.</i>
</details>
---

## 🔐 Security & Access Control

Enterprise-grade data segregation is enforced via **Role-Based Access Control (RBAC)**.

* **HR Admins:** Full organizational access (recruitment, payroll, promotions).
* **Standard Employees:** Limited view strictly restricted to their own personal records and tasks.

<details>
  <summary><b>👀 Click to compare: HR Admin View vs. Employee View</b></summary>
  <br>
  <p><b>HR Admin View:</b> Full access to global metrics.</p>
  <img src="./assets/dashboard.png" alt="HR View" width="800">
  <br><br>
  <p><b>Employee View:</b> Restricted dashboard protecting company privacy.</p>
  <img src="./assets/employee_dashboard.png" alt="Employee View" width="800">
</details>

<br>

**🛡️ Local Data Ownership & Backup**
Your talent data is never locked in a black box. The system includes built-in local backup functionalities, allowing administrators to securely export the entire SQLite database at any time.

<div align="center">
  <img src="./assets/backup.png" alt="System Backup" width="600">
</div>

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
