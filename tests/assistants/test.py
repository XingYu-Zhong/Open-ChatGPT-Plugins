# test_assistants.py
import os
import pytest
from assistants.assistants import Assistants

# 假设你有一个有效的 YAML 文件路径和一个 assistant_id
assistant_id = 'eafa9807-7cff-4afb-b069-ce3437c076fb'
# 获取测试文件所在的目录
test_dir = os.path.dirname(os.path.abspath(__file__))

# 构建 YAML 文件的绝对路径
valid_yaml_file_path = os.path.join(test_dir, 'openai.yaml')

# 测试初始化
def test_assistants_init():
    # assistant = Assistants(yaml_file_path='../openai.yaml')
    assistant = Assistants(assistant_id=assistant_id,tools_model='gpt-4-1106-preview')

    # print(assistant.run('请您查一下贵州茅台的昨天股票历史数据'))
    # print(assistant.run('请您分析一下贵州茅台这个股票'))
    print(assistant.run('1+1等于几'))


