import json
import uuid

import pika

amqp_conn = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq',
        credentials=pika.PlainCredentials('guest', 'guest')
    )
)


class RPCProcedure:
    def __init__(self, connection, routing_key, serialize, deserialize):
        self.connection = connection
        self.channel = connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.routing_key = routing_key
        self.serialize = serialize
        self.deserialize = deserialize

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.correlation_id = None
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = self.deserialize(body)

    def __call__(self, **kwargs):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.correlation_id,
            ),
            body=self.serialize(kwargs),
        )
        self.connection.process_data_events(time_limit=None)
        return self.response


create_video = RPCProcedure(amqp_conn, 'videos.create_video', serialize=json.dumps, deserialize=json.loads)
update_video = RPCProcedure(amqp_conn, 'videos.update_video', serialize=json.dumps, deserialize=json.loads)
get_video = RPCProcedure(amqp_conn, 'videos.get_video', serialize=json.dumps, deserialize=json.loads)
list_videos = RPCProcedure(amqp_conn, 'videos.list_videos', serialize=json.dumps, deserialize=json.loads)
