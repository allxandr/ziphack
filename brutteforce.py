#----THIS FILE IS USED FOR TESTS ONLY---------
import os 
import Queue
from threading import Thread
import time


def extraction_success(output):
    '''checks the output of the 7z command'''
    # This function may differ. Realisation depends on current version of 7z. This simple check works for me
    return 'Everything is Ok' in output

def valid_password(filename, password):
    '''runs 7z command, waits for output and checks results'''
    stream = os.popen("7z e {} -p{} -y".format(filename, password))
    output = stream.read()
    #print(output)
    stream.close()
    return extraction_success(output.encode())


def worker(filename, queue, found):
    '''worker for a thread. queue - passwords queue, found - correct answers'''
    while not queue.empty() and found.empty():
        password = queue.get()
        #print password
        if valid_password(filename, password):
            found.put(password)
            return

def get_stream(filename, password):
    '''launches 7z command in the background and returns output stream'''
    stream = os.popen("7z e {} -p{} -y".format(filename, password))
    return stream, password

def brutte(filename, passwords, workers_count):
    '''non thread version of brutte force'''
    # 1 - fill array with first N streams
    streams = [get_stream(filename, i) for i in passwords[0:workers_count]]
    # 2 - for every password more than N append it to array, and check and delete first element
    for password in passwords[workers_count:]:
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


def brutte2(filename, passwords, workers_count):
    '''non thread version of brutte force number 2 (works slower)'''
    for epoch in range(len(passwords)//workers_count+1):
        epoch_slice = slice(epoch*workers_count, (epoch+1)*workers_count)
        streams = [get_stream(filename, i) 
                        for i in passwords[epoch_slice]]
        for stream, password in streams:
            if extraction_success(stream.read().encode()):
                return password
    return "not found"


def brutte_thread(filename, passwords, workers_count, priority):
    '''thread based version of brutte force'''
    queue = Queue() # - queue for saving passwords
    found = Queue() # - queue for saving valid passwords
    for i in passwords:
        queue.put(i)
    threads = [Thread(target=worker, 
                        args = [filename, queue, found]) 
                        for i in range(workers_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if found.empty():
        return None
    else:
        return found.get()

if __name__ == '__main__':
    passwords = ["123", "q33q3", "eesasa", "00sdosd","0ekskdskdkssd"]*20+['qwerty']
    t = time.time()
    print brutte("secretinfo.zip", passwords, 10 )
    print "time for first brutteforce", time.time()-t

    t = time.time()
    print brutte2("secretinfo.zip",passwords, 10)
    print "time for second brutte force", time.time()-t

    t = time.time()
    print brutte_thread("secretinfo.zip",passwords, 10)
    print "time for thread based brutte force", time.time()-t

    # -- tests show that first version is the fastest 