import os
import yaml


def read_config():
    config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.yml")
    with open(config_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
    return y


def get_account(env='test'):
    # 获取具体登录账户
    y = read_config()
    if env == 'test':
        account = y['test_env']['account']
    elif env == 'pro':
        account = y['pro_env']['account']
    elif env == 'h5_test':
        account = y['h5_test']['account']
    elif env == 'h5_pro':
        account = y['h5_pro']['account']
    elif env == 'group_account':
        account = y['h5_test']['group_account']
    elif env == 'group_account_pro':
        account = y['h5_pro']['group_account']
    else:
        account = None
    return account


def get_root_url(env='test'):
    y = read_config()
    if env == 'test':
        root_url = y['test_env']['base_url']
    elif env == 'pro':
        root_url = y['pro_env']['base_url']
    elif env == 'h5_test':
        root_url = y['h5_test']['base_url']
    elif env == 'h5_pro':
        root_url = y['h5_pro']['base_url']
    else:
        root_url = None
    return root_url


def get_mysql(env='test'):
    # print(env)
    y = read_config()
    if env == 'test':
        msyql = y['test_env']['mysql']
    elif env == 'pro':
        msyql = y['pro_env']['mysql']
    else:
        msyql = None
    return msyql


def get_redis(env='test'):
    y = read_config()
    if env == 'test':
        redis = y['test_env']['redis']
    elif env == 'pro':
        redis = y['pro_env']['redis']
    else:
        redis = None
    return redis


if __name__ == '__main__':
    print(get_mysql(env='test'))
