import os
from openai import OpenAI
from langchain_community.llms import Ollama
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

DEEPSEEK_API_KEY = os.environ["DEEPSEEK_API_KEY"]
BASE_URL = "https://api.deepseek.com/v1"


class DeepseekCoder:
    def __init__(self, model_name: str = 'deepseek-coder:6.7b-instruct', is_local: bool = True):
        self.model_name = model_name
        self.is_local = is_local
        self.model = self.__initiate_llm()

    def __initiate_llm(self):
        if self.is_local:
            return Ollama(model=self.model_name, temperature=0.2)
        else:
            return OpenAI(api_key=DEEPSEEK_API_KEY, base_url=BASE_URL)

    def create_request(self, system_message: str, human_message: str, **kwargs):
        system_message = SystemMessagePromptTemplate.from_template(system_message)

        human_message = HumanMessagePromptTemplate.from_template(human_message)

        template_messages = [system_message, human_message]

        prompt_template = ChatPromptTemplate.from_messages(template_messages)

        return prompt_template.format_prompt(**kwargs).to_messages()

    def run(self, system_message: str, human_message: str, **kwargs):
        request = self.create_request(system_message, human_message, **kwargs)

        if self.is_local:
            return self.model.invoke(request)
        else:
            return self.__run_using_openai_client(request)

    def __run_using_openai_client(self, request, **kwargs):
        if 'temperature' not in kwargs:
            kwargs['temperature'] = 0.2

        response = self.model.chat.completions.create(
            model="deepseek-coder",
            messages=[
                {"role": "system", "content": request[0].content},
                {"role": "user", "content": request[1].content},
            ],
            temperature=kwargs['temperature']
        )

        return response.choices[0].message.content
