import numpy as np


def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0

    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def calculate_pass_at_k(test_results, k=1):
    pass_at_k_values = []

    for task in test_results:
        task_id = task['task_id']
        total_attempts = len(task['attempts'])
        correct_attempts = len([attempt for attempt in task['attempts'] if attempt['output'] == True])

        pass_at_k_value = {
            'task_id': task_id,
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'pass_at_k': pass_at_k(total_attempts, correct_attempts, k)
        }

        pass_at_k_values.append(pass_at_k_value)

    return pass_at_k_values, round(np.mean([pass_at_k_value['pass_at_k'] for pass_at_k_value in pass_at_k_values]), 4)
