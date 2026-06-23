import gradio as gr

from uuid import uuid4
import base64
from langgraph.checkpoint.memory import InMemorySaver
from prod_rag.agents.default import default_agent
from prod_rag.config import settings
from pathlib import Path
from huggingface_hub import snapshot_download
import os


# Initialize Chroma DB on app startup (runs once per container)
def init_chroma_db():
    db_path = Path(settings.chroma_db_path)
    if not db_path.exists() and os.environ.get("SPACE_ID"):
        # if not db_path.exists():
        print("Downloading Chroma database...")
        try:
            snapshot_download(
                repo_id="adityanandan/lyrics-embeddings-chromadb",
                repo_type="dataset",
                local_dir=str(db_path),
            )
            print("Chroma database downloaded")
        except Exception as e:
            print(f"Failed to download Chroma DB: {e}")

    db_path.mkdir(parents=True, exist_ok=True)


# Run once on app startup
init_chroma_db()

checkpointer = InMemorySaver()
agent = default_agent


theme = gr.themes.Soft(
    primary_hue="indigo",
    secondary_hue="slate",
    radius_size="lg",
)

CUSTOM_CSS = """
.gradio-container {
    max-width: 1200px !important;
    margin: auto;
}

#chatbot {
    height: 70vh;
}

.footer {
    text-align: center;
    opacity: 0.7;
    font-size: 0.9rem;
}
"""


async def chat(message, image, thread_id):
    content = []

    if message:
        content.append(
            {
                "type": "text",
                "text": message,
            }
        )

    if image:
        with open(image, "rb") as f:
            image_bytes = f.read()

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        content.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
            }
        )

    result = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": content,
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": thread_id,
            }
        },
    )

    response = result["messages"][-1]
    return response.content if hasattr(response, "content") else str(response)


with gr.Blocks(
    title='Image to "The Strokes" lyrics',
) as demo:

    thread_id = gr.State(str(uuid4()))

    gr.HTML("""
        <div style="text-align:center;padding:20px">
            <h1>Image to "The Strokes" lyrics</h1>
            <p>
                Upload an image, describe the vibe, and discover matching
                Strokes lyrics.
            </p>
            <img style="height: 300px;display:block;margin:auto;" src="https://m.media-amazon.com/images/M/MV5BM2JjMDBlNjItZDQ3OS00NzExLTgyYjktM2Y2ODU5MjhiMzk5XkEyXkFqcGc@._V1_.jpg">
        </div>
        """)

    with gr.Row():

        with gr.Column(scale=1):

            image_input = gr.Image(
                type="filepath",
                label="Image",
                height=300,
            )

            clear_btn = gr.Button(
                "🗑️ New Conversation",
                variant="secondary",
            )

        with gr.Column(scale=3):

            chatbot = gr.Chatbot(
                label="Conversation", elem_id="chatbot", buttons=["copy"]
            )

            with gr.Row():

                text_input = gr.Textbox(
                    placeholder="Describe the mood or ask about the image...",
                    scale=8,
                    lines=2,
                    container=False,
                )

                submit_btn = gr.Button(
                    "Send",
                    variant="primary",
                    scale=1,
                )

    async def respond(message, image, history, tid):
        if not message and not image:
            return history, "", image

        response = await chat(message, image, tid)

        history.append(
            {
                "role": "user",
                "content": message or "📷 Uploaded image",
            }
        )

        history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return history, "", None

    submit_btn.click(
        respond,
        inputs=[
            text_input,
            image_input,
            chatbot,
            thread_id,
        ],
        outputs=[
            chatbot,
            text_input,
            image_input,
        ],
        show_progress="full",
    )

    text_input.submit(
        respond,
        inputs=[
            text_input,
            image_input,
            chatbot,
            thread_id,
        ],
        outputs=[
            chatbot,
            text_input,
            image_input,
        ],
    )

    clear_btn.click(
        lambda: ([], str(uuid4())),
        outputs=[chatbot, thread_id],
    )

    gr.HTML("""
        <div class="footer">
            Yeet
        </div>
        """)

demo.launch(
    theme=theme,
    css=CUSTOM_CSS,
)
