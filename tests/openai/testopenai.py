import pytest
import openai
import os

from openainode.openai_node import *


def test_openai_gpt_response():
     # 创建一个 OpenAINode 对象
    response_node = OpenAINode()


    prompt = "print hello world"

     # 创建一个 ChatInput 对象
    chat_config = OldCompleteInput(
        model="gpt-3.5-turbo-instruct",
        prompt = prompt,
        use_streaming=False
    )

    response = response_node.use_old_openai_with_prompt(chat_config).text
    print(f'response:{response}')


