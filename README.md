# Prerequisites

1. [Git](https://git-scm.com/)
2. [Homebrew](https://brew.sh)
3. [Anaconda](https://docs.anaconda.com/anaconda/install/mac-os/)

```
brew install node
```

# Setup

First, clone this repo

```
git clone https://github.com/aneeshvathul/DocLlama
```
<br />

Then, create a new conda environment and activate it

```
conda create -n DocLlama
```
```
conda activate DocLlama
```
Change directory to your cloned DocLlama repo
```
cd PATH_TO_DOCLLAMA
```
Install Python dependencies and start server
```
pip install -r backend/requirements.txt
```
```
python3 backend/server.py
```
Change directory to the React app
```
cd frontend/react-app
```
Install React/Node dependencies and launch the app!
```
npm install axios
```
```
npm start
```

https://github.com/user-attachments/assets/fee470d5-ae6a-442a-9c3a-5a7bce55335f




