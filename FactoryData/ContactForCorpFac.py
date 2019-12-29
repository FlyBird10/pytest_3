from api.ContactForCorp import Contact
import factory.fuzzy
import datetime


class ContactFac(factory.Factory):
    class Meta:
        model = Contact

    name = factory.Faker("name", locale="zh_CN")
    sex = factory.fuzzy.FuzzyChoice([0, 1])
    cellphone = factory.Faker("phone_number", locale="zh_CN")
    birth = factory.fuzzy.FuzzyDate(start_date=datetime.date(1900, 1, 1), end_date=datetime.date(2000, 1, 1))
    email = factory.Faker("email", locale="zh_CN")
    address = factory.Faker("address", locale='zh_CN')
    pkCustomerSort = factory.fuzzy.FuzzyChoice(["3036443533", "5114883119", "6145407299", "8276581514"])
    qqnumber = factory.fuzzy.FuzzyText("128", 6, "0", "0123456789", )  # 128开头，0结尾，中间随机6位数
    wxnumber = cellphone
    otherPhone = cellphone


def get_contact(n=1):
    contacts = factory.build_batch(ContactFac, n)
    contacts_list = [item.__dict__ for item in contacts]
    return contacts_list


if __name__ == '__main__':
    print(get_contact())
