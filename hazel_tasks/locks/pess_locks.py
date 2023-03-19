import hazelcast

client = hazelcast.HazelcastClient()
distributed_map = client.get_map("my-distributed-map").blocking()

key = "1"

for i in range(1000):
    distributed_map.lock(key)
    try:
        value = distributed_map.get(key)
        value += 1
        distributed_map.put(key, value)
    finally:
        distributed_map.unlock(key)
