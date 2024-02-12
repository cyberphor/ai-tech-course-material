sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 -y
sudo apt install python3.10-venv -y
sudo apt install python3-pip -y
cd ~/multi-model-databases/
python3.10 -m venv project-env
source project-env/bin/activate
pip install -r requirements.txt