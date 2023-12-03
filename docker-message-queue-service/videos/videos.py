from datetime import datetime
from typing import Optional
import pydantic
import psycopg2
from psycopg2.extras import DictCursor


class Video(pydantic.BaseModel):
    id: pydantic.PositiveInt
    title: Optional[str]
    description: Optional[str]
    url: str
    file_url: Optional[str]
    created_at: datetime


class CreateVideo(pydantic.BaseModel):
    url: str


class UpdateVideo(pydantic.BaseModel):
    id: pydantic.PositiveInt
    title: Optional[str]
    description: Optional[str]
    url: Optional[str]
    file_url: Optional[str]


class GetVideo(pydantic.BaseModel):
    id: pydantic.PositiveInt


def list_videos(conn: psycopg2.extensions.connection) -> list[Video]:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('select * from videos;')
        return [Video(**video) for video in cursor.fetchall()]


def get_video(conn: psycopg2.extensions.connection, get_video_request: GetVideo) -> Optional[Video]:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('select * from videos where id = %s;', (get_video_request.id,))
        video = cursor.fetchone()
        if video is None:
            return None
        return Video(**video)
    

def create_video(conn: psycopg2.extensions.connection, video: CreateVideo) -> Video:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        cursor.execute('insert into videos (url) values (%s) returning *;', (video.url,))
        conn.commit()
        return Video(**cursor.fetchone())
    

def update_video(conn: psycopg2.extensions.connection, video: UpdateVideo) -> Optional[Video]:
    with conn.cursor(cursor_factory=DictCursor) as cursor:
        query = 'update videos set '
        params = []
        if video.title is not None:
            query += 'title = %s, '
            params.append(video.title)
        if video.description is not None:
            query += 'description = %s, '
            params.append(video.description)
        if video.url is not None:
            query += 'url = %s, '
            params.append(video.url)
        if video.file_url is not None:
            query += 'file_url = %s, '
            params.append(video.file_url)
        if len(params) != 0:
            query = query.rstrip(', ') + ' where id = %s returning *;'
            params.append(video.id)
            cursor.execute(query, tuple(params))
            video = cursor.fetchone()
            conn.commit()
            if video is None:
                return None
            return Video(**video)
        else:
            return get_video(conn, GetVideo(id=video.id))