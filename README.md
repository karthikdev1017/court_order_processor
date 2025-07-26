## Prerequisites
- Python 3.11+
- Git
- OpenAI API key (from [platform.openai.com](https://platform.openai.com))
- Ngrok authtoken (from [ngrok.com](https://ngrok.com))
- Google Colab account (for running in Colab)

## Setup
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/agentic_ai_court_order_processor.git
   cd agentic_ai_court_order_processor
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

## Running Locally
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

## Running in Google Colab
1. **Upload Files**
   - Upload the entire project folder to `/content/agentic_ai_court_order_processor` in Colab.

2. **Run the Colab Script**
   - Open `run_colab.py` in a Colab notebook and execute it.
   - Provide `OPENAI_API_KEY` and `NGROK_AUTH_TOKEN` via Colab Secrets or manual input when prompted.

3. **Access the App**
   - Use the ngrok public URL displayed in the output.
