import pika
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import xgboost as xgb
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error
import pickle

def basic_preprocessing(df, target, test=0.75, categorical=[]):
    if categorical:
        df = pd.get_dummies(df, columns=[categorical])
        df = df.dropna(how='all', axis='columns').copy()
    y = pd.DataFrame(df[target])
    df = df.drop([target], axis=1).copy()
    features = df.columns
    X = pd.DataFrame(data=StandardScaler().fit_transform(df), columns=features)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=0)
    return X_train, X_test, y_train, y_test

def svm(X_train, X_test, y_train, y_test):
    svm = SVC()
    model=svm.fit(X_train, y_train)
    predictions = model.predict(X_test)
    #mse=mean_squared_error(y_test, predictions)
    name="svm"
    return pickle.dumps({"model":model,"name":name})

def logistic(X_train, X_test, y_train, y_test):
    lr = LogisticRegression(random_state=0).fit(X_train, y_train)
    model=lr.fit(X_train, y_train)
    #score=model.score(X_test, y_test)
    name="logistic"
    return pickle.dumps({"model":model,"name":name})

def linear(X_train, X_test, y_train, y_test):
    lm = LinearRegression()
    model = lm.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse=mean_squared_error(y_test, predictions)
    name="linear"
    return pickle.dumps({"model":model,"mse":mse, "name":name})

def xgboost_regressor(X_train, X_test, y_train, y_test):
    xgboost = xgb.XGBRegressor(objective ='reg:squarederror', colsample_bytree = 0.3, learning_rate = 0.1,max_depth = 5, alpha = 10, n_estimators = 10)
    model = xgboost.fit(X_train, y_train)
    predictions = model.predict(X_test)
    mse=mean_squared_error(y_test, predictions)

    name="xgboost"
    return pickle.dumps({"model":model,"mse":mse, "name":name})

def on_request1(ch, method, props, body):
    try:
        body = pickle.loads(body)
        df=body['dataset']
        print(" [.] svm")
        X_train, X_test, y_train, y_test=basic_preprocessing(df, body['target'], body['test']*0.01, body['categorical'])
        response = svm(X_train, X_test, y_train, y_test)
    except:
        response = pickle.dumps({"model":-1})
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request2(ch, method, props, body):
    try:
        body = pickle.loads(body)
        df=body['dataset']
        print(" [.] xgboost")
        X_train, X_test, y_train, y_test = basic_preprocessing(df, body['target'], body['test']*0.01, body['categorical'])
        response = xgboost_regressor(X_train, X_test, y_train, y_test)
    except:
        response = pickle.dumps({"model":-1})
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request3(ch, method, props, body):
    try:
        body = pickle.loads(body)
        df=body['dataset']
        print(" [.] linear")
        X_train, X_test, y_train, y_test = basic_preprocessing(df, body['target'], body['test']*0.01, body['categorical'])
        response = linear(X_train, X_test, y_train, y_test)
    except:
        response = pickle.dumps({"model":-1})
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def on_request4(ch, method, props, body):
    try:
        body = pickle.loads(body)
        df=body['dataset']
        print(" [.] logistic")
        X_train, X_test, y_train, y_test = basic_preprocessing(df, body['target'], body['test']*0.01, body['categorical'])
        response = logistic(X_train, X_test, y_train, y_test)
    except:
        response = pickle.dumps({"model":-1})
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=response)
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
