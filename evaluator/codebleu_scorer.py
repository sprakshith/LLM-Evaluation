import numpy as np


def calculate_average_codebleu(test_results):
    all_codebleus = []

    for result in test_results:
        for attempt in result['attempts']:
            all_codebleus.append(attempt['result']['codebleu'])

    return np.mean(all_codebleus)


def calculate_average_codebleu_per_task(attempts):
    all_codebleus = []

    for attempt in attempts:
        all_codebleus.append(attempt['result']['codebleu'])

    return np.mean(all_codebleus)
