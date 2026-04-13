<div align="center">

# 💎 SQL AI
### The Intelligent Semantic Layer for Enterprise Data Teams

<br/>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![DeepSeek V3](https://img.shields.io/badge/LLM-DeepSeek_V3-6366F1?style=for-the-badge)](https://deepseek.com)
[![LangChain](https://img.shields.io/badge/Agent-LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Interface-Premium_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![PostgreSQL](https://img.shields.io/badge/Scalability-PostgreSQL_Ready-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)

<br/>

**Daniel SQL AI** is a production-grade, autonomous Data Intelligence Agent designed to bridge the chasm between raw relational databases and executive decision-making. By leveraging the reasoning capabilities of DeepSeek-V3 and the orchestration of LangChain, Daniel transforms natural language into high-fidelity, safe SQL analytics.

[**Architecture**](#-architecture-blueprints) • [**Capabilities**](#-core-capabilities) • [**Setup**](#-lightning-deployment) • [**Security**](#-security--safety-protocols)

---

</div>

## 🚀 The Value Proposition

In the modern enterprise, data is the new oil, but the "extraction process" (SQL) remains a critical bottleneck.

*   **Zero-Knowledge Barrier**: Empower non-technical stakeholders to query complex schemas without learning SQL.
*   **Eliminate Latency**: Say goodbye to "Analytical Backlogs" and Jira tickets for simple data pulls.
*   **Contextual Reasoning**: Unlike standard Text-to-SQL, Daniel understands schema relationships and business intent.

---

## ✨ Core Capabilities

### 🧠 Autonomous Agentic Reasoning
Daniel doesn't just "guess" SQL. It operates via a robust **ReAct (Reason + Action) loop**:
*   **Schema Discovery**: Dynamically inspects tables and column types before proposing a query.
*   **Self-Correction**: If a query fails due to syntax or logic, the agent analyzes the traceback and iterates.
*   **Multi-Step Analysis**: Capable of complex JOINs and CTE generation for deep insights.

### 📊 Predictive Visualization Engine
Stop staring at rows. Daniel detects the shape of your result set and selects the optimal Plotly visualization.
*   **Time-Series**: Spline charts for revenue/usage trends.
*   **Breakdowns**: Donut and Bar charts for categorical distribution.
*   **Executive Metrics**: Instant summary statistics (Mean, Median, Std Dev) for every result.

### 📥 Enterprise Exfiltration
One-click export of structured datasets to high-fidelity Excel (`.xlsx`) files for further offline modeling.

---

## 🛡️ Security & Safety Protocols

Enterprise data safety is not an afterthought; it is the core of our architecture.

1.  **Layer 1: Semantic Auditing**: Real-time heuristic check for destructive keywords (`DROP`, `DELETE`, `TRUNCATE`).
2.  **Layer 2: Read-Only Constrainment**: The environment is strictly SELECT-only. No DML/DDL operations can pass.
3.  **Layer 3: Row-Level Safety**: Automated `LIMIT` injection (default 100 rows) prevents memory exhaustion and system DOS.
4.  **Complexity Scoring**: Pre-execution analysis flags performance-heavy queries (e.g., recursive joins).

---

## 📑 Architecture Blueprints

### The nexus of Intelligence
```mermaid
graph TD
    A[Business User] -->|Natural Language| B[Daniel Intelligence Agent]
    B --> C{Strategic Planner}
    C -->|Schema Request| D[Schema Inspector]
    D -->|Table Info| C
    C -->|SQL Generation| E[Safe SQL Executor]
    E -->|Validation Check| F[Relational DB]
    F -->|Dataset| G[Result Parser]
    G --> H[Visualizer Engine]
    H --> I[Executive Dashboard]
    E -->|Logic Error| C
```

---

## ⚡ Lightning Deployment

### 1. Provision Environment
```bash
git clone https://github.com/Daniel-pk/Daniel-SQL-AI.git
cd Daniel-SQL-AI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Credentials
Create a `.env` file in the root directory:
```env
DEEPSEEK_API_KEY=your_sk_key
DATABASE_TYPE=sqlite  # or postgresql
# If postgres: POSTGRES_DB_URL=postgresql://user:pass@host:port/db
```

### 3. Launch the Hub
```bash
streamlit run app.py
```

---

## 🗺️ Roadmap to v3.0

- [x] **v1.0**: Core ReAct Engine + Visualizer.
- [x] **v2.0**: Advanced Security Layer + Excel Export + Schema Explorer.
- [ ] **v2.5**: Semantic Caching (Redis) for instantaneous repeat queries.
- [ ] **v3.0**: Multi-Agent Orchestration (Specialized Visual Agents).

---

<div align="center">

Built with ❤️ by [Daniel](https://github.com/daniellopez882/)

**Transforming raw data into mission-critical intelligence.**

</div>
