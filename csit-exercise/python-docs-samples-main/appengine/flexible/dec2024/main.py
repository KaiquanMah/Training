# # Copyright 2015 Google LLC
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #     http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.

# # [START gae_flex_quickstart]
# from flask import Flask


# app = Flask(__name__)


# @app.route("/")
# def hello() -> str:
#     """Return a friendly HTTP greeting.

#     Returns:
#         A string with the words 'Hello World!'.
#     """
#     return "Hello World!"




from flask import Flask, request, jsonify
import requests  # Used to make HTTP requests to external services

app = Flask(__name__)

# Gatekeeper Service endpoint
GATEKEEPER_URL = "https://dec-2024-mini-challenge.csit-events.sg/api/gatekeeper/access"

# Toy Production Service URL (replace with actual URL if known)
TOY_PRODUCTION_URL = "http://toy-production-service.local/api/toyProductionKey"

# Replace with your Compute Engine external IP and port
ORDER_SERVICE_IP = "34.145.30.44:8080"  # Update with your public IP and port


@app.route("/api/toyProductionKey", methods=["POST"])
def order_service():
    """
    Endpoint to retrieve the toy production key.
    """
    try:
        # Step 1: Send a request to Gatekeeper Service
        gatekeeper_payload = {
            "orderServiceHostOrIpAddress": ORDER_SERVICE_IP,
            "secretInput": "secret_value"  # Replace 'secret_value' with actual secret
        }
        gatekeeper_response = requests.post(GATEKEEPER_URL, json=gatekeeper_payload)

        # Check if Gatekeeper response is successful
        if gatekeeper_response.status_code != 200:
            return (
                jsonify({"error": "Failed to authenticate with Gatekeeper Service"}),
                502,
            )

        # Step 2: Extract the secret input
        gatekeeper_data = gatekeeper_response.json()
        secret_input = gatekeeper_data.get("secretInput")
        if not secret_input:
            return jsonify({"error": "Invalid Gatekeeper response"}), 502

        # Step 3: Forward the secretInput to Toy Production Service
        toy_production_payload = {"toyProductionKey": secret_input}
        toy_production_response = requests.post(
            TOY_PRODUCTION_URL, json=toy_production_payload
        )

        # Check if Toy Production Service response is successful
        if toy_production_response.status_code != 200:
            return (
                jsonify({"error": "Toy Production Service request failed"}),
                502,
            )

        # Step 4: Return the response from Toy Production Service
        return jsonify(
            {"message": "Toy Production Key retrieved!", "data": toy_production_response.json()}
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def hello():
    """
    Health check endpoint.
    """
    return "Hello World!"
    

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]
