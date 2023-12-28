
# Open-ChatGPT-Plugins 😎

*Read this in other languages: [English](README_EN.md), [中文](README.md).*

Open-ChatGPT-Plugins is an open-source project🌟 aimed at building an open and diverse ecosystem of chatbot plugins. This project enables developers to easily add new functionalities and interactive experiences to the ChatGPT model✨.

## Background 📚

At the Developer Conference, OpenAI introduced GPT-4 Turbo, proposing the concept of "Assistants". This was seen by developers as a plugin marketplace for the general public version (non-plugin developers). With the increased context length of GPT-4 Turbo and its high comprehension ability, we can replicate the capabilities of ChatGPT-Plugins, thus building an open-source local version of ChatGPT-Plugins.

## Features 💡

1. Unlike other tool projects, this project is fully compatible with the ChatGPT-Plugins API service. This means that if you have previously written an API for ChatGPT-Plugins, you can directly interface with the previous API service using this project, without the need for redevelopment🚀.
2. Experience Plugins services without purchasing ChatGPT Plus🎉.

## Installation 🔧

To install the necessary packages for this plugin, run the following command:

```shell
pip install openplugins
```

## Usage 🖥️

- First method: Upload the API's YAML file

```python
import openplugins
assistant = openplugins.Assistants(yaml_file_path='../openai.yaml', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('Please check the historical stock data of Guizhou Maotai for yesterday'))
print(assistant.id)
```

- Second method: Use via Assistant ID

```python
import openplugins
assistant = openplugins.Assistants(assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('Please check the historical stock data of Guizhou Maotai for yesterday'))
```

- Third method: Update the YAML file

```python
import openplugins
assistant = openplugins.Assistants(yaml_file_path='openai.yaml', assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('Please check the historical stock data of Guizhou Maotai for yesterday'))
```

Note: The API service must be run first. For the API service, refer to the [StockMarketAssistant](https://github.com/XingYu-Zhong/StockMarketAsisstant) project🔗.Or check out the official openai project[plugins-quickstart](https://github.com/openai/plugins-quickstart)
return is a dict
```python
import openplugins
assistant = openplugins.Assistants(yaml_file_path='openai.yaml', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxxxxxx')
print(assistant.run('result of 1+1'))
```
```shell
{'plan': [{'tool': '', 'plan': 'Reply with the result of "1+1", which is "2".'}], 'response': '2'}
```
View currently available assistants
```python
import openplugins
data = openplugins.DataInfo()
print(data.get_all_assistants_info())
```

Delete currently available assistants
```python
import openplugins
data = openplugins.DataInfo()
data.delete_assistant(assistant_id = 'cf1f114a-019c-4e36-a8d4-681f5027ef8c')
```

## Principle 🤖

This project replicates ChatGPT-Plugins and requires a YAML file to describe the interface, with one YAML corresponding to the initialization of an Assistant. The main process includes:

- Reading the YAML file and creating an Assistant based on the file description.
- Starting a thread.
- First, recommend tools.
- Formulate a plan based on the recommendation list.
- Call the services step by step according to the plan.
- Generate the final result by combining the results of each step.

### TODO List:

- Check if the YAML file meets requirements (To be completed)📝.
- Integrate Streamlit UI (To be completed)🖌️.

## 📝 License
MIT License 
Disclaimer: We share this code for academic purposes under the MIT educational license.
