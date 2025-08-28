# Financial Document Analyzer with CrewAI

This project is an AI-powered financial document analysis system built with CrewAI and FastAPI. It allows users to upload a corporate financial report (in PDF format) and receive a comprehensive investment analysis, including key insights, a bull vs. bear case, and a final recommendation.

## Features

-   **PDF Document Upload**: Securely upload financial documents via a REST API endpoint.
-   **AI-Powered Analysis**: Utilizes a crew of specialized AI agents to perform in-depth financial analysis.
-   **Structured Reporting**: Generates a professional investment report with an executive summary, investment thesis, and risk assessment.
-   **Sequential Task Processing**: The AI crew first analyzes the document for key data and then synthesizes that data into a final report.

## System Architecture

The application uses a multi-agent framework powered by **CrewAI**:

1.  **Financial Analyst Agent**: This agent's primary role is to read the uploaded financial document using a specialized tool. It extracts critical data points, including financial health metrics (margins, cash flow), operational highlights (production numbers), growth strategies, and identified risks.

2.  **Investment Advisor Agent**: This agent takes the structured analysis from the Financial Analyst. Its role is to synthesize this information into a high-level investment report, creating a narrative that is easy for an investor to understand. It formulates the bull case, bear case, and provides a final, justified recommendation.

The process is managed by a **Crew** that executes two sequential tasks: first the analysis, then the reporting.

---

## Bugs Found and Fixed

The original codebase was non-functional and contained several critical bugs and design flaws. This submission addresses them as follows:

1.  **Unprofessional Agent & Task Prompts**:
    * **Bug**: The core logic of the AI agents and tasks was satirical, instructing them to generate nonsensical and fabricated financial advice.
    * **Fix**: All agent roles, goals, backstories, and task descriptions have been completely rewritten to be professional and aligned with a genuine financial analysis workflow.

2.  **Missing LLM Initialization**:
    * **Bug**: The language model (`llm`) was never initialized (`llm = llm`).
    * **Fix**: The code now correctly initializes the Google Gemini LLM using `langchain_google_genai` and loads the API key from a `.env` file.

3.  **Broken Document Reading Tool**:
    * **Bug**: The tool for reading PDFs was non-functional due to a missing import (`Pdf` class) and a poor design that made it impossible to pass the uploaded file's path.
    * **Fix**: The tool was rebuilt using the standard `PyPDFLoader` from `crewai_tools` and decorated with `@tool` for simplicity and reliability.

4.  **Ineffective Crew Structure**:
    * **Bug**: The main crew was not receiving the uploaded file path as input, causing it to always analyze a default placeholder file. The crew was also poorly designed with only a single agent and task.
    * **Fix**: The `main.py` was updated to correctly pass the `file_path` to the crew's `kickoff` method. The crew was restructured to use two specialized agents (analyst and advisor) and two sequential tasks, leveraging the power of CrewAI for better results.

5.  **Dependency Issues**:
    * **Bug**: The `requirements.txt` file was missing key libraries required for the application to run (`langchain-google-genai`, `python-dotenv`, `pypdf`).
    * **Fix**: The `requirements.txt` file has been updated with all necessary dependencies.

---

## Setup and Installation

### Prerequisites

-   Python 3.9+
-   A Google Gemini API Key

### Instructions

1.  **Clone the Repository**:
    ```sh
    git clone <your-repo-link>
    cd financial-document-analyzer
    ```

2.  **Create and Activate a Virtual Environment**:
    ```sh
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**:
    * Create a file named `.env` in the root of the project.
    * Add your Google Gemini API key to it:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```

5.  **Prepare Sample Document**:
    * Create a `data` folder in the project root.
    * Place a sample financial PDF in this folder (e.g., `TSLA-Q2-2025-Update.pdf`).

---

## How to Run the Application

Execute the following command in the terminal from the project's root directory:

```sh
uvicorn main:app --reload
