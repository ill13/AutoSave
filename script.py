import gradio as gr
import modules.shared as shared
import json
from datetime import datetime
from pathlib import Path


myprompt="no data"

params = {
    "name": "AutoSave",
    "display_name": "AutoSave",
    "activate": True,
    "custom string": "n/a",
}

def save_data(string,timestamp=True):
    mydate=datetime.now().strftime('%Y%m%d')
    fname = f"{mydate}_text_log.txt"
    
    file_path=f'extensions/{params["name"]}/output'
    
    if not Path(file_path).exists():
        Path(file_path).mkdir()
    
    model = shared.model_name
    adapter = getattr(shared.model,'active_adapter','None')    
        
    with open(Path(f'{file_path}/{fname}'), 'a+', encoding='utf-8') as f:
        f.write(json.dumps({"model": model, "adapter":  adapter, "prompt" : myprompt, "reply":string} , indent=2 ))
    
    return Path(f'{file_path}/{fname}')

def input_modifier(string):
    """
    This function is applied to your text inputs before
    they are fed into the model.
    """ 
    global myprompt
    myprompt=string
    #print (f"input query:{myprompt}")

    return string

def output_modifier(string):
    """
    This function is applied to the model outputs.
    """
    if not params['activate']:
        return string
    
    save_data(string,timestamp=False)

    return string

def bot_prefix_modifier(string):
    """
    This function is only applied in chat mode. It modifies
    the prefix text for the Bot and can be used to bias its
    behavior.
    """
    return string

def ui():
    # Gradio elements
    activate = gr.Checkbox(value=params['activate'], label='Activate AutoSave')
    #string = gr.Textbox(value=params["bias string"], label='Custom Text')

    # Event functions to update the parameters in the backend
    #string.change(lambda x: params.update({"custom string": x}), string, None)
    activate.change(lambda x: params.update({"activate": x}), activate, None)

