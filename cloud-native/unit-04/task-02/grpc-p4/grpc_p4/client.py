"""
A module for an Large Language Model (LLM) gRPC client
"""

# import third-party modules
import asyncio
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc


# text goes here
async def main() -> None:
    """
    Text goes here
    """
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = llm_pb2_grpc.LLMServiceStub(channel)
        for element in stub.LLMStream(llm_pb2.LLMStreamRequest(message="hello")):
            print(element.choices[0].text, end="", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
