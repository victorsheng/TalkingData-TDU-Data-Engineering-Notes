docker run -d -p 2181:2181 -p 2888:2888 -p 3888:3999 --net network-spark --name zookeeper-vic zookeeper
# https://hub.docker.com/_/zookeeper