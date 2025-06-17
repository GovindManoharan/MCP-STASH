# 🧠 MCP-Powered AI Agents Demo

This repository demonstrates how to use [Model Context Protocol (MCP)](https://modelcontextprotocol.io) to build AI agents powered by external tools like Airtable, Notion, MongoDB, and financial data providers using FastAPI, LangChain, and MCP servers.

---

## 📚 Reference Links

1. **📽️ MCP Explained (Video):** [YouTube](https://youtu.be/FLpS7OfD5-s?si=NQD7P2w-vyc3sFtZ)  
2. **⭐ Awesome MCP Servers:** [GitHub](https://github.com/punkpeye/awesome-mcp-servers?tab=readme-ov-file)  
3. **🔗 LangChain MCP Adapters:** [GitHub](https://github.com/langchain-ai/langchain-mcp-adapters)  
4. **⚙️ Langchain MCP-Use:** [GitHub](https://github.com/mcp-use/mcp-use)  
5. **🚀 FastAPI MCP Template:** [GitHub](https://github.com/tadata-org/fastapi_mcp)  
6. **🔌 Official MCP Servers:** [GitHub](https://github.com/modelcontextprotocol/servers)  
7. **📖 MCP Docs (Anthropic):** [Quickstart](https://modelcontextprotocol.io/quickstart/server)  
8. **🎓 MCP Course (DeepLearning.ai):** [Course Link](https://learn.deeplearning.ai/courses/mcp-build-rich-context-ai-apps-with-anthropic/lesson/fkbhh/introduction)

---

## 🛠️ Project Setup

### ✅ Step 1: Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### ✅ Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ Step 3: API Keys Setup

Generate the following API keys:

- **OpenAI** – https://platform.openai.com
- **Notion** – https://www.notion.so/my-integrations
- **Airtable** – https://airtable.com/account

Place them in your `.env` files and in the appropriate JSON config files inside the `mcp-servers` folder.

---

## 🔌 Using External MCP Server (e.g., Airtable)

### 🚦 Run Airtable MCP Sample

```bash
cd external-mcp-server/mcp-use
python airtable-with-use-mcp.py
```

---

## 🧪 Using Dummy Data for Call Center Agent

### ✅ Step 1: Setup Local MongoDB

1. Install MongoDB: https://www.mongodb.com/try/download/community
2. Start MongoDB and create a database called `call_canter_db`.
3. Inside that DB, create collections:
   - `claims`
   - `pa_requests`
4. Import data from the `/data` folder using MongoDB Compass or CLI:

```bash
mongoimport --db call_canter_db --collection claims --file ./data/claims.json --jsonArray
mongoimport --db call_canter_db --collection pa_requests --file ./data/pa_requests.json --jsonArray
```

---

## ⚙️ Running the APIs and Agents

### 🛰️ Run Dummy API Server

```bash
cd dummy-data
uvicorn main:app --reload
```

### 🤖 Run Call Center Agent with API as Tools

```bash
cd call-prediction-agent
uvicorn CallCenterPredictions:app --host 0.0.0.0 --port 9000 --reload
```

Test via Swagger at: http://localhost:9000/docs#/default/predict_call_reason_predict_post

Use this payload:

```json
{
  "user_id": "U234567890"
}
```

---

## 🔄 Using MCP Server with Local Dummy Data

### 🛠️ Run Local MCP Server

```bash
cd dummy-data
python mcpServer.py
```

### 🚀 Run Agent to Interact with MCP Server

```bash
cd call-prediction-agent
uvicorn CallCenterMcpClient:app --host 0.0.0.0 --port 9000 --reload
```

Try this query in Swagger UI:

> "Why is user U234567890 calling the agent? Based on his data, what will he need clarifications for?"

---

## 📈 Testing with External Finance APIs + MCP Inspector

### 🔑 Required API Keys

- https://site.financialmodelingprep.com/
- https://gnews.io/

### 👁️‍🗨️ Run Inspector for External APIs

```bash
cd call-prediction-agent
npx @modelcontextprotocol/inspector uv run financeMCPServer.py
# or alternatively:
mcp dev financeMCPServer.py
```

Open the inspector at http://127.0.0.1:6274

### ⚡ Run the Financial Prediction Agent

```bash
cd finance-agent
uvicorn MCPFinancePrediction:app --host 0.0.0.0 --port 9000 --reload
```

---

## 🧼 Tips

- Make sure your `.env` and config JSONs are updated with proper API keys before testing.
- If using multiple terminals, label them to avoid confusion (e.g., Server, Agent, Inspector).
- Ensure MongoDB is running while testing the dummy-data setup.

---

## 📬 Questions or Feedback?

Open an issue or contact the maintainers. Contributions are welcome!