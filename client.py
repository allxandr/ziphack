import grpc
from concurrent import futures
import time
import ziphack_pb2_grpc as pb2_grpc
import ziphack_pb2 as pb2
import argparse
import os


class ZipHackClient(object):
    '''client for gRPC service'''
    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.ZiphackStub(self.channel)

    def send_message(self, passwords, archive):
        message = pb2.Message(passwords = passwords, archive = archive)
        return self.stub.GetServerResponse(message)

def get_file(fn):
    with open(fn, 'rb') as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description='Provide passwords and archive')
    parser.add_argument("-p", dest="passwords", required=True)
    parser.add_argument("archive", type=str)

    args = parser.parse_args()
    if not os.path.isfile(args.passwords):
        print "passwords file not found"
        return
    if not os.path.isfile(args.archive):
        print "archive file not found"
        return

    client = ZipHackClient()
    result = client.send_message(passwords = get_file(args.passwords), archive = get_file(args.archive))
    print result

if __name__ == '__main__':
    main()