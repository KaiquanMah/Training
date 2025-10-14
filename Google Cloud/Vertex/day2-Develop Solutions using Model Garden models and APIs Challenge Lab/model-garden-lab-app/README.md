# Model Garden API Playground

This repo contains code to be used in labs where students complete a simple
application that uses two partner APIs to return LLM responses.

## Setup and run application
To set up and run the application:

1. Make sure you have a **Vertex AI Workbench** instance created
2. Click on **Open JupyterLab**
3. Click on Terminal
4. Set up the application with the following commands
   ```bash
   cd ~
   git clone https://github.com/jwd-cloud/model-garden-lab-app.git
   cd model-garden-lab-app
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   export GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project)
   export GOOGLE_CLOUD_REGION="us-central1"
   export GOOGLE_CLOUD_CLAUDE_REGION="us-east5"
      gcloud compute firewall-rules create allow-port-8088 \
    --allow tcp:8088 \
    --source-ranges=0.0.0.0/0 \
    --description="Allow TCP 8088 to this machine from any source"
   streamlit run mg_apis.py
   ```
5. Click on the **External URL** link to open the application

## Make changes to the application

1. In the JupyterLab file browser UI, navigate to the file you want to edit and double-click.
2. Any changes you make should be immediately reflected in the live application
3. Errors will be displayed in the Web UI, and a stack trace will be displayed in the terminal pane.