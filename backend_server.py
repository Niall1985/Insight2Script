from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import json

from query_processor.query_agent import query_processing_agent
from content_main import combined
from analytics_main import get_trend_data

app = Flask(__name__)
CORS(app)


@app.route("/api/generate", methods=["POST"])
def generate_content():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "").strip()

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

       
        formatted_prompt = query_processing_agent(prompt)


        trend_data = get_trend_data(formatted_prompt)
        print(trend_data)
  
        if isinstance(trend_data, str):
            try:
                trend_data = json.loads(trend_data)
            except Exception as e:
                print("Error parsing trend_data:", e)
                trend_data = None

        if not isinstance(trend_data, list) or len(trend_data) < 10:
            return jsonify({"error": "Invalid trend data format"}), 500
        (
            score,
            score_2018,
            score_2019,
            score_2020,
            score_2021,
            score_2022,
            score_2023,
            score_2024,
            score_2025,
            reasoning
        ) = trend_data

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(combined(formatted_prompt))

        return jsonify({
            "trend_data": {
                "score": score,
                "score_2018": score_2018,
                "score_2019": score_2019,
                "score_2020": score_2020,
                "score_2021": score_2021,
                "score_2022": score_2022,
                "score_2023": score_2023,
                "score_2024": score_2024,
                "score_2025": score_2025,
                "reasoning": reasoning,
            },
            "content": str(result)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
