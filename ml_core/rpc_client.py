
import pika
import uuid
import pickle
class MLRpcClient(object):

    def __init__(self):
        credentials = pika.PlainCredentials('test', 'test')
        parameters = pika.ConnectionParameters('172.31.85.15',
                                               5672,
                                               '/',
                                               credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call_svm(self, dataset, target, test):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_svm',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(dataset+" "+target+" "+str(test)))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def call_xgboost(self, dataset, target, test):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_xgboost',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(dataset+" "+target+" "+str(test)))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def call_linear(self, dataset, target, test):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_linear',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(dataset+" "+target+" "+str(test)))
        while self.response is None:
            self.connection.process_data_events()
        return self.response

    def call_logistic(self, dataset, target, test):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue_logistic',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(dataset+" "+target+" "+str(test)))
        while self.response is None:
            self.connection.process_data_events()
        return self.response
