# agents.py
import os
from dotenv import load_dotenv
load_dotenv()

# Agent class (CrewAI)
from crewai.agents import Agent

# Tools (from tools.py)
from tools import search_tool, FinancialDocumentTool

# Initialize LLM (best-effort). Replace with your specific LLM initialization if required.
try:
    from crewai import LLM
    # This may require environment configuration (CREWAI_API_KEY, etc.)
    llm = LLM()
except Exception:
    # fallback to None; Agent constructors may accept None depending on SDK version
    llm = None

# Creating an experienced financial analyst agent (safe, factual)
financial_analyst = Agent(
    role="Senior Financial Analyst - objective document summarizer",
    goal=(
        "Read the provided financial document and extract key financial metrics "
        "(e.g., total revenue, net income, operating income, free cash flow). Provide a concise, "
        "fact-based summary of operational highlights, material risks, and potential opportunities. "
        "Do NOT give personalized investment advice; instead provide neutral analysis and suggest "
        "consulting a licensed financial professional for investment decisions."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are an experienced financial analyst who emphasizes accuracy and cites the document when possible. "
        "If uncertain, explicitly state uncertainty. Use available tools to read the PDF and (only if needed) to corroborate facts."
    ),
    tools=[FinancialDocumentTool.read_data_tool, search_tool] if search_tool is not None else [FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=3,
    max_rpm=10,
    allow_delegation=False
)

# Verifier agent - checks whether the uploaded file looks like a financial document
verifier = Agent(
    role="Financial Document Verifier",
    goal=(
        "Determine whether the uploaded file is a financial report (earnings release, investor deck, 10-Q/10-K, etc.). "
        "Return a boolean flag and a short rationale referencing evidence from the document."
    ),
    verbose=True,
    memory=False,
    backstory=(
        "You are detail-oriented and compliance-aware. Look for hallmarks like tables, sections labeled 'Total revenues', 'Net income', 'Financial summary', 'Outlook', etc."
    ),
    tools=[FinancialDocumentTool.read_data_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)
