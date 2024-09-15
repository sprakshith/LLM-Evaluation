import os
import json
import time
from tqdm import tqdm
from assertion.test_generated_code import TestFrontEndGeneratedCode


class FrontEndDeveloperAgentEvaluator():
    def __init__(self, model, model_id: str, model_display_name: str, required_attempts: int):
        self.model = model
        self.model_id = model_id
        self.model_display_name = model_display_name
        self.required_attempts = required_attempts

    def __get_testing_codes(self):
        testing_codes_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../assertion/test_cases/frontend_test_cases.json")
        testing_codes = json.load(open(testing_codes_path, "r"))

        return testing_codes

    def __get_model_data(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        all_models_data_path = os.path.join(dir_path, "../assertion/test_cases_results/frontend_dev_agent_results.json")

        if not os.path.exists(all_models_data_path):
            all_models_data = {}
        else:
            milliseconds = int(round(time.time() * 1000))
            all_models_data_backup_path = os.path.join(dir_path, f"../assertion/test_cases_results/frontend_dev_agent_results_backup_{milliseconds}.json")

            all_models_data = json.load(open(all_models_data_path, "r"))

            json.dump(all_models_data, open(all_models_data_backup_path, "w"), indent=4)

        if self.model_id in all_models_data.keys():
            return all_models_data[self.model_id]
        else:
            model_data_dict = {}
            model_data_dict["name"] = self.model_display_name
            model_data_dict["test_results"] = []

            all_models_data[self.model_id] = model_data_dict

            json.dump(all_models_data, open(all_models_data_path, "w"), indent=4)

            return model_data_dict

    def __update_model_data(self, model_data):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        all_models_data_path = os.path.join(dir_path, "../assertion/test_cases_results/frontend_dev_agent_results.json")

        all_models_data = json.load(open(all_models_data_path, "r"))

        all_models_data[self.model_id] = model_data

        json.dump(all_models_data, open(all_models_data_path, "w"), indent=4)

    def __get_prompts(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        system_message_path = os.path.join(dir_path, "../prompts/FrontendDev/Frontend-System-Message.prompt")
        human_message_path = os.path.join(dir_path, "../prompts/FrontendDev/Frontend-Human-Message.prompt")

        system_message = open(system_message_path, "r").read()
        human_message = open(human_message_path, "r").read()

        return system_message, human_message

    def __get_tested_results(self, task, response):
        return TestFrontEndGeneratedCode(task, response).score_response()

    def evaluate_model(self):
        testing_codes = self.__get_testing_codes()

        model_data = self.__get_model_data()

        SYSTEM_MESSAGE, HUMAN_MESSAGE = self.__get_prompts()

        for task in tqdm(testing_codes, desc="Evaluating Model"):
            current_task_data = None
            current_task_data_index = None
            for index, results in enumerate(model_data["test_results"]):
                if results["task_id"] == task["id"]:
                    current_task_data = results
                    current_task_data_index = index

            request = self.model.create_request(system_message=SYSTEM_MESSAGE, human_message=HUMAN_MESSAGE,
                                                coding_task=task["coding_task"], function_signature=task["function_signature"])

            if current_task_data is None:
                current_task_data = {
                    "task_id": task["id"],
                    "prompt": "\n\n".join([i.content for i in request]),
                    "reference_solution": task["reference_solution"],
                    "attempts": []
                }

            while len(current_task_data["attempts"]) < self.required_attempts:
                response = self.model.run(system_message=SYSTEM_MESSAGE, human_message=HUMAN_MESSAGE,
                                          coding_task=task["coding_task"], function_signature=task["function_signature"])

                codebleu_results = self.__get_tested_results(task, response)

                current_task_data["attempts"].append({
                    "attempt_no": len(current_task_data["attempts"]) + 1,
                    "llm_response": response,
                    "result": codebleu_results
                })

            if current_task_data_index is None:
                model_data["test_results"].append(current_task_data)
            else:
                model_data["test_results"][current_task_data_index] = current_task_data

            model_data["test_results"] = sorted(model_data["test_results"], key=lambda x: x["task_id"])

            self.__update_model_data(model_data)
