"""
A module for an Large Language Model (LLM) gRPC server
"""

# import built-in modules
from time import time
from typing import AsyncGenerator
from typing import Dict
from typing import List

# import third-party modules
from google.protobuf.timestamp_pb2 import Timestamp
from llama_cpp import Llama
import asyncio
import grpc

# import local modules
from grpc_p4.llmproto.v1 import llm_pb2
from grpc_p4.llmproto.v1 import llm_pb2_grpc

# set environment variable
port = "50051"

# declare and initialize a variable called "model" by assigning a Llama object to it
model = Llama(model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf", n_ctx=512, n_batch=1)

# set the max number of tokens allowed for each LLM prompt
MAX_TOKENS = 512


# text goes here
class LLMService(llm_pb2_grpc.LLMServiceServicer):
    """
    Text goes here
    """

    async def Completion(
        self, request: llm_pb2.CompletionRequest, context: grpc.ServicerContext
    ) -> llm_pb2.CompletionResponse:
        """
        Text goes here
        """
        print(f"Completion Request: {request.message}")
        seconds = int(time())
        timestamp = Timestamp()
        timestamp.FromSeconds(seconds)
        return llm_pb2.CompletionResponse(
            id="cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4",
            object="text_completion",
            created=timestamp,
            model="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
            choices=[
                llm_pb2.Choice(
                    text="Beep boop", index=0, logprobs="null", finish_reason="stop"
                )
            ],
            usage=llm_pb2.Usage(
                prompt_tokens=198, completion_tokens=10, total_tokens=208
            ),
        )

    async def LLMStream(
        self, request: llm_pb2.LLMStreamRequest, context: grpc.ServicerContext
    ) -> AsyncGenerator[llm_pb2.LLMStreamResponse, None]:
        """
        Text goes here
        """
        print(f"LLM Stream Request: {request.message}")
        model_description = "You are an assistant."
        llmprompt = f"<|system|>\n{model_description}</s>\n<|user|>{request.message}</s><|assistant|>"
        for element in model(
            llmprompt, temperature=0.0, max_tokens=MAX_TOKENS, stream=True
        ):
            assert isinstance(element, Dict)
            assert isinstance(element["choices"], List)
            assert element["choices"][0]["logprobs"] is None
            seconds = int(element["created"])
            timestamp = Timestamp()
            timestamp.FromSeconds(seconds)
            yield llm_pb2.LLMStreamResponse(
                id=element["id"],
                object=element["object"],
                created=timestamp,
                model=element["model"],
                choices=element["choices"],
            )


# text goes here
async def main() -> None:
    """
    Text goes here
    """
    # declare and initialize a variable called "server" using
    # a grpc.server() object
    server = grpc.aio.server()

    # declare and initialize a variable called "llmservice" using
    # a LLMService() object
    llmservice = LLMService()

    # bind the LLMService to the gRPC server
    llm_pb2_grpc.add_LLMServiceServicer_to_server(llmservice, server)

    # add a port to the gRPC server
    server.add_insecure_port("[::]:" + port)

    # start the gRPC server
    await server.start()
    print(f"Server started, listening on {port}")
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(main())
