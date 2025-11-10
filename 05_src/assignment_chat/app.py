from assignment_chat.main import swanson_quote_chat
import gradio as gr
from dotenv import load_dotenv
import os

from utils.logger import get_logger

_logs = get_logger(__name__)

load_dotenv('.secrets')

chat = gr.ChatInterface(
    fn=swanson_quote_chat,
    type="messages"
)

if __name__ == "__main__":
    _logs.info('Getting the Swanson Bot...')
    chat.launch()