sudo apt install jq -y
sudo apt install python3-pip python3-venv -y
cd llmservice-handout/
python3 -m venv venv
source venv/bin/activate
python3 -m pip install flask llama-cpp-python waitress locust wonderwords