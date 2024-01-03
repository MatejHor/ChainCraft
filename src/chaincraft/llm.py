from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

import os

from ChainCraft.src.chaincraft.module import Module

class LLMmodel(Module):
    def __init__(self, **kwargs):
        self.callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
        self.llm = None
        super().__init__()

    def setup(
        self,
        name="llama13b.gguf",
        temperature=0.3,
        verbose=True,
        n_batch=512,
        n_threads=6,
        n_gpu_layers=32,
        n_ctx=50000,
    ):
        model_path = os.path.join(".", "models", name)

        self.llm = LlamaCpp(
            model_path=model_path,
            temperature=temperature,
            n_gpu_layers=n_gpu_layers,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_batch=n_batch,
            callback_manager=self.callback_manager,
            verbose=verbose,
        )

    def process(self, prompt):
        if self.llm:
            return self.llm(prompt)
        return "Model is not loaded!"
