
import json
import pika
from videos import get_video, list_videos, create_video, update_video
from videos import GetVideo, CreateVideo, UpdateVideo
import psycopg2

amqp_conn = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        credentials=pika.PlainCredentials('guest', 'guest')
    )
)

channel = amqp_conn.channel()

channel.queue_declare(queue='videos.create_video')
channel.queue_declare(queue='videos.update_video')
channel.queue_declare(queue='videos.get_video')
channel.queue_declare(queue='videos.list_videos')


psql_conn = psycopg2.connect(
    host='db',
    dbname='postgres',
    user='postgres',
    password='example'
)


def on_request_list_videos(ch, method, props, body):
    print('list_videos')
    response = list_videos(psql_conn, )
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps('[' + ','.join(video.model_dump_json() for video in response) + ']')
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_get_video(ch, method, props, body):
    print('get_video')
    request = GetVideo.model_validate_json(body)
    response = get_video(psql_conn, request)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response.model_dump_json() if response else 'null'
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_create_video(ch, method, props, body):
    print('create_video')
    request = CreateVideo.model_validate_json(body)
    response = create_video(psql_conn, request)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response.model_dump_json()
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def on_request_update_video(ch, method, props, body):
    print('update_video')
    request = UpdateVideo.model_validate_json(body)
    response = update_video(psql_conn, request)
    ch.basic_publish(
        exchange='',
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=response.model_dump_json() if response else 'nu'
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='videos.list_videos', on_message_callback=on_request_list_videos)
channel.basic_consume(queue='videos.get_video', on_message_callback=on_request_get_video)
channel.basic_consume(queue='videos.create_video', on_message_callback=on_request_create_video)
channel.basic_consume(queue='videos.update_video', on_message_callback=on_request_update_video)

print('Awaiting RPC requests')
channel.start_consuming()