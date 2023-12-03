import os

import flask

import rpc


app = flask.Flask(__name__)


@app.get('/videos')
def list_videos():
    return rpc.list_videos()


@app.post('/videos')
def create_video():
    return rpc.create_video(
        url=flask.request.json['url'],
    )


@app.get('/videos/<int:video_id>')
def get_video(video_id):
    video = rpc.get_video(id=video_id)
    if video is None:
        return {'error': 'Video not found'}, 404
    return video
