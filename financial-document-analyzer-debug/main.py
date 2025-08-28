# main.py
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid

from crewai import Crew, Process
from agents import financial_analyst
# avoid name collision: import Task as analyze_task
from task import analyze_financial_document as analyze_task

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the Crew with the financial analyst and tasks.
    Provide both query and file_path to the kickoff context so tasks/agents can read the PDF.
    """
    financial_crew = Crew(
        agents=[financial_analyst],
        tasks=[analyze_task],
        process=Process.sequential,
    )

    # pass both query and file path into the Crew context
    context = {'query': query, 'file_path': file_path}
    result = financial_crew.kickoff(context)
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Summarize the attached financial document")
):
    """Analyze financial document and provide comprehensive (non-personalized) recommendations and summary."""
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"

    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Validate query
        if not query:
            query = "Summarize the attached financial document"

        # Run crew with query & file path
        response = run_crew(query=query.strip(), file_path=file_path)

        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
