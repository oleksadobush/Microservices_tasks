import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()

    my_map = client.get_map("my-distributed-map").blocking()
    for i in range(1000):
        my_map.put("key" + str(i), "value" + str(i))
