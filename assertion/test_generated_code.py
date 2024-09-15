import os
import re
import subprocess
from codebleu import calc_codebleu
from code_optimizer.code_optimizer import CodeOptimizer


class TestDBArchGeneratedCode():
    def __init__(self, task, response):
        self.test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db_generated_code.py')
        self.python_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../venv/Scripts/python')
        self.task = task
        self.response = response

    def __extract_code(self):
        try:
            match = re.search('```python\n(.*?)```', self.response, re.DOTALL)

            if match:
                code = match.group(1)
                return code
            else:
                if type(self.response) == str:
                    return self.response
        except Exception as e:
            pass

        return ""

    def __write_code(self):
        try:
            with open(self.test_path, 'w') as file:
                # Optimizes the code which has initial imports and the imports inside the model's response
                all_imports = self.task['imports'] + "\n\n" + self.__extract_code()
                optimizer = CodeOptimizer(all_imports)
                optimized_imports = optimizer.optimize_imports()

                # Writes the optimized imports, initial code(creating a session)
                file.write(optimized_imports + "\n\n")
                file.write(self.task['initial_code'] + "\n\n")

                # Extracts only the function definition and body from the response
                optimizer = CodeOptimizer(self.__extract_code())
                function = optimizer.optimize_functions()
                file.write(function + "\n\n")

                # Writes the assertion code
                file.write("def assert_code():\n    ")

                if 'pre_test_code' in self.task.keys():
                    file.write("try:\n        ")
                    file.write(self.task['pre_test_code'])
                    file.write(
                        "\n    except Exception:\n        print('Error in pre-test code')\n        return False\n\n    ")

                file.write("try:\n        ")
                file.write("\n        ".join(self.task['test_cases']))
                file.write(
                    "\n    except AssertionError:\n        print('Error in Assertion!')\n        return False")

                if 'post_test_code' in self.task.keys():
                    file.write("\n\n    try:\n        ")
                    file.write(self.task['post_test_code'])
                    file.write(
                        "\n    except Exception:\n        print('Error in post-test code')\n        return False")

                file.write("\n\n    return True")
                file.write("\n\nprint(assert_code())")
        except Exception as e:
            pass

    def __get_optimized_code(self):
        return open(self.test_path, 'r').read()

    def test_code(self):
        self.__write_code()

        result = subprocess.run([self.python_path, '-m', 'assertion.db_generated_code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = True if result.stdout.decode('utf-8').strip() == "True" else False

        errors = result.stderr.decode('utf-8') if result.stderr.decode('utf-8') else "No errors"

        return output, errors, self.__get_optimized_code()


class TestBackEndGeneratedCode():
    def __init__(self, task, response):
        self.test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'backend_generated_code.py')
        self.python_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../venv/Scripts/python')
        self.task = task
        self.response = response

    def __extract_code(self):
        try:
            match = re.search('```python\n(.*?)```', self.response, re.DOTALL)

            if match:
                code = match.group(1)
                return code
            else:
                if type(self.response) == str:
                    return self.response
        except Exception as e:
            pass

        return ""

    def __write_code(self):
        try:
            with open(self.test_path, 'w') as file:
                # Optimizes the code which has initial imports and the imports inside the model's response
                all_imports = self.task['imports'] + "\n\n" + self.__extract_code()
                optimizer = CodeOptimizer(all_imports)
                optimized_imports = optimizer.optimize_imports()

                # Writes the optimized imports
                file.write(optimized_imports + "\n\n")

                # Extracts only the function definition and body from the response
                optimizer = CodeOptimizer(self.__extract_code())
                function = optimizer.optimize_functions()
                file.write(function + "\n\n")

                # Writes the assertion code
                file.write("def assert_code():\n    ")

                file.write("try:\n        ")

                if 'pre_test_code' in self.task.keys():
                    file.write(self.task['pre_test_code'] + "\n        ")

                file.write("\n        ".join(self.task['test_cases']))

                if 'post_test_code' in self.task.keys():
                    file.write("\n        " + self.task['post_test_code'])

                file.write("\n    except AssertionError:\n        print('Error in Assertion!')\n        return False")

                file.write("\n\n    return True")

                file.write("\n\nprint(assert_code())")
        except Exception as e:
            pass

    def __get_optimized_code(self):
        return open(self.test_path, 'r').read()

    def test_code(self):
        self.__write_code()

        result = subprocess.run([self.python_path, '-m', 'assertion.backend_generated_code'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output = True if result.stdout.decode('utf-8').strip() == "True" else False

        errors = result.stderr.decode('utf-8') if result.stderr.decode('utf-8') else "No errors"

        return output, errors, self.__get_optimized_code()


class TestFrontEndGeneratedCode():
    def __init__(self, task, response):
        self.task = task
        self.response = response

    def __extract_code(self):
        try:
            match = re.search('```javascript\n(.*?)```', self.response, re.DOTALL)

            if match:
                code = match.group(1)
                return code
            else:
                if type(self.response) == str:
                    return self.response
        except Exception as e:
            pass

        return ""

    def score_response(self):
        result = calc_codebleu([self.task["reference_solution"]], [self.__extract_code()], lang="javascript", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
        return result
