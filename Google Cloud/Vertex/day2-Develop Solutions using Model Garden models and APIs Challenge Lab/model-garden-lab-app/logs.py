from google.cloud import logging as cloud_logging

# Initialize Google Cloud Logging
cloud_logging_client = cloud_logging.Client()
cloud_logging_client.setup_logging()
logger = cloud_logging_client.logger(
    "model-garden-api-playground-activity")  # Custom log name

def write_log_entry(model, prompt, chunk):
    """Writes a log message to Google Cloud Logging."""
    structured_log = {
        "model": model,
        "prompt": prompt[:100],
        "chunk": chunk
    }
    logger.log_struct(structured_log)
