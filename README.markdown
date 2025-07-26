# Court Order Processor

A FastAPI-based application for processing court order PDFs, extracting `national_id` and `action` fields using OpenAI's GPT-3.5-turbo or regex, and performing customer lookups and actions. The app uses LangGraph for workflow orchestration and serves a web interface for PDF uploads.

## Project Structure
```
court_order_processor
├── app.py              # FastAPI application
├── customer_db.py      # Customer database operations
├── actions.py          # Action definitions and processing
├── utils.py            # Utility functions (PDF text extraction, regex)
├── llm_extractor.py    # LLM-based field extraction
├── langgraph_agent.py  # LangGraph workflow orchestration
├── data/
│   ├── customers.csv   # Customer data
│   └── actions.csv     # Action log
├── templates/
│   └── index.html      # Web interface
├── static/
│   └── styles.css      # CSS styles
├── docs/
│   └── workflow.mmd    # Mermaid workflow diagram
├── README.md           # Project documentation
├── requirements.txt    # Dependencies
└── run_colab.py        # Colab script to run the app
```

## Prerequisites
- Python 3.11+
- Git
- OpenAI API key (from [platform.openai.com](https://platform.openai.com))
- Ngrok authtoken (from [ngrok.com](https://ngrok.com))
- Google Colab account (for running in Colab)
- For Windows: Command Prompt or PowerShell

## Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/court_order_processor.git
   cd court_order_processor
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Environment Variables**
   - Create a `.env` file or set variables directly:
     ```bash
     export OPENAI_API_KEY="your-openai-api-key"
     export NGROK_AUTH_TOKEN="your-ngrok-authtoken"
     ```
   - On Windows (see below for details), use Command Prompt or PowerShell to set variables.

## Running Locally (Linux/MacOS)
1. **Start the FastAPI App**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Expose with Ngrok**
   In a separate terminal:
   ```bash
   ngrok http 8000
   ```
   Copy the public URL (e.g., `https://<random>.ngrok.io`).

3. **Access the App**
   Open the ngrok URL in a browser to upload PDFs.

## Running on Windows
1. **Install Python**
   - Download and install Python 3.11+ from [python.org](https://www.python.org/downloads/windows/).
   - During installation, check "Add Python to PATH" to enable `python` and `pip` commands.
   - Verify installation in Command Prompt:
     ```cmd
     python --version
     pip --version
     ```

2. **Install Git**
   - Download and install Git for Windows from [git-scm.com](https://git-scm.com/download/win).
   - Verify installation:
     ```cmd
     git --version
     ```

3. **Clone the Repository**
   - Open Command Prompt or PowerShell.
   - Clone the repository:
     ```cmd
     git clone https://github.com/your-username/court_order_processor.git
     cd court_order_processor
     ```

4. **Create a Virtual Environment**
   - Create and activate a virtual environment to isolate dependencies:
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - In PowerShell, use:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - Verify the virtual environment is active (prompt shows `(venv)`).

5. **Install Dependencies**
   - With the virtual environment activated, install dependencies:
     ```cmd
     pip install -r requirements.txt
     ```

6. **Set Environment Variables**
   - Set `OPENAI_API_KEY` and `NGROK_AUTH_TOKEN` in Command Prompt:
     ```cmd
     set OPENAI_API_KEY=your-openai-api-key
     set NGROK_AUTH_TOKEN=your-ngrok-authtoken
     ```
   - In PowerShell:
     ```powershell
     $env:OPENAI_API_KEY="your-openai-api-key"
     $env:NGROK_AUTH_TOKEN="your-ngrok-authtoken"
     ```
   - Alternatively, create a `.env` file in the project root with:
     ```
     OPENAI_API_KEY=your-openai-api-key
     NGROK_AUTH_TOKEN=your-ngrok-authtoken
     ```
     Load it using a library like `python-dotenv` (not required for this project unless modified).

7. **Start the FastAPI App**
   - With the virtual environment activated, run:
     ```cmd
     uvicorn app:app --host 0.0.0.0 --port 8000 --reload
     ```

8. **Expose with Ngrok**
   - Download ngrok from [ngrok.com](https://ngrok.com) and extract `ngrok.exe`.
   - In a new Command Prompt, navigate to the ngrok directory and run:
     ```cmd
     ngrok http 8000
     ```
   - In PowerShell:
     ```powershell
     .\ngrok http 8000
     ```
   - Copy the public URL (e.g., `https://<random>.ngrok.io`).

9. **Access the App**
   - Open the ngrok URL in a browser to upload PDFs.

## Running in Google Colab
1. **Upload Files**
   - Upload the entire project folder to `/content/court_order_processor` in Colab.

2. **Run the Colab Script**
   - Open `run_colab.py` in a Colab notebook and execute it.
   - Provide `OPENAI_API_KEY` and `NGROK_AUTH_TOKEN` via Colab Secrets or manual input when prompted.

3. **Access the App**
   - Use the ngrok public URL displayed in the output.

## Testing
1. **Create Sample PDFs**
   In a Colab cell or locally with Python:
   ```python
   from reportlab.lib.pagesizes import letter
   from reportlab.pdfgen import canvas

   # Sample 1.pdf
   c = canvas.Canvas("Sample 1.pdf", pagesize=letter)
   c.drawString(100, 750, "National ID: 9876543210")
   c.drawString(100, 730, "Action: freeze_account")
   c.save()

   # Sample 2.pdf
   c = canvas.Canvas("Sample 2.pdf", pagesize=letter)
   c.drawString(100, 750, "National ID number 12345667890")
   c.drawString(100, 730, "Action: release_funds")
   c.save()

   # Sample 3.pdf
   c = canvas.Canvas("Sample 3.pdf", pagesize=letter)
   c.drawString(100, 750, "ID No.112112334445")
   c.drawString(100, 730, "Action: freeze_account")
   c.save()

   # Sample 4.pdf
   c = canvas.Canvas("Sample 4.pdf", pagesize=letter)
   c.drawString(100, 750, "identification number 5544332211")
   c.drawString(100, 730, "Action: suspend_accounts")
   c.save()

   # Sample 5.pdf
   c = canvas.Canvas("Sample 5.pdf", pagesize=letter)
   c.drawString(100, 750, "Amman Economic Court")
   c.save()
   ```

2. **Upload PDFs**
   - Access the ngrok URL in a browser.
   - Upload each PDF via the web interface.

3. **Expected Outputs**
   - Sample 1: `Customer CUST001: Freeze account`
   - Sample 2: `Customer CUST002: Release funds`
   - Sample 3: `Customer CUST003: Freeze account`
   - Sample 4: `Customer CUST004: Suspend accounts`
   - Sample 5: `National ID None not found. Order discarded.`

## Dependencies
See `requirements.txt` for a full list. Key dependencies:
- `fastapi==0.115.0`
- `uvicorn==0.30.6`
- `openai==1.55.3`
- `pymupdf==1.24.10`
- `langgraph==0.2.23`
- `pyngrok==7.2.0`

## Notes
- **OpenAI API Key**: Required for LLM extraction. Without a valid key, the app falls back to regex extraction.
- **Ngrok**: Free accounts may disconnect after a few hours; consider a paid plan for persistence.
- **Colab**: Re-run `run_colab.py` if the session restarts.
- **Windows**: Use Command Prompt or PowerShell for commands. Ensure Python and Git are added to PATH.
- **Logging**: Check logs for `INFO`, `WARNING`, `ERROR` messages to debug issues.

## Troubleshooting
- **API Key Errors**: Verify the key at [platform.openai.com](https://platform.openai.com).
- **JSON Parsing Errors**: Check logs for `Raw content from LLM: ...` to diagnose LLM output.
- **File Issues**: Ensure all files are in `/content/court_order_processor` (Colab) or project root (local).
- **Event Loop Errors**: Ensure `nest-asyncio` is applied in Colab.
- **Windows PATH Issues**: If `python` or `pip` commands fail, re-install Python with "Add to PATH" enabled or manually add Python to the system PATH.

## License
MIT License