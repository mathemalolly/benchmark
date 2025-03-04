import os

import time
import numpy as np
from deephyper.problem import HpProblem
from deephyper.evaluator import profile, RunningJob

nb_dim = os.environ.get("DEEPHYPER_BENCHMARK_NDIMS", 5)
domain = (-10.0, 10.0)
problem = HpProblem()
for i in range(nb_dim):
    problem.add_hyperparameter(domain, f"x{i}")


def levy(x):
    z = 1 + (x - 1) / 4
    return (
        np.sin(np.pi * z[0]) ** 2
        + np.sum((z[:-1] - 1) ** 2 * (1 + 10 * np.sin(np.pi * z[:-1] + 1) ** 2))
        + (z[-1] - 1) ** 2 * (1 + np.sin(2 * np.pi * z[-1]) ** 2)
    )


@profile
def run(job: RunningJob, sleep=False, sleep_mean=60, sleep_noise=20) -> dict:

    config = job.parameters

    if sleep:
        t_sleep = np.random.normal(loc=sleep_mean, scale=sleep_noise)
        t_sleep = max(t_sleep, 0)
        time.sleep(t_sleep)

    x = np.array([config[k] for k in config if "x" in k])
    x = np.asarray_chkfinite(x)  # ValueError if any NaN or Inf

    return -levy(x)


if __name__ == "__main__":
    print(problem)
    default_config = problem.default_configuration
    print(f"{default_config=}")
    result = run(RunningJob(parameters=default_config))
    print(f"{result=}")
