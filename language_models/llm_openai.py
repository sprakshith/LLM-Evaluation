from langchain_openai import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate


class OpenAI:
    def __init__(self, model_name: str = 'gpt-3.5-turbo'):
        self.model_name = model_name
        self.model = self.__initiate_llm()

    def __initiate_llm(self):
        return ChatOpenAI(model=self.model_name, temperature=0.2)

    def create_request(self, system_message: str, human_message: str, **kwargs):
        system_message = SystemMessagePromptTemplate.from_template(system_message)

        human_message = HumanMessagePromptTemplate.from_template(human_message)

        template_messages = [system_message, human_message]

        prompt_template = ChatPromptTemplate.from_messages(template_messages)

        return prompt_template.format_prompt(**kwargs).to_messages()

    def run(self, system_message: str, human_message: str, **kwargs):
        request = self.create_request(system_message, human_message, **kwargs)
        return self.model.invoke(request).content
