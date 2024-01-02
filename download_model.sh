#!/bin/bash
URL="https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q5_K_M.gguf?download=true"
MODEL_PATH=models/llama13b_chat_q5km.gguf
if [ ! -d ./models ]; then
    mkdir /models
fi

curl -L $URL -o $MODEL_PATH