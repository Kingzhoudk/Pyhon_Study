# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt_client
import json
import time

'''
data = {
    "id":"xxx", [0-999999]
    "type": "xxx", [ / ]
    "timestamp": "xxx", [1234567890]s
    "data": "xxx", [[**:**],[]]
}
'''


class MqttClient(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.running = False
        # 初始化mqtt client,订阅topic，开启loop
        self.client = mqtt_client.Client()
        self.client.username_pw_set("compass", "compass")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_disconnect = self.on_disconnect
        self.client.connect_async(self.host, self.port, 10)

    # 开启异歩循环
    def start(self):
        self.client.loop_start()

    def stop(self):
        self.running = False
        self.client.loop_stop()

    # 开启订阅
    def subscribe(self, topic):
        self.client.subscribe(topic)

    # 发送消息
    def publish(self, topic, msg):
        self.client.publish(topic, payload=msg, qos=0)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.running = True
            print("connected succed")
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print("On Subscribed: qos = %d" % granted_qos)

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected disconnection %s" % rc)


test = MqttClient("127.0.0.1", 1883)
test.start()
time.sleep(1)
test.subscribe("#")

while True:
    test.publish("python/test","test")
    time.sleep(1)
