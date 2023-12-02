from dataclasses import asdict

import flask
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from db import db


class Video(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)


videos = flask.Blueprint('videos', __name__)


@videos.get('/')
def list_videos():
    videos = db.session.execute(db.select(Video)).scalars()
    return [asdict(video) for video in videos]


@videos.post('/')
def create_video():
    video = Video(
        id=None,
        title=flask.request.json['title'],
        url=flask.request.json['url'],
        description=flask.request.json['description'],
    )
    db.session.add(video)
    db.session.commit()
    return asdict(video)


@videos.get('/<int:video_id>')
def get_video(video_id):
    video = db.session.execute(db.select(Video).where(Video.id == video_id)).scalar()
    if video is None:
        return {'error': 'Video not found'}, 404
    return asdict(video)
