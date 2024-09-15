import time
from language_models.llm_openai import OpenAI
from language_models.llm_mistral import Mistral
from language_models.llm_ollama import OllamaLLM
from language_models.llm_deepseek import DeepseekCoder
from evaluator.frontend_agent_evaluator import FrontEndDeveloperAgentEvaluator

start_time = time.time()

# ------------------------------ DATABASE ARCHITECT AGENT EVALUATION ------------------------------

# print('Evaluating Codellama 7b...')
# model = OllamaLLM(model_name='codellama:7b-instruct')
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='codellama-7b', model_display_name='Codellama 7b', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# print('Evaluating Deepseek Coder 6.7b...')
# model = DeepseekCoder(model_name='deepseek-coder:6.7b-instruct', is_local=True)
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='deepseek-coder-6.7b', model_display_name='Deepseek Coder 6.7b', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# print('Evaluating OpenAI GPT-3.5-Turbo...')
# model = OpenAI(model_name='gpt-3.5-turbo')
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='gpt-3.5-turbo', model_display_name='GPT-3.5-Turbo', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# print('Evaluating OpenAI gpt-4...')
# model = OpenAI(model_name='gpt-4')
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='gpt-4', model_display_name='GPT-4', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# print('Evaluating OpenCodeInterpreter DS 6.7b...')
# model = OllamaLLM(model_name='pxlksr/opencodeinterpreter-ds:6.7b-Q4_K')
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='pxlksr-opencodeinterpreter-ds-6.7b', model_display_name='OpenCodeInterpreter DS 6.7b', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# print('Evaluating Mistral 7b...')
# model = Mistral(model_name='open-mistral-7b', is_local=False)
# db_architect_agent_evaluator = DatabaseArchitectAgentEvaluator(model, model_id='mistral-7b', model_display_name='Mistral 7b', required_attempts=5)
# db_architect_agent_evaluator.evaluate_model()

# ------------------------------ BACKEND DEVELOPER AGENT EVALUATION ------------------------------

# print('Evaluating Codellama 7b...')
# model = OllamaLLM(model_name='codellama:7b-instruct')
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='codellama-7b', model_display_name='Codellama 7b', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# print('Evaluating Deepseek Coder 6.7b...')
# model = DeepseekCoder(model_name='deepseek-coder:6.7b-instruct', is_local=True)
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='deepseek-coder-6.7b', model_display_name='Deepseek Coder 6.7b', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# print('Evaluating OpenAI GPT-3.5-Turbo...')
# model = OpenAI(model_name='gpt-3.5-turbo')
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='gpt-3.5-turbo', model_display_name='GPT-3.5-Turbo', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# print('Evaluating OpenAI gpt-4...')
# model = OpenAI(model_name='gpt-4')
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='gpt-4', model_display_name='GPT-4', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# print('Evaluating OpenCodeInterpreter DS 6.7b...')
# model = OllamaLLM(model_name='pxlksr/opencodeinterpreter-ds:6.7b-Q4_K')
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='pxlksr-opencodeinterpreter-ds-6.7b', model_display_name='OpenCodeInterpreter DS 6.7b', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# print('Evaluating Mistral 7b...')
# model = Mistral(model_name='open-mistral-7b', is_local=False)
# backend_dev_agent_evaluator = BackEndDeveloperAgentEvaluator(model, model_id='mistral-7b', model_display_name='Mistral 7b', required_attempts=5)
# backend_dev_agent_evaluator.evaluate_model()

# ------------------------------ FRONTEND DEVELOPER AGENT EVALUATION ------------------------------

# print('Evaluating Codellama 7b...')
# model = OllamaLLM(model_name='codellama:7b-instruct')
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='codellama-7b', model_display_name='Codellama 7b', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

# time.sleep(10)

# print('Evaluating Deepseek Coder 6.7b...')
# model = DeepseekCoder(model_name='deepseek-coder:6.7b-instruct', is_local=True)
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='deepseek-coder-6.7b', model_display_name='Deepseek Coder 6.7b', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

# time.sleep(10)

# print('Evaluating OpenAI GPT-3.5-Turbo...')
# model = OpenAI(model_name='gpt-3.5-turbo')
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='gpt-3.5-turbo', model_display_name='GPT-3.5-Turbo', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

# time.sleep(10)

# print('Evaluating OpenAI gpt-4...')
# model = OpenAI(model_name='gpt-4')
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='gpt-4', model_display_name='GPT-4', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

# time.sleep(10)

# print('Evaluating OpenCodeInterpreter DS 6.7b...')
# model = OllamaLLM(model_name='pxlksr/opencodeinterpreter-ds:6.7b-Q4_K')
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='pxlksr-opencodeinterpreter-ds-6.7b', model_display_name='OpenCodeInterpreter DS 6.7b', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

# time.sleep(10)

# print('Evaluating Mistral 7b...')
# model = Mistral(model_name='open-mistral-7b', is_local=False)
# frontend_dev_agent_evaluator = FrontEndDeveloperAgentEvaluator(model, model_id='mistral-7b', model_display_name='Mistral 7b', required_attempts=2)
# frontend_dev_agent_evaluator.evaluate_model()

end_time = time.time()
print(f'Time taken: {(end_time - start_time)/60} minutes')
