import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    for i in range(1, 1001):
        while True:
            if queue.offer("value-" + str(i)).result():
                print("write ", i)
                break
    for i in range(2):
        while True:
            if queue.offer(-1).result():
                break
