import threading

counter = 0

def increment():
    global counter
    temp = counter
    temp += 1
    counter = temp

threads = [threading.Thread(target=increment) for _ in range(100)]
for t in threads:
    t.start()