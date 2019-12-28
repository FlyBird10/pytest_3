import os
import yaml


def get_account():
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    account = y['test_env']['account']
    return account


def get_url():
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    root_url = y['test_env']['base_url']
    return root_url


if __name__ == '__main__':
    print(get_account())
