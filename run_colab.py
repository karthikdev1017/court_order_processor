

# Apply nest_asyncio for Colab's event loop
import nest_asyncio
nest_asyncio.apply()

# Import required libraries
from pyngrok import conf, ngrok
import uvicorn
import os
from google.colab import userdata
import openai
import asyncio

# Log OpenAI version
print(f"OpenAI version: {openai.__version__}")

# Set up OpenAI API key
try:
    openai_key = userdata.get('OPENAI_API_KEY')
    if not openai_key:
        raise ValueError("OPENAI_API_KEY not found in Colab Secrets")
    os.environ["OPENAI_API_KEY"] = openai_key
except:
    openai_key = input("Enter your OpenAI API key: ")
    if not openai_key:
        raise ValueError("OpenAI API key is required")
    os.environ["OPENAI_API_KEY"] = openai_key

# Test OpenAI API key
try:
    test_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = test_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Return {'test': 'success'} in JSON format"}],
        temperature=0.0
    )
    print(f"OpenAI test response: {response.choices[0].message.content}")
except Exception as e:
    print(f"OpenAI test failed: {str(e)}")
    print("Continuing with regex extraction as fallback.")

# Verify directory structure
base_dir = "/content/agentic_ai_court_order_processor"
required_files = [
    "app.py",
    "customer_db.py",
    "actions.py",
    "utils.py",
    "llm_extractor.py",
    "langgraph_agent.py",
    "data/customers.csv",
    "data/actions.csv",
    "templates/index.html",
    "static/styles.css"
]
missing_files = [f for f in required_files if not os.path.exists(os.path.join(base_dir, f))]
if missing_files:
    print(f"Error: Missing files: {missing_files}")
    raise FileNotFoundError(f"Missing required files: {missing_files}")
else:
    print("All required files found.")

# Log contents of data files
print("Contents of customers.csv:")
!cat {base_dir}/data/customers.csv
print("\nContents of actions.csv:")
!cat {base_dir}/data/actions.csv

# Set up ngrok authtoken
try:
    ngrok_token = userdata.get('NGROK_AUTH_TOKEN')
except:
    ngrok_token = input("Enter your ngrok authtoken: ")
conf.get_default().auth_token = ngrok_token

# Expose FastAPI app via ngrok
try:
    public_url = ngrok.connect(8000)
    print(f"🚀 Public URL: {public_url}")
except Exception as e:
    print(f"Error starting ngrok: {str(e)}")
    raise

# Change to project directory
os.chdir(base_dir)

# Run FastAPI app asynchronously
async def run_server():
    config = uvicorn.Config("app:app", host="0.0.0.0", port=8000, reload=True)
    server = uvicorn.Server(config)
    await server.serve()

# Execute the async function in Colab's event loop
await run_server()