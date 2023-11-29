import sys
sys.path.append('/home/ubuntu/openplugins')
from openplugins import DataInfo,Assistants

# assistant = Assistants(yaml_file_path='openai.yaml',assistant_id = 'cf1f114a-019c-4e36-a8d4-681f5027ef8c', tools_model='gpt-4-1106-preview', openai_api_key='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')
# print(assistant.run('请打印1+1的结果'))
data = DataInfo()
data.delete_assistant(assistant_id = 'cf1f114a-019c-4e36-a8d4-681f5027ef8c')
print(data.get_all_assistants_info())
