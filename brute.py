from Queue import PriorityQueue
from collections import namedtuple
from concurrent import futures
from threading import Thread,Event
import os


def create_zip(fn, data):
    with open(fn, 'wb') as f:
        f.write(data)


def extraction_success(output):
    '''checks the output of the 7z command'''
    # This function may differ. Realisation depends on current version of 7z. This simple check works for me
    return 'Everything is Ok' in output


def get_stream(filename, password):
    '''launches 7z command in the background and returns output stream'''
    stream = os.popen("7z e {} -p{} -y".format(filename, password))
    return stream, password

def brutte(filename, passwords, frame_size):
    '''non thread version of brutte force'''
    # 1 - fill array with first N streams
    streams = [get_stream(filename, i) for i in passwords[0:frame_size]]
    # 2 - for every password more than N append it to array, and check and delete first element
    for password in passwords[frame_size:]:
        first_stream = streams[0][0]
        first_password = streams[0][1]
        if extraction_success(first_stream.read().encode()):
                return first_password
        first_stream.close()
        del streams[0]
        streams.append(get_stream(filename, password))
    # 3 - check the last elements in array
    for stream, password in streams:
            if extraction_success(stream.read().encode()):
                return password
            stream.close()
    return None


class BruteResult:
    '''Composition class with threading.Event class'''
    def __init__(self):
        self.event = Event()
        self._password = None

    @property
    def password(self):
        self.event.wait()
        return self._password

    def set_password(self, password):
        self._password = password
        self.event.set()



class BruteItem:
    def __init__(self, peer, archive, passwords, priority):
        self.peer = peer
        self.archive = archive
        self.passwords = passwords
        self.priority = priority
        self.brute_result = BruteResult()

    def __lt__(self, obj):
        return self.priority < obj.priority

    def __le__(self, obj):
        return self.priority <= obj.priority


def work(queue):
    '''thread function'''
    while True:
        task = queue.get(block = True)
        filename = "{}.zip".format(task.peer.replace(':',''))
        create_zip(filename, bytes(task.archive))
        found_password = brutte(filename, [i.strip() for i in task.passwords.split("\n")], 10)
        task.brute_result.set_password(found_password)
        os.remove(filename)



class BruteArchive():
    """Singleton class for bruteforce"""
    def __init__(self, workers):
        self._workers = workers
        self._queue = PriorityQueue()
        self._threads = [Thread(target = work, args = (self._queue,)) for i in range(workers)]
        for thread in self._threads:
            thread.start()

    def brute(self, peer, archive, passwords, priority):     
        task = BruteItem(peer, archive, passwords, priority)
        self._queue.put(task)
        return task.brute_result





