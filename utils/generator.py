import yaml
import os


def read_yml(yml_file):
    # data_path = "E:\\pytest_3\\data\\customer_my.yml"
    with open(yml_file, encoding='utf-8') as f:
        y = yaml.load(f, Loader=yaml.FullLoader)
        return y


def write_py(data_file, case_file, template_file):
    data_yml = read_yml(data_file)
    yml_file_name = os.path.basename(data_file)
    if os.path.exists(case_file):
        return '{file} is exist,please check it'.format(file=case_file)
    else:
        with open(template_file) as f:
            template_info_header = ''
            i = 0
            while i < 7:
                data = f.readline()
                template_info_header = template_info_header + data
                i += 1
            template_info_body = f.readlines()
            template_info_body_str = ''
            for item in template_info_body:
                template_info_body_str = template_info_body_str + item
            with open(case_file, 'a+') as f:
                template_info_header = template_info_header.format(yaml_file=yml_file_name)
                f.write(template_info_header)
                # print(data_yml.items())
                for k, v in data_yml.items():
                    print(k)
                    new_py = template_info_body_str.format(API_id=k)
                    # print(new_py)
                    f.write(new_py)
        return '{file} create success'.format(file=case_file)


def generator_test_case(get_path):
    print(get_path['template_file'])
    file_list = os.listdir(get_path['data_path'])
    result_list = []
    for item in file_list:
        data_file = os.path.join(get_path['data_path'], item)
        case_file = os.path.join(get_path['test_path'], 'test_' + item).replace('.yml', '.py')
        result = write_py(data_file, case_file, get_path['template_file'])
        result_list.append(result)
    return result_list


if __name__ == '__main__':
    print(read_yml("E:\\pytest_3\\data\\h5_index.yml"))
    # print(generator_test_case())
