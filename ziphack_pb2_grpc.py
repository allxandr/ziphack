# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ziphack_pb2 as ziphack__pb2


class ZiphackStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetServerResponse = channel.unary_unary(
                '/ziphack.Ziphack/GetServerResponse',
                request_serializer=ziphack__pb2.Message.SerializeToString,
                response_deserializer=ziphack__pb2.MessageResponse.FromString,
                )


class ZiphackServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetServerResponse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ZiphackServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetServerResponse': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerResponse,
                    request_deserializer=ziphack__pb2.Message.FromString,
                    response_serializer=ziphack__pb2.MessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ziphack.Ziphack', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Ziphack(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetServerResponse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ziphack.Ziphack/GetServerResponse',
            ziphack__pb2.Message.SerializeToString,
            ziphack__pb2.MessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)