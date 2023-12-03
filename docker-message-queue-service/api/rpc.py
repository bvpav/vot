import json
import uuid

import pika

params = pika.ConnectionParameters(
    host='rabbitmq',
    credentials=pika.PlainCredentials('guest', 'guest')
)


class RPCProcedure:
    def __init__(self, connection_parameters, routing_key, serialize, deserialize):
        self.connection_parameters = connection_parameters
        self.connection = None
        self.channel = None
        self.callback_queue = None

        self.routing_key = routing_key
        self.serialize = serialize
        self.deserialize = deserialize

        self.correlation_id = None
        self.response = None

    def connect(self):
        self.connection = pika.BlockingConnection(self.connection_parameters)
        self.channel = self.connection.channel()
        self.callback_queue = self.channel.queue_declare(queue='', exclusive=True).method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def disconnect(self):
        self.connection.close()
        self.connection = None
        self.channel = None
        self.callback_queue = None

    def on_response(self, ch, method, props, body):
        if self.correlation_id == props.correlation_id:
            self.response = self.deserialize(body)

    def __call__(self, **kwargs):
        self.connect()
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
        self.disconnect()
        return self.response


create_video = RPCProcedure(params, 'videos.create_video', serialize=json.dumps, deserialize=json.loads)
update_video = RPCProcedure(params, 'videos.update_video', serialize=json.dumps, deserialize=json.loads)
get_video = RPCProcedure(params, 'videos.get_video', serialize=json.dumps, deserialize=json.loads)
list_videos = RPCProcedure(params, 'videos.list_videos', serialize=json.dumps, deserialize=json.loads)
