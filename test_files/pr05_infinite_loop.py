def find_item(items, target):
    i = 0
    while True:
        if items[i] == target:
            return i
        i += 1