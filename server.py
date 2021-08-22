import grpc
from concurrent import futures
import time
import ziphack_pb2_grpc as pb2_grpc
import ziphack_pb2 as pb2
import os
from brute import BruteArchive

class ZipHackService(pb2_grpc.ZiphackServicer):
    '''Wrapper for Service that generated from proto'''
    def __init__(self, max_workers):
        self._max_workers = max_workers
        self.brutter = BruteArchive(max_workers)


    def GetServerResponse(self, request, context):
        '''Only overload function - gets request and returns response'''
        brute_result = self.brutter.brute(context.peer(),request.archive, request.passwords, request.priority)
        password = brute_result.password # - blocking getter 
        if password is not  None:
            return pb2.MessageResponse(password = password)
        return  pb2.MessageResponse(password = "", error = "Password not found")
        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(10))
    pb2_grpc.add_ZiphackServicer_to_server(ZipHackService(max_workers = 10), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print "Listening on 50051"
    server.wait_for_termination()


if __name__ == '__main__':
    serve()