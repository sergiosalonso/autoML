import pika

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)
def suma(n):
    return n+n

def on_request1(ch, method, props, body):
    n = int(body)

    print(" [.] fib(%s)" % n)
    response = fib(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request2(ch, method, props, body):
    n = int(body)

    print(" [.] suma(%s)" % n)
    response = suma(n)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    print('ente')
    credentials = pika.PlainCredentials('test', 'test')
    parameters = pika.ConnectionParameters('172.31.85.15',
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue')
    channel.queue_declare(queue='rpc_queue_suma')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)
    channel.basic_consume(queue='rpc_queue_suma', on_message_callback=on_request2)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
