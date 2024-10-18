import os


def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise Exception(f"{var_name} not set")
    return value
