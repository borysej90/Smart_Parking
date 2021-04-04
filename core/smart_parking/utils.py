from os import environ

from environs import EnvError


def get_secret_value_from_file_or_env(env_var_name: str, t: type = str):
    """
    The function check if environment variable with secret file location is passed.
    One of this is performed (in that order):

    1. Checks for "{env_var_name}_FILE" environment variable containing file path and gets its value.
    2. Gets value from the actual environment variable.

    Raises:
        EnvError - If neither of "{env_var_name}" or "{env_var_name}_FILE" was set.
    """
    if (secret := environ.get(f'{env_var_name}_FILE', '')) == '':
        value = environ.get(env_var_name, '')
    else:
        with open(secret, 'r') as file:
            value = file.read()

    if value == '':
        raise EnvError(f'Environment variable "{env_var_name}" not set')

    return t(value)
