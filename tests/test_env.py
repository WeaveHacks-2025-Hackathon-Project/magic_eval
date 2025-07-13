import os
from dotenv import load_dotenv

load_dotenv()


def test_env():
    assert os.getenv("LLAMA_API_KEY") is not None
    assert os.getenv("WANDB_API_KEY") is not None
