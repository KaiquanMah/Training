import streamlit as st
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from streamlit.runtime.scriptrunner import add_script_run_ctx

from claude import get_claude_response
from llama import get_llama_response
from ui_helpers import render_prompt_box, create_model_column_ui

st.set_page_config(page_title='Model Garden API Playground', layout="wide")
st.title("Model Garden API Playground — Compare APIs")
st.divider()

models = {
    "Claude": "claude-3-7-sonnet@20250219",
    "Llama": "meta/llama-3.3-70b-instruct-maas",
}

pde, containers, empties = create_model_column_ui(models)

prompt = st.chat_input("Your prompt")
if prompt:
    pde.markdown(render_prompt_box(prompt), unsafe_allow_html=True)

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
# TODO Claude Sonnet 3.7
          # 1st full block
          executor.submit(
              get_claude_response, 
              models, 
              prompt, 
              empties[0]
          ),
          # block 1 ends here  

# TODO Meta Llama
         # 2nd full block
              executor.submit(
               get_llama_response, 
               models, 
               prompt,
               empties[1]
           )
          # block 2 ends here
        ]
        for t in executor._threads:
            add_script_run_ctx(t)
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                st.error(f"An error occurred: {e}")
                print(f"Error: {e}")
                traceback.print_exc()
