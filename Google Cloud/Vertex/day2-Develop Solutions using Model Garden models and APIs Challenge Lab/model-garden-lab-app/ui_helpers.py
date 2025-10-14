import streamlit as st

header_styles = {
    "Claude": """
        background-color: #F0EEE5;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    """,
    "Llama": """
        background-color: rgb(0, 129, 251);
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    """
}

prompt_display_outline = """
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 5px;
        padding: 10px 15px;
        display: block;
        margin-bottom: 10px;
    """

prompt_display_title = """
        background-color: #000;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        border-radius: 5px;
        margin-bottom: 10px;
    """

def render_prompt_box(prompt):
    prompt_display_content = f"""
        <div style='{prompt_display_outline}'>
            <div style='{prompt_display_title}'>
                Prompt
            </div>
            {prompt}
        </div>
    """
    return prompt_display_content


def create_model_column_ui(models):

    pdc = st.container()
    pde = pdc.empty()

    cols = [col for col in st.columns(2)]
    containers = []
    empties = []

    for i, model in enumerate(models):
        container = cols[i].container(border=True)
        container.markdown(
            f"<div style='{header_styles[model]}'>{model}</div>",
            unsafe_allow_html=True)
        empty = container.empty()
        containers.append(container)
        empties.append(empty)

    return pde, containers, empties
