one time 

install uv
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv init
uv sync

uv venv    
 .\.venv\Scripts\activate
#install jupyterlab if missing
uv add jupyterlab
#Start jupyterlab
python -m jupyterlab


2_healt_analysis
    streamlit run app.py