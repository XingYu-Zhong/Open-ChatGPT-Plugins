from pydantic import BaseModel, Field
import os
from datetime import datetime
import uuid
import yaml
import json
import inspect
import shutil

class YamlDataInfo(BaseModel):
    assistant_id: str = Field(description="assistant的唯一id")
    org_file_name: str = Field(description="文件原本上传的名字")
    created_at: str = Field(description="创建时间")
    updated_at: str = Field(description="更新时间")

class DataInfo():
    def __init__(self):
        # 获取当前文件的绝对路径
        data_path = os.path.dirname(os.path.abspath(__file__))
        # 构建要删除的文件的绝对路径
        self.data_info_path = os.path.join(data_path, 'datainfo.json')
        if not os.path.exists(self.data_info_path):
            with open(self.data_info_path, 'w') as file:
                json.dump({}, file, indent=4)

        with open(self.data_info_path, 'r') as file:
            try:
                self.data_info = json.load(file)
            except json.JSONDecodeError:
                self.data_info = {}


    def get_all_assistants_info(self) -> dict:
        return self.data_info

    def create_assistant(self,yaml_file_path:str):
        org_file_name =  os.path.basename(yaml_file_path)
        assistant_id=str(uuid.uuid4())
        yaml_data_info = YamlDataInfo(
            assistant_id=assistant_id,
            org_file_name=org_file_name,
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        # 读取现有的JSON数据或初始化一个空字典
        if os.path.exists(self.data_info_path) and os.path.getsize(self.data_info_path) > 0:
            with open(self.data_info_path, 'r') as file:
                data_info = json.load(file)
        else:
            data_info = {}

        # 添加新的数据
        data_info[assistant_id] = yaml_data_info.dict()

        # 写回JSON文件
        with open(self.data_info_path, 'w') as file:
            json.dump(data_info, file, indent=4)
        self.data_info = data_info
        # 将这个yaml文件按照{seld.id}.yaml重新命名存到assistants/data目录下
        # 获取当前文件的绝对路径
        data_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(data_path, f'{assistant_id}.yaml')
        # 获取调用此方法的栈帧
        stack = inspect.stack()
        caller_frame = stack[2]
        # 获取调用者的文件路径
        caller_path = caller_frame.filename
        # 获取调用者的目录路径
        caller_dir = os.path.dirname(caller_path)
        # 构建 openai.yaml 文件的绝对路径
        yaml_file_path = os.path.join(caller_dir, yaml_file_path)
        shutil.copy(yaml_file_path, data_file_path)
        return assistant_id
    
    def update_assistant(self,assistant_id:str,yaml_file_path:str):
        org_file_name =  os.path.basename(yaml_file_path)
       # 读取现有的 data_info 数据
        if os.path.exists(self.data_info_path) and os.path.getsize(self.data_info_path) > 0:
            with open(self.data_info_path, 'r') as file:
                data_info = json.load(file)
        else:
            data_info = {}

        # 更新对应的 DataInfo
        if assistant_id in data_info:
            data_info[assistant_id]['org_file_name'] = org_file_name
            data_info[assistant_id]['updated_at'] = datetime.utcnow().isoformat()  # JSON不支持原生的datetime，需要转换为字符串
            # 写回更新后的数据
            with open(self.data_info_path, 'w') as file:
                json.dump(data_info, file, indent=4)
            self.data_info = data_info
        else:
            raise ValueError(f"Assistant ID '{assistant_id}' not found in data info.")
                # 将这个yaml文件按照{seld.id}.yaml重新命名存到assistants/data目录下
        # 获取当前文件的绝对路径
        data_path = os.path.dirname(os.path.abspath(__file__))
        data_file_path = os.path.join(data_path, f'{assistant_id}.yaml')
        # 获取调用此方法的栈帧
        stack = inspect.stack()
        caller_frame = stack[2]
        # 获取调用者的文件路径
        caller_path = caller_frame.filename
        # 获取调用者的目录路径
        caller_dir = os.path.dirname(caller_path)
        # 构建 openai.yaml 文件的绝对路径
        yaml_file_path = os.path.join(caller_dir, yaml_file_path)
        shutil.copy(yaml_file_path, data_file_path)


    def delete_assistant(self,assistant_id:str):
        # 获取当前文件的绝对路径
        data_path = os.path.dirname(os.path.abspath(__file__))
        # 构建要删除的文件的绝对路径
        data_file_path = os.path.join(data_path, f'{assistant_id}.yaml')
        # 如果文件存在，则删除
        if os.path.exists(data_file_path):
            os.remove(data_file_path)
        else:
            raise FileNotFoundError(f"File '{data_file_path}' not found.")
       # 读取现有的 data_info 数据
        if os.path.exists(self.data_info_path) and os.path.getsize(self.data_info_path) > 0:
            with open(self.data_info_path, 'r') as file:
                data_info = json.load(file)
        else:
            data_info = {}

        # 删除对应的assistant_id信息
        if assistant_id in data_info:
            del data_info[assistant_id]
            # 写回更新后的数据
            with open(self.data_info_path, 'w') as file:
                json.dump(data_info, file, indent=4)
            # 更新self.data_info以反映删除操作
            self.data_info = data_info
        else:
            raise ValueError(f"Assistant ID '{assistant_id}' not found in data info.")

    def get_assistant_info(self,assistant_id:str):
        # 获取当前文件的绝对路径
        data_path = os.path.dirname(os.path.abspath(__file__))
        # 构建要删除的文件的绝对路径
        yaml_file_path = os.path.join(data_path, f'{assistant_id}.yaml')

        #根据上传的yaml文件去解析对应的AssistantConfig，然后把yaml文件重命名id.yaml
        with open(yaml_file_path, 'r',encoding='utf-8') as file:
            ods_yaml = yaml.safe_load(file)
        components = ods_yaml.get('components', {})
        # 提取 YAML 文件中的数据
        title = ods_yaml.get('info', {}).get('title')
        description = ods_yaml.get('info', {}).get('description')
        # 提取 paths 作为 tools
        tools = []
        paths = ods_yaml.get('paths', {})
        for path, operations in paths.items():
            for method, details in operations.items():
                tool = {
                        'path': path,
                        'method': method,
                        'operation':details['operationId'],
                        'summary': details['summary'],
                        'parameters':details.get('parameters', []),
                        'responses':details['responses']
                    }
                tools.append(tool)      
        # 提取 servers 的 urls
        servers = [server['url'] for server in ods_yaml.get('servers', [])]
        config = {
            'components':components,
            'title':title,
            'description':description,
            'tools':tools,
            'servers':servers
        }
        return config

        
    
