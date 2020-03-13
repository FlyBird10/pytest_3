import pytest
from utils.generator import read_yml
import os
from FactoryData.ContactForCorpFac import get_subject

root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
data_path = os.path.join(root_path, "data")
finance_path = os.path.join(data_path, "data_finance")

yml_data = read_yml(os.path.join(finance_path, "finance_assistAccoun.yml"))


@pytest.fixture(params=yml_data['addContacts']['requestList'])
def get_add_contacts_data(request):
    request.param['pkAccountBook'] = yml_data['findContacts']['requestList'][0]['pkAccountBook']
    request.param['contactsCrop'] = get_subject()[0]['subjectName']
    return request.param


@pytest.fixture(params=yml_data['findContacts']['requestList'])
def get_find_all_contacts_data(request):
    return request.param
