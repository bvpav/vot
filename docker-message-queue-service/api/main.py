import os
import flask

from db import db, Video

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

db.init_app(app)


@app.get('/videos')
def list_videos():
    videos = db.session.execute(db.select(Video)).scalars()
    return [video.to_json() for video in videos]


@app.post('/videos')
def create_video():
    video = Video(
        title=flask.request.json['title'],
        url=flask.request.json['url'],
        description=flask.request.json['description'],
    )
    db.session.add(video)
    db.session.commit()
    return video.to_json()


@app.get('/videos/<int:video_id>')
def get_video(video_id):
    video = db.session.execute(db.select(Video).where(Video.id == video_id)).scalar()
    if video is None:
        return {'error': 'Video not found'}, 404
    return video.to_json()


def main():
    # while True:
    #     pass
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()