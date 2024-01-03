# ChainCraft
Python-powered toolkit for seamless language model modification. Leverage the robust capabilities of the large language model, seamlessly integrate and modify language models, exploring a range of linguistic functionalities. From efficient scraping tools to advanced calculations, etc...

## Instalation
1. Install anaconda with python>=3.9 
2. Create enviroment `conda create -n ChainCraft`
3. Activate conda env `conda activate ChainCraft`
4. Install necessary libraries `pip install -r requirements`
5. Download LLM model (I tested it with `llama-2-13b-chat.Q5_K_M` via `./download_model.sh`)

## Run
```shell
conda activate ChainCraft
python app.py
```

# Architecture
- configs - Configuration files
    - domains.yaml - List of most common domains
- models - Directory for loading LLM models
- src - Main code
    - chaincraft - Main module
        - llm.py - Code model for LLM 
        - utils.py - Additional reusable functions
        - module.py - Abstract class for all modules
    - scrapper - Scrapper module
- app.py - Main app
- download_model.sh - Script for downloading test LLM model
