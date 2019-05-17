# Docker images containing data-producer and data-consumer.


FROM ubuntu:latest
MAINTAINER Vcitor Sheng "18510085912@163.com"

RUN apt-get update && apt-get install -y \
                                    python \
                                    python-pip \
                                    wget
COPY ./data_producer.py /
COPY ./data_consumer.py /
COPY ./requirements.txt /
RUN pip install --index https://pypi.mirrors.ustc.edu.cn/simple/ -r requirements.txt
CMD python data_producer.py BTC-USDC test kafka:9092