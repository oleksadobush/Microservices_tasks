from time import sleep

import hazelcast

client = hazelcast.HazelcastClient()
distributed_map = client.get_map("my-distributed-map").blocking()

key = "1"

for i in range(1000):
    value = distributed_map.get(key)
    sleep(0.001)
    value += 1
    distributed_map.put(key, value)
