# tools.py
## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

# Search tool (Serper dev tool wrapper)
try:
    from crewai_tools.tools.serper_dev_tool import SerperDevTool
    search_tool = SerperDevTool()
except Exception:
    # If Serper tool is not available/configured, set a safe placeholder
    search_tool = None

# PDF reading: use PyPDF2 (add to requirements). It's a robust lightweight reader for text extraction.
try:
    from PyPDF2 import PdfReader
except Exception:
    PdfReader = None

class FinancialDocumentTool:
    @staticmethod
    async def read_data_tool(path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path.

        Returns the full text content or raises FileNotFoundError.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"PDF not found at path: {path}")

        if PdfReader is None:
            # Clear, actionable error for the user
            return "PyPDF2 is not installed. Please add PyPDF2 to requirements and reinstall."

        try:
            reader = PdfReader(path)
            full_report = ""
            for page in reader.pages:
                content = page.extract_text() or ""
                # normalize line endings and extra blank lines
                content = content.replace("\r\n", "\n")
                while "\n\n" in content:
                    content = content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

class InvestmentTool:
    @staticmethod
    async def analyze_investment_tool(financial_document_data: str):
        """
        Minimal investment heuristics placeholder.
        Returns a dict; implement richer logic as needed.
        """
        import re
        result = {"summary": "", "metrics": {}}
        # very simple pattern extraction (example)
        m = re.search(r"Total revenues\s*[:\-]?\s*([0-9\.,]+)", financial_document_data, re.IGNORECASE)
        if m:
            result["metrics"]["total_revenues"] = m.group(1)
        result["summary"] = "Placeholder investment analysis. Implement real analysis logic here."
        return result

class RiskTool:
    @staticmethod
    async def create_risk_assessment_tool(financial_document_data: str):
        """
        Very light heuristic risk detection. Expand for production.
        """
        import re
        risks = []
        if re.search(r"\brisk\b", financial_document_data, re.IGNORECASE):
            risks.append("Document contains explicit 'risk' language — read those sections carefully.")
        if re.search(r"tariff|tariffs|trade", financial_document_data, re.IGNORECASE):
            risks.append("Mentions of tariffs/trade may impact margins or supply chain.")
        return {"risks": risks, "note": "Heuristic-only; build quantitative risk models for production."}
