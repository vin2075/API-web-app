import os
import json
import requests
from flask import Flask, request, jsonify, current_app
from flask_migrate import Migrate
from flask_cors import CORS       # <-- import CORS here
from config import Config
from models import db, SearchResult

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app)                        # <-- enable CORS here

# init db + migrations
db.init_app(app)
migrate = Migrate(app, db)

# ---------- Helpers ----------
def fetch_github_repos(query, page=1, per_page=10):
    """Fetch repos from GitHub API"""
    url = "https://api.github.com/search/repositories"
    headers = {}
    token = current_app.config.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    params = {"q": query, "page": page, "per_page": per_page}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {"meta": {"total_count": data.get("total_count")}, "items": data.get("items", [])}


def fetch_openweather(query):
    """Fetch weather info by city name"""
    api_key = current_app.config.get("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OpenWeather API key not configured (OPENWEATHER_API_KEY)")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": query, "appid": api_key, "units": "metric"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    return {"meta": {}, "items": [data]}

# ---------- API Endpoints ----------
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "app": "api-driven-mini-app-backend"}), 200

@app.route("/api/search", methods=["POST"])
def search_and_store():
    payload = request.get_json(force=True, silent=True) or {}
    provider = payload.get("provider")
    query = payload.get("query")
    page = int(payload.get("page") or 1)
    per_page = int(payload.get("per_page") or current_app.config.get("DEFAULT_PER_PAGE", 10))

    if not provider or not query:
        return jsonify({"error": "provider and query are required"}), 400
    if provider not in ["github", "openweather"]:
        return jsonify({"error": f"unknown provider '{provider}'"}), 400

    try:
        if provider == "github":
            result = fetch_github_repos(query, page=page, per_page=per_page)
        else:
            result = fetch_openweather(query)
    except requests.HTTPError as he:
        try:
            msg = he.response.json()
        except Exception:
            msg = str(he)
        return jsonify({"error": "upstream_api_error", "details": msg}), 502
    except Exception as e:
        return jsonify({"error": "failed_fetch", "details": str(e)}), 500

    try:
        rec = SearchResult(
            provider=provider,
            search_term=query,
            page=page,
            per_page=per_page,
            result_json=json.dumps(result),
        )
        db.session.add(rec)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "db_error", "details": str(e)}), 500

    return jsonify({
        "status": "saved",
        "id": rec.id,
        "summary": {
            "provider": provider,
            "query": query,
            "items_stored": len(result.get("items", []))
        }
    }), 201

@app.route("/api/results", methods=["GET"])
def list_results():
    provider = request.args.get("provider")
    query = request.args.get("query")
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except:
        page = 1
    try:
        per_page = max(int(request.args.get("per_page", current_app.config.get("DEFAULT_PER_PAGE", 10))), 1)
    except:
        per_page = current_app.config.get("DEFAULT_PER_PAGE", 10)

    q = SearchResult.query
    if provider:
        q = q.filter_by(provider=provider)
    if query:
        q = q.filter(SearchResult.search_term.ilike(f"%{query}%"))

    total = q.count()
    items = q.order_by(SearchResult.created_at.desc()) \
             .offset((page - 1) * per_page) \
             .limit(per_page) \
             .all()

    return jsonify({
        "meta": {"total": total, "page": page, "per_page": per_page},
        "results": [it.to_dict() for it in items]
    }), 200

@app.route("/api/results/<int:rid>", methods=["GET"])
def get_result(rid):
    rec = SearchResult.query.get(rid)
    if not rec:
        return jsonify({"error": "not_found"}), 404
    return jsonify(rec.to_dict()), 200

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "Welcome to API Driven Mini Web App Backend",
        "status": "running",
        "endpoints": ["/api/health", "/api/search", "/api/results"]
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
