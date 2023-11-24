# Open-ChatGPT-Plugins
Open-ChatGPT-Plugins is an open-source project🌟, aimed at building an open and diversified ecosystem for chatbot plugins. This project enables developers to easily add new features and interactive experiences to the ChatGPT model✨.
[Contact Author](https://github.com/XingYu-Zhong)

## Background 📚

OpenAI introduced GPT-4 Turbo at the developer conference, proposing the concept of "Assistants." This was seen by developers as a plugin marketplace for the general public version (non-plugin developers). With the increased context length and high comprehension ability of GPT-4 Turbo, we can replicate the capabilities of ChatGPT-Plugins, thus building an open-source local version of ChatGPT-Plugins.

## Features 💡

1. Unlike other tool projects, our project fully adapts to the API service of ChatGPT-Plugins. This means if you have previously written an API for ChatGPT-Plugins, you can directly interface with the previous API service using this project, with no need for redevelopment🚀.
2. Experience the Plugins service without purchasing ChatGPT Plus🎉.

## Installation 🔧

To install the required packages for this plugin, run the following command:

.. code-block:: shell

    pip install -r requirements.txt

## Usage 🖥️

- First Method: Upload the API's YAML file

.. code-block:: python

    assistant = Assistants(yaml_file_path='../openai.yaml', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
    print(assistant.run('Please look up the historical stock data of Guizhou Moutai for yesterday'))

- Second Method: Use through Assistant ID

.. code-block:: python

    assistant = Assistants(assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
    print(assistant.run('Please look up the historical stock data of Guizhou Moutai for yesterday'))

- Third Method: Update the YAML file

.. code-block:: python

    assistant = Assistants(yaml_file_path='../openai.yaml', assistant_id='eafa9807-7cff-4afb-b069-ce3437c076fb', tools_model='gpt-4-1106-preview', openai_api_key='sk-xxxx')
    print(assistant.run('Please look up the historical stock data of Guizhou Moutai for yesterday'))

Note: The API service must be run first. For the API service, refer to the [StockMarketAssistant](https://github.com/XingYu-Zhong/StockMarketAsisstant) project🔗.

## Principle 🤖

This project replicates ChatGPT-Plugins, requiring a YAML file to describe the interface, with one YAML corresponding to the initialization of an Assistant. The main process includes:

- Reading the YAML file and creating an Assistant based on its description.
- Starting a thread.
- First, recommend tools.
- Then, combine the recommendation list to make a plan.
- Follow the plan step by step.
- Combine the results of each step to generate the final result.

## 📝 License
MIT License
Disclaimer: We share this code for academic purposes under the MIT educational license.
