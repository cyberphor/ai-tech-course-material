sudo apt install jq -y
sudo apt install python3-pip python3-venv -y
cd llmservice-handout/
python3 -m venv venv
source venv/bin/activate
python3 -m pip install flask llama-cpp-python waitress locust wonderwords
cd worker/src/
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q2_K.gguf