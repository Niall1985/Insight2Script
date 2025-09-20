# Insight2Script Backend

This backend powers the **Insight2Script** application.  
It provides content generation, research aggregation, and trend analysis services that the frontend consumes through an API.

---

## 🚀 Project Overview

The backend is organized into modular agents and tools.  
Each **agent** is responsible for a higher-level task (e.g., research, trend analysis, query processing), while **tools** provide lower-level utilities for data collection from external sources like Wikipedia, Reddit, or news sites.

The system is designed around these principles:
- **Separation of concerns**: Agents handle orchestration, tools handle data collection.  
- **Extensibility**: New research sources or agents can be easily added.  
- **LLM-ready**: Data is structured into clean JSON/text for further processing.  

---

## 📂 Project Structure

### Root Files
- **`backend_server.py`**  
  Main entry point for the backend server (Flask/FastAPI expected). Exposes REST API endpoints to the frontend.

- **`analytics_main.py`**  
  Script to handle analytics/metrics logic (possibly aggregating research and content statistics).

- **`content_main.py`**  
  Orchestrates the content generation pipeline, pulling from agents and tools to return the final output.

- **`.env`**  
  Environment configuration file (API keys, passwords, etc.).

---

### Content Generation
- **`content_generator/content_agent.py`**  
  Handles LLM-powered text/content generation based on prompts provided by the frontend.

---

### Query Processing
- **`query_processor/query_agent.py`**  
  Manages prompt preprocessing, query refinement, and parsing before sending requests to research or content agents.

---

### Research Agents
- **`research_agent/agent.py`**  
  Main research orchestration agent. Calls external tools to fetch research content.  
- **`research_agent/ddgs_scraper.py`**  
  Scraper for DuckDuckGo Search results.  
- **`research_agent/intermediate_summarizer.py`**  
  Summarizes intermediate results before final aggregation.  
- **`research_agent/serp_content_extractor.py`**  
  Extracts and processes content from SERP (Search Engine Results Page).

---

### Research Tools
- **`research_tools/ddg_tool.py`**  
  Utility wrapper for DuckDuckGo search API.  
- **`research_tools/serp_tool.py`**  
  Fetches structured SERP results (Google/Bing, etc.).  
- **`research_tools/wiki_tool.py`**  
  Wikipedia content extractor.  

---

### Trends Agents
- **`trends_agent/agent.py`**  
  Orchestrates trend analysis tasks. Pulls from `trends_tool` utilities and produces structured trend data.  

---

### Trends Tools
- **`trends_tool/news_tool.py`**  
  Fetches news articles for trend tracking.  
- **`trends_tool/search_tool.py`**  
  Searches queries to analyze popularity.  
- **`trends_tool/yt_tool.py`**  
  Extracts YouTube trends (views, metadata, transcripts).  

---

## 🔄 Data Flow

1. **Frontend sends a request** → to `backend_server.py`.  
2. **Query Processing** → `query_processor/query_agent.py` refines the query.  
3. **Research & Trends**:  
   - Research data → `research_agent/agent.py` calls tools (Wiki, Reddit, SERP).  
   - Trend data → `trends_agent/agent.py` calls tools (News, Search, YouTube).  
4. **Intermediate Summarization** → Condenses raw results (`intermediate_summarizer.py`).  
5. **Content Generation** → `content_generator/content_agent.py` (LLM-powered text output).  
6. **Response** → Sent back to the frontend as structured JSON with:  
   - Generated content  
   - Trend analysis results  

---

## ⚙️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Niall1985/Insight2Script
cd backend
````

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file with your secrets:

```
news_api 
user_agent_api
serp_api 
groq_key1 
groq_key2
groq_key3 
gemini_api 
file_path 
query_key 
content_api 
yt_api
gemini_api2 
```

### 4. Run the Server

```bash
python backend_server.py
```

Server will start at:

```
http://127.0.0.1:5000
```

---

## 📡 API Endpoints

* **`POST /api/generate`**
  Request:

  ```json
  { "prompt": "Explain Nikola Tesla’s contributions" }
  ```

  Response:

  ```json
  {
    "content": "...generated script...",
    "trend_data": {
      "score_2023": 78,
      "reasoning": "Interest in Tesla spiked due to..."
    }
  }
  ```

* **`/api/research`** (planned) – Aggregate multi-source research.

* **`/api/trends`** (planned) – Direct trend analysis results.

---

## 🛠️ Tech Stack

* **Python** (Flask/FastAPI backend)
* **Requests** (API requests & scraping)
* **BeautifulSoup**
* **LangChain with Gemini and LLama** (LLM text generation)


---

## 📌 Notes

* Agents are high-level orchestrators.
* Tools are source-specific fetchers.
* Summarization ensures the LLM doesn’t get overwhelmed by raw data.
* System is modular → easy to add new agents/tools.

---

## 🔮 Future Work

* Add caching layer for repeated queries.
* Improve summarization pipeline.
* Expand trend analysis sources (TikTok, Twitter/X).
* Add unit tests for each agent & tool.

---

