from time import sleep

import hazelcast

client = hazelcast.HazelcastClient()
distributed_map = client.get_map("my-distributed-map").blocking()

key = "1"

for i in range(1000):
    while True:
        old_value = distributed_map.get(key)
        new_value = old_value
        sleep(0.001)
        new_value += 1
        if distributed_map.replace_if_same(key, old_value, new_value):
            break

