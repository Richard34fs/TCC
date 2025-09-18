import heapq

class SeedQueue:
    def __init__(self):
        self.queue = []  # heap: (priority, seed_filename)

    def push(self, seed_filename, priority):
        heapq.heappush(self.queue, (priority, seed_filename))

    def pop(self):
        if self.queue:
            return heapq.heappop(self.queue)
        return None, None

    def is_empty(self):
        return len(self.queue) == 0
