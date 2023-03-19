import hazelcast

if __name__ == "__main__":
    client = hazelcast.HazelcastClient()
    queue = client.get_queue("queue")
    i = 0
    while True:
        m = queue.take().result()
        i += 1
        if m == -1:
            break
        print("reader1 takes ", i)
