import os
import yaml


def get_account(env='test'):
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    if env == 'test':
        account = y['test_env']['account']
    elif env == 'pro':
        account = y['pro_env']['account']
    else:
        account = None
    return account


def get_root_url(env='test'):
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    if env == 'test':
        root_url = y['test_env']['base_url']
    elif env == 'pro':
        root_url = y['pro_env']['base_url']
    else:
        root_url = None
    return root_url


if __name__ == '__main__':
    print(get_account())
