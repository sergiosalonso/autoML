import pika
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle
def get_dataset(dataset):
    return pd.read_csv(dataset)

def basic_preprocessing(df, target, test=0.75):
    y=pd.DataFrame(df[target])
    df=df.drop([target], axis=1).copy()
    features = df.columns
    X = pd.DataFrame(data=StandardScaler().fit_transform(df), columns=features)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=0)
    return X_train, X_test, y_train, y_test

def svm(X_train, X_test, y_train, y_test):
    svm = SVC()
    model=svm.fit(X_train, y_train)
    pickle.dump(model, open("svm.pkl", 'wb'))
    return model.score(X_test, y_test)

def logistic(X_train, X_test, y_train, y_test):
    lr = LogisticRegression(random_state=0).fit(X_train, y_train)
    model=lr.fit(X_train, y_train)
    pickle.dump(model, open("LR.pkl", 'wb'))
    return model.score(X_test, y_test)

def linear(X_train, X_test, y_train, y_test):
    lm = linear_model.LinearRegression()
    model = lm.fit(X_train, y_train)
    #predictions = lm.predict(X_test)
    pickle.dump(model, open("regression.pkl", 'wb'))
    return model.score(X_test, y_test)

def xgboost(X_train, X_test, y_train, y_test):
    xgboost = XGBClassifier()
    model = xgboost.fit(X_train, y_train)
    predictions = model.predict(X_test)
    pickle.dump(model, open("xgboost.pkl", 'wb'))
    return accuracy_score(y_test, predictions)

def on_request1(ch, method, props, body):
    body = str(body).decode('utf-8').split()
    df=get_dataset(body[0])
    print(" [.] svm")
    X_train, X_test, y_train, y_test=basic_preprocessing(df, body[1], body[2])
    response = svm(X_train, X_test, y_train, y_test)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request2(ch, method, props, body):
    body = str(body).decode('utf-8')split()
    df=get_dataset(body[0])
    print(" [.] xgboost")
    X_train, X_test, y_train, y_test = basic_preprocessing(df, body[1], body[2])
    response = xgboost(X_train, X_test, y_train, y_test)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request3(ch, method, props, body):
    body = str(body).decode('utf-8').split()
    df=get_dataset(body[0])
    print(" [.] linear")
    X_train, X_test, y_train, y_test = basic_preprocessing(df, body[1], body[2])
    response = linear(X_train, X_test, y_train, y_test)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request4(ch, method, props, body):
    body = str(body).decode('utf-8').split()
    df=get_dataset(body[0])
    print(" [.] logistic")
    X_train, X_test, y_train, y_test = basic_preprocessing(df, body[1], body[2])
    response = logistic(X_train, X_test, y_train, y_test)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == '__main__':
    print('entra')
    credentials = pika.PlainCredentials('test', 'test')
    parameters = pika.ConnectionParameters('172.31.85.15',
                                           5672,
                                           '/',
                                           credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue_svm')
    channel.queue_declare(queue='rpc_queue_xgboost')
    channel.queue_declare(queue='rpc_queue_linear')
    channel.queue_declare(queue='rpc_queue_logistic')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='rpc_queue_svm', on_message_callback=on_request1)
    channel.basic_consume(queue='rpc_queue_xgboost', on_message_callback=on_request2)
    channel.basic_consume(queue='rpc_queue_linear', on_message_callback=on_request3)
    channel.basic_consume(queue='rpc_queue_logistic', on_message_callback=on_request4)
    print(" [x] Awaiting RPC requests")
    channel.start_consuming()
