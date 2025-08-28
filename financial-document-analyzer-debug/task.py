# task.py
from crewai import Task
from agents import financial_analyst, verifier
from tools import search_tool, FinancialDocumentTool

analyze_financial_document = Task(
    description=(
        "Read the financial document located at {file_path} and optional user query {query}. "
        "Extract key metrics (total revenue, net income, operating income, cashflow where available), "
        "produce a concise factual summary, list material risks and opportunities, and output a structured result. "
        "Do NOT provide personalized financial advice; encourage consulting a licensed financial professional as appropriate."
    ),
    expected_output=(
        "A structured response like: { 'summary': str, 'key_metrics': dict, 'risks': [str], 'opportunities': [str], 'notes': str }"
    ),
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool, search_tool] if search_tool is not None else [FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

investment_analysis = Task(
    description="Non-personalized factual analysis of financial drivers and sensitivity.",
    expected_output="Factual analysis with suggestions for follow-ups (no personalized investment recommendations).",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

risk_assessment = Task(
    description="Produce a risk summary (regulatory, operational, supply-chain, macro).",
    expected_output="List of risks with short rationale.",
    agent=financial_analyst,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False,
)

verification = Task(
    description="Check whether file seems to be a financial report and provide the evidence.",
    expected_output="{'is_financial': bool, 'evidence': str}",
    agent=verifier,
    tools=[FinancialDocumentTool.read_data_tool],
    async_execution=False
)
