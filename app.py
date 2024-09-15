import os
import json
from flask_cors import CORS
from flask import Flask, request, render_template
from evaluator.pass_at_k import calculate_pass_at_k
from evaluator.codebleu_scorer import calculate_average_codebleu, calculate_average_codebleu_per_task

app = Flask(__name__)
CORS(app)

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def format_number(value):
    try:
        formatted_number = "{:.4f}".format(float(value))
        return formatted_number
    except (ValueError, TypeError):
        return value


app.jinja_env.filters['format_number'] = format_number


@app.route('/', methods=['GET'])
def index():
    response = {
        'system_architect': 0,
        'db_architect': len(json.load(open(os.path.join(DIR_PATH, 'assertion/test_cases_results/db_arch_agent_results.json'), 'r')).keys()),
        'backend_dev': len(json.load(open(os.path.join(DIR_PATH, 'assertion/test_cases_results/backend_dev_agent_results.json'), 'r')).keys()),
        'frontend_dev': len(json.load(open(os.path.join(DIR_PATH, 'assertion/test_cases_results/frontend_dev_agent_results.json'), 'r')).keys()),
    }

    return render_template('index.html', response=response)


@app.route('/evaluation/<agent_type>', methods=['GET'])
def db_architect(agent_type):
    response = {}

    if agent_type == 'db_architect':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/db_arch_agent_results.json')
        response['agent_name'] = 'Database Architect'
        response['agent_type'] = 'db_architect'
    elif agent_type == 'backend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/backend_dev_agent_results.json')
        response['agent_name'] = 'Backend Developer'
        response['agent_type'] = 'backend_dev'
    elif agent_type == 'frontend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/frontend_dev_agent_results.json')
        response['agent_name'] = 'Frontend Developer'
        response['agent_type'] = 'frontend_dev'
    else:
        return "This agent type is under development!"

    all_results = json.load(open(all_results_file_path, 'r'))

    response['total_models'] = len(all_results.keys())

    all_models = []

    for model_id in all_results.keys():
        model_name = all_results[model_id]['name']
        total_tasks = len(all_results[model_id]['test_results'])

        if response['agent_type'] == 'db_architect' or response['agent_type'] == 'backend_dev':
            passed_tasks = len([result for result in all_results[model_id]['test_results'] if any(attempt['output'] for attempt in result['attempts'])])

            all_models.append({
                'model_id': model_id,
                'model_name': model_name,
                'total_tasks': total_tasks,
                'passed_tasks': passed_tasks,
                'pass_at_k': calculate_pass_at_k(all_results[model_id]['test_results'])[1],
            })
        elif response['agent_type'] == 'frontend_dev':
            all_models.append({
                'model_id': model_id,
                'model_name': model_name,
                'total_tasks': total_tasks,
                'average_codebleu': round(calculate_average_codebleu(all_results[model_id]['test_results']), 4),
            })

    response['all_models'] = all_models

    return render_template('overview.html', response=response)


@app.route('/evaluation/<agent_type>/<model_id>', methods=['GET'])
def get_db_architect_model_individual_results(agent_type, model_id):
    if agent_type == 'db_architect':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/db_arch_agent_results.json')
    elif agent_type == 'backend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/backend_dev_agent_results.json')
    elif agent_type == 'frontend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/frontend_dev_agent_results.json')

    tasks_results_json = json.load(open(all_results_file_path, 'r'))[model_id]

    tasks_results_json['agent_type'] = agent_type
    tasks_results_json['model_id'] = model_id

    if agent_type == 'db_architect' or agent_type == 'backend_dev':
        return render_template('evaluation_db_be.html', results=tasks_results_json)
    elif agent_type == 'frontend_dev':
        return render_template('evaluation_fe.html', results=tasks_results_json)


@app.route('/evaluation_data/<agent_type>/<model_id>', methods=['GET'])
def get_evaluation_results(agent_type, model_id):
    if agent_type == 'db_architect':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/db_arch_agent_results.json')
    elif agent_type == 'backend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/backend_dev_agent_results.json')
    elif agent_type == 'frontend_dev':
        all_results_file_path = os.path.join(DIR_PATH, 'assertion/test_cases_results/frontend_dev_agent_results.json')

    all_results = json.load(open(all_results_file_path, 'r'))

    tasks_results_json = all_results[model_id]

    model_name = tasks_results_json['name']

    total_tasks = len(tasks_results_json['test_results'])

    if agent_type == 'db_architect' or agent_type == 'backend_dev':
        passed_tasks = len([result['task_id'] for result in tasks_results_json['test_results'] if any(attempt['output'] for attempt in result['attempts'])])

        failed_tasks = total_tasks - passed_tasks

        failed_with_error = len([result['task_id'] for result in tasks_results_json['test_results']
                                 if all(attempt['output'] == False and attempt['errors'] != "No errors" for attempt in result['attempts'])])

        unsuccessful_in_test_cases = failed_tasks - failed_with_error

        pass_at_k, average_pass_at_k = calculate_pass_at_k(tasks_results_json['test_results'])

        other_models = []
        for id in all_results.keys():
            pt = len([result['task_id'] for result in all_results[id]['test_results'] if any(attempt['output'] for attempt in result['attempts'])])

            if pt < 5:
                continue

            model_name = all_results[id]['name']
            _, apak = calculate_pass_at_k(all_results[id]['test_results'])

            other_models.append({
                'model_id': id,
                'model_name': model_name,
                'average_pass_at_k': apak
            })

        other_models = sorted(other_models, key=lambda x: x['average_pass_at_k'], reverse=True)

        model_results = {
            'model_id': model_id,
            'model_name': model_name,
            'total_tasks': total_tasks,
            'passed_tasks': passed_tasks,
            'failed_tasks': failed_tasks,
            'failed_with_error': failed_with_error,
            'unsuccessful_in_test_cases': unsuccessful_in_test_cases,
            'pass_at_k': pass_at_k,
            'average_pass_at_k': average_pass_at_k,
            'other_models': other_models
        }
    elif agent_type == 'frontend_dev':
        average_codebleu = round(calculate_average_codebleu(tasks_results_json['test_results']), 4)
        average_codebleu_per_task = [{"task_id": result['task_id'], "average_codebleu": calculate_average_codebleu_per_task(result['attempts'])} for result in tasks_results_json['test_results']]

        other_models = []
        for id in all_results.keys():
            model_name = all_results[id]['name']
            avg_cb = round(calculate_average_codebleu(all_results[id]['test_results']), 4)

            other_models.append({
                'model_id': id,
                'model_name': model_name,
                'average_codebleu': avg_cb
            })

        other_models = sorted(other_models, key=lambda x: x['average_codebleu'], reverse=True)

        model_results = {
            'model_id': model_id,
            'model_name': model_name,
            'total_tasks': total_tasks,
            'average_codebleu': average_codebleu,
            'average_codebleu_per_task': average_codebleu_per_task,
            'other_models': other_models
        }

    return json.dumps(model_results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
