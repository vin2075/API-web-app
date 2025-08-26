from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class SearchResult(db.Model):
    __tablename__ = "search_results"

    id = db.Column(db.Integer, primary_key=True)
    provider = db.Column(db.String(50), nullable=False)  # github | openweather
    search_term = db.Column(db.String(255), nullable=False)
    page = db.Column(db.Integer, nullable=True)
    per_page = db.Column(db.Integer, nullable=True)
    result_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "provider": self.provider,
            "search_term": self.search_term,
            "page": self.page,
            "per_page": self.per_page,
            "result": json.loads(self.result_json),
            "created_at": self.created_at.isoformat(),
        }
