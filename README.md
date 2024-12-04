# How to Install
## Create New Python Virtual Environment
- **Conda Env**
  
  - **Create Environtment**
    
   ```bash
   conda create -m <name_env> python=<python_version>
   ```
   
  - **Activate Environtment**
  ```bash
  conda activate <name_env>
  ```

- **Python Venv**

  - **Create Python VENV**
  ```bash
  python3 -m venv <name_env>
  ```
  
  - **Activate Environtment**
  ```bash
  ./<name_env>/Scripts/activate
  ```

## Installing Dependencies
```bash
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlin run app.py
```
