import uuid
import time
import yaml
from typing import Callable, Optional,List
from pydantic import BaseModel, Field
import os
import shutil
import inspect
from collections import deque
from openainode.openai_node import *
import ast
from dotenv import load_dotenv
import openai
import json
import requests
import re

from .prompt.few_shot_tools_choose_prompt import *
from .prompt.few_shot_plan_prompt import *
from .prompt.few_shot_parameters_generate_prompt import *

class MessageRecord(BaseModel):
    role: str = Field(description="角色")
    content: str = Field(description="内容")

class Assistants():
    def __init__(self,yaml_file_path:Optional[str]=None,assistant_id:Optional[str]=None,tools_model:Optional[str]=None,openai_api_key:Optional[str]=None):
        load_dotenv()  # 加载.env文件
        if openai_api_key:
            openai.api_key = openai_api_key
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        if tools_model:
            self.tools_model = tools_model
        else:
            self.tools_model = 'gpt-4-1106-preview'
        self.message_history = deque(maxlen=10)
        if yaml_file_path and not assistant_id:
            # 获取调用此方法的栈帧
            stack = inspect.stack()
            # 假设调用者是栈的第二个帧（第一个是当前的 __init__ 方法）
            caller_frame = stack[1]
            # 获取调用者的文件路径
            caller_path = caller_frame.filename
            # 获取调用者的目录路径
            caller_dir = os.path.dirname(caller_path)
            # 构建 openai.yaml 文件的绝对路径
            yaml_file_path = os.path.join(caller_dir, yaml_file_path)

            #根据上传的yaml文件去解析对应的AssistantConfig，然后把yaml文件重命名id.yaml
            with open(yaml_file_path, 'r') as file:
                ods_yaml = yaml.safe_load(file)
            self.components = ods_yaml.get('components', {})
            # 提取 YAML 文件中的数据
            self.title = ods_yaml.get('info', {}).get('title')
            self.description = ods_yaml.get('info', {}).get('description')
            self.id=str(uuid.uuid4())
            self.created_time=int(time.time())
            # 提取 paths 作为 tools
            self.tools = []
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
                    self.tools.append(tool)
                    
            # 提取 servers 的 urls
            self.servers = [server['url'] for server in ods_yaml.get('servers', [])]
            # 将这个yaml文件按照{seld.id}.yaml重新命名存到assistants/data目录下
            # 获取当前文件的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, 'data')
            data_file_path = os.path.join(data_path, f'{self.id}.yaml')
            shutil.copy(yaml_file_path, data_file_path)
        elif assistant_id and not yaml_file_path:
            self.id=assistant_id
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, 'data')
            data_file_path = os.path.join(data_path, f'{self.id}.yaml')
            #根据上传的yaml文件去解析对应的AssistantConfig，然后把yaml文件重命名id.yaml
            with open(data_file_path, 'r') as file:
                ods_yaml = yaml.safe_load(file)
            # 提取 YAML 文件中的数据
            self.components = ods_yaml.get('components', {})
            self.title = ods_yaml.get('info', {}).get('title')
            self.description = ods_yaml.get('info', {}).get('description')
            self.created_time=int(time.time())
            # 提取 paths 作为 tools
            self.tools = []
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
                    self.tools.append(tool)
            
            # 提取 servers 的 urls
            self.servers = [server['url'] for server in ods_yaml.get('servers', [])]
        elif assistant_id and yaml_file_path:
            self.id=assistant_id
            # TODO 检查文件
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_path = os.path.join(current_dir, 'data')
            data_file_path = os.path.join(data_path, f'{assistant_id}.yaml')
            # 获取调用此方法的栈帧
            stack = inspect.stack()
            # 假设调用者是栈的第二个帧（第一个是当前的 __init__ 方法）
            caller_frame = stack[1]
            # 获取调用者的文件路径
            caller_path = caller_frame.filename
            # 获取调用者的目录路径
            caller_dir = os.path.dirname(caller_path)
            # 构建 openai.yaml 文件的绝对路径
            yaml_file_path = os.path.join(caller_dir, yaml_file_path)
            shutil.copy(yaml_file_path, data_file_path)

            with open(data_file_path, 'r') as file:
                ods_yaml = yaml.safe_load(file)
            self.components = ods_yaml.get('components', {})
            # 提取 YAML 文件中的数据
            self.title = ods_yaml.get('info', {}).get('title')
            self.description = ods_yaml.get('info', {}).get('description')
            
            self.created_time=int(time.time())
            # 提取 paths 作为 tools
            self.tools = []
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
                    self.tools.append(tool)
            
            # 提取 servers 的 urls
            self.servers = [server['url'] for server in ods_yaml.get('servers', [])]
        
        
    def run(self, input_text: str):
        self.input_text = input_text
        self._recommend_tools()
        self._get_plan()
        response = self._run_plan()
        return response
        
        
        
        # self.message_history.append(MessageRecord(role = 'user',content = input_text))
    def _GPTLLM(self,model_name :str,prompt:str):
        publicnode = OpenAINode()
        system_prompt = f"""You're an {self.title} assistant. That's your description.\n{self.description}\n """
        system_prompt += f"\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        publicnode.add_system_message(system_prompt)
        if model_name == 'gpt-3.5-turbo-instruct':
             # 创建一个 ChatInput 对象
            chat_config = OldCompleteInput(
                model="gpt-3.5-turbo-instruct",
                prompt = prompt,
                use_streaming=False
            )

            response = publicnode.use_old_openai_with_prompt(chat_config).text
        else:
            message_config = Message(
                role = 'user',
                content = prompt
            )

            # 创建一个 ChatInput 对象
            chat_config = ChatWithMessageInput(
                message=message_config,
                model=model_name,
                append_history=False,
                use_streaming=False
            )
            # 使用 chat_with_prompt_template 方法进行聊天
            response = publicnode.chat_with_message(chat_config).message.content
        return response

    def _recommend_tools(self):
        tools_summary = {}
        for tool in self.tools:
            summary = tool['summary']
            tools_summary[tool['path']] = summary
       
        tools_choose_prompt = TOOLS_CHOOSE_PROMPT + TOOLS_CHOOSE_EXAMPLE_PROMPT + TOOLS_CHOOSE_HINT +f"""\nInput:\ntools_info:{self.tools}\ntools_summary: {tools_summary}\ninput_text: {self.input_text}\nOutput:\n"""     

        response = self._GPTLLM(self.tools_model,tools_choose_prompt)
        # 使用正则表达式匹配字典部分
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            dict_str = match.group()
            # 使用json.loads()函数将字符串转换为字典
            response = json.loads(dict_str)
        else:
            response = json.loads(response)
        # tools_list = response.strip("[]").split(", ")
        tools_list = response['tool']['name']
        self.tools_list = [tool for tool in self.tools if tool['path'] in tools_list]
        self.tools_summary = {}
        for tool in self.tools_list:
            summary = tool['summary']
            self.tools_summary[tool['path']] = summary
        
    
    def _get_plan(self):
        if len(self.tools_summary)==0:
            plan_prompt = PLAN_PROMPT + PLAN_EXAMPLE_PROMPT + PLAN_HINT +f"""\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\nInput:\ntools_summary:you can't use tool\ninput_text: {self.input_text}\nOutput:\n""" 
        else:
            plan_prompt = PLAN_PROMPT + PLAN_EXAMPLE_PROMPT + PLAN_HINT +f"""\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\nInput:\ntools_summary: {self.tools_summary}\ninput_text: {self.input_text}\nOutput:\n"""     
        response = self._GPTLLM(self.tools_model,plan_prompt)
        match = re.search(r'\[.*\]', response)
        if match:
            list_str = match.group()
            # 使用json.loads()函数将字符串转换为列表
            self.plans = ast.literal_eval(list_str)
        else:
            self.plans = ast.literal_eval(response)

    def _get_parametes(self,plan_response:List[str],tool_path:str,plan:str,input_text:str):
        tool_info = {}
        for tool in self.tools:
            if tool['path'] == tool_path:
                tool_info = tool
                break
        parametes_prompt = PARAMETERS_GENERATE_PROMPT + PARAMETERS_GENERATE_EXAMPLE_PROMPT+PARAMETERS_GENERATE_HINT+f"""\nCurrent time: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\nhistory plan:{plan_response}\nInput:\ntools_path:{tool_path}\nplan:{plan}\ninput_text:{self.input_text}\ntool_input_schema:{tool_info}\nOutput:\n""" 
        response = self._GPTLLM(self.tools_model,parametes_prompt)
        # 使用正则表达式匹配字典部分
        match = re.search(r'\{.*\}', response, re.DOTALL)
        if match:
            dict_str = match.group()
            # 使用json.loads()函数将字符串转换为字典
            tool_params = ast.literal_eval(dict_str)
        else:
            tool_params = ast.literal_eval(response)
        return  tool_params

    def _run_plan(self):
        plans_responses = []
        for plan in self.plans:
            if len(plan['tool'])>0:
                #当前需要用到tool，第一步先调用tool需要的参数集合,
                input_text = self.input_text
                tool_params = self._get_parametes(plans_responses,plan['tool'],plan['plan'],input_text)
                tool_response = self._use_tool(plan['tool'],tool_params)
                plan['response'] = tool_response
                
                plans_responses.append(plan)
        #聊天
        chat_prompt = f"""History_message:{self.message_history}\nPlease respond based on current plans (plan_responses) and user input (input_text).\nplans_response:{plans_responses}\ninput_text:{self.input_text}"""
        print(f'chat_prompt:{chat_prompt}')
        response = self._GPTLLM(self.tools_model,chat_prompt)
        self.message_history.append(
            [
                MessageRecord(role="user", content=self.input_text),
                MessageRecord(role="assistant", content=response),
            ]
        )
        return response

    def _use_tool(self,tool_path:str,tool_params:dict):
        method = ''
        tool_responses_info = {}
        for tool in self.tools:
            if tool['path'] == tool_path:
                method = tool['method']
                tool_responses_info = tool['responses']
                break
        
        _, schemas, schema_name = tool_responses_info['200']['content']['application/json']['schema']['$ref'].split("/")[1:]
        # 获取schema
        schema = self.components[schemas][schema_name]
        tool_url = self.servers[0]+tool_path
        try:
            if method == 'get':
                response = requests.get(tool_url, params=tool_params)
            else:
                response = requests.post(tool_url, params=tool_params)
            tool_response = {}
            if response.status_code == 200:
                tool_response['type'] = response.status_code
                tool_response['content'] = response.json()
                tool_response['params'] = schema
            else:
                tool_response['type'] = response.status_code
                tool_response['content'] = []
                tool_response['params'] = []
        except Exception as e:
            tool_response = {
                'type': 'Error',
                'content': str(e),
                'params': []
            }
        return tool_response
        


    



