# Open-ChatGPT-Plugins 😎

Open-ChatGPT-Plugins 是一个开源项目🌟，旨在构建一个开放和多元化的聊天机器人插件生态系统。本项目使得开发者可以轻松地为 ChatGPT 模型增添新的功能和交互体验✨。

## 背景 📚

OpenAI 在开发者大会上推出了 GPT-4 Turbo，提出了“Assistants”概念。这被开发者视为面向大众版本（非插件开发者）的插件商城。随着 GPT-4 Turbo 上下文长度的增加及其高理解能力，我们可以基于这些特性复刻 ChatGPT-Plugins 的能力，从而构建一个开源本地版本的 ChatGPT-Plugins。

## 特点 💡

1. 与其他工具项目不同，本项目完全适配 ChatGPT-Plugins 的 API 服务。这意味着如果你之前为 ChatGPT-Plugins 编写过 API，那么你可以直接使用本项目与之前的 API 服务对接，无需二次开发🚀。
2. 无需购买 ChatGPT Plus 即可体验 Plugins 服务🎉。

## 安装 🔧

要安装此插件所需的软件包，请运行以下命令：

```shell
pip install -r requirements.txt
```

## 使用方式 🖥️

- 第一种：上传 API 的 YAML 文件

```python
assistant = Assistants(yaml_file_path='../openai.yaml', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('请您查一下贵州茅台的昨天股票历史数据'))
```

- 第二种：通过 Assistant ID 使用

```python
assistant = Assistants(assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('请您查一下贵州茅台的昨天股票历史数据'))
```

- 第三种：更新 YAML 文件

```python
assistant = Assistants(yaml_file_path='../openai.yaml', assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
print(assistant.run('请您查一下贵州茅台的昨天股票历史数据'))
```

注意：需要先运行 API 服务。API 服务可参考 [StockMarketAssistant](https://github.com/XingYu-Zhong/StockMarketAsisstant) 项目🔗。

## 原理 🤖

本项目通过复刻 ChatGPT-Plugins，需要一个 YAML 文件来说明接口，一个 YAML 对应一个 Assistant 的初始化。主要流程包括：

- 阅读 YAML 文件，根据文件描述创建一个 Assistant。
- 开启一个线程。
- 先进行工具推荐（recommend tools）。
- 结合推荐列表制定计划（plan）。
- 按计划逐步调用。
- 结合每一步的结果生成最终结果。

### TODO List:

- 检测 YAML 文件是否符合要求（待完成）📝。
- 集成 Streamlit UI（待完成）🖌️。

## 📝 许可证
MIT License 
免责声明：我们根据 MIT 教育许可出于学术目的共享此代码。