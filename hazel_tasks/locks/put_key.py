import hazelcast

client = hazelcast.HazelcastClient()
distributed_map = client.get_map("my-distributed-map").blocking()

key = "1"
distributed_map.put(key, 0)