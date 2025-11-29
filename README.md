https://platform.openai.com/docs/guides/agents/agent-builder

System Setup (Windows)
- powershell execution policy:
  - `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
- intialize conda for powershell: 
  - `& "C:\Users\kydan\miniconda3\Scripts\conda.exe" init powershell`
- git setup
  - `git config --global user.email "you@example.com"`
  - `git config --global user.name "Your Name"`

Step 1. Install Python
- `conda create -n agent python=3.12`

Step 2. Install requirements.txt
- `pip install -r requirements.txt`

Step 3. Write the agent code
- agent code sample: https://github.com/openai/openai-agents-python
- streamlit code sample: 
- git commands to update:
  - `git stash push`  --save all changes locally
  - `git pull`        --load latest from repository


Step 4. Run python code
- `python agent.py`
- `streamlit run app.py`


### Sample Question
Tell me about the Narmer Palette and the Bing Ma Yong