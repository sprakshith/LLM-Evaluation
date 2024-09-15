from langchain_community.llms import Ollama
from langchain_mistralai.chat_models import ChatMistralAI
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


class Mistral:
    def __init__(self, model_name: str = 'mistral:7b-instruct', is_local: bool = True):
        self.model_name = model_name
        self.is_local = is_local
        self.model = self.__initiate_llm()

    def __initiate_llm(self):
        if self.is_local:
            return Ollama(model=self.model_name, temperature=0.2)
        else:
            return ChatMistralAI(model=self.model_name, temperature=0.2)

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
            return self.model.invoke(request).content
