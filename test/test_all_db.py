import os

import pytest

from app import app
from chroma_db import collection
from database import db
from business.models import User


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client


def test_user_data(client):
    with app.app_context():
        # insert user data
        c = User()
        c.username = 'xxx@qq.com'
        c.password = 'xxx'
        db.session.add(c)
        db.session.commit()


def test_chroma(client):
    with app.app_context():
        print(os.environ.get('OPENAI_API_KEY'))
        collection.add(
            metadatas=[
                {"id": 0, "word": "race", "trans": "种族"},
                {"id": 1, "word": "ethnic", "trans": "种族的"},
                {"id": 2, "word": "hardly", "trans": "困难的"},
                {"id": 3, "word": "assess", "trans": "评价，评定；估价，估计"},
                {"id": 4, "word": "defend", "trans": "保护、防守"},
                {"id": 5, "word": "protect", "trans": "保护、防卫"},
                {"id": 6, "word": "preserve", "trans": "保护"},
            ],
            documents=["race n.种族、人种",
                       "ethnic adj.种族的、人种的",
                       "hardly adj.困难的",
                       "assess n.国土、领土",
                       "defend vt.保护、防守",
                       "protect vt.保护、防卫",
                       "preserve vt.保护"],
            ids=["id1", "id2", "id3", "id4", "id5", "id6", "id7"]
        )
        results = collection.query(
            query_texts=["防护"],
            n_results=3,
            include=["metadatas"]
        )
        print(results)
