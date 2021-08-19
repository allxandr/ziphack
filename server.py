import grpc
from concurrent import futures
import time
import ziphack_pb2_grpc as pb2_grpc
import ziphack_pb2 as pb2
from brutteforce import brutte, brutte_thread
import os


def create_zip(fn, data):
    with open(fn, 'wb') as f:
        f.write(data)

class ZipHackService(pb2_grpc.ZiphackServicer):
    '''Wrapper for Service that generated from proto'''
    def __init__(self, max_workers):
        self._max_workers = max_workers

    def GetServerResponse(self, request, context):
        '''Only overload function - gets request and returns response'''

        passwords = request.passwords
        filename = "{}.zip".format(context.peer().replace(':',''))
        create_zip(filename, bytes(request.archive))
        password = brutte(filename, 
                            [i.strip() for i in passwords.split("\n")], 
                            self._max_workers) # brutte_thread is also available
        os.remove(filename)
        if password:
            return pb2.MessageResponse(password = password)
        return  pb2.MessageResponse(password = "", error = "Password not found")
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))
    pb2_grpc.add_ZiphackServicer_to_server(ZipHackService(max_workers = 10), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print "Listening on 50051"
    server.wait_for_termination()


if __name__ == '__main__':
    serve()