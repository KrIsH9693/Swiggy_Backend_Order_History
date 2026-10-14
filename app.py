
from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

BASE_URL = "http://127.0.0.1:32567/api/v1/swiggy"


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Order Integration API is running"
    })


def fetch_api_data(url, params=None):
    try:
        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        try:
            body = response.json()
        except ValueError:
            body = response.text

        if not response.ok:
            return {
                "success": False,
                "upstream_status": response.status_code,
                "upstream_error": body
            }, 502

        return {
            "success": True,
            "data": body
        }, 200

    except requests.RequestException as error:
        app.logger.error(
            "Third-party API request failed: %s", error
        )

        return {
            "success": False,
            "error": "Cannot connect to third-party software"
        }, 502


@app.route("/api/orders", methods=["GET"])
def get_orders():
    result, status = fetch_api_data(
        f"{BASE_URL}/orders"
    )
    return jsonify(result), status


@app.route("/api/order-history", methods=["GET"])
def get_order_history():
    restaurant_id = request.args.get("restaurant_id")

    if not restaurant_id:
        return jsonify({
            "success": False,
            "error": "restaurant_id is required",
            "example": (
                "/api/order-history?restaurant_id=515676"
            )
        }), 400

    result, status = fetch_api_data(
        f"{BASE_URL}/orderHistory",
        params={"restaurant_id": restaurant_id}
    )

    return jsonify(result), status


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
