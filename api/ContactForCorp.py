class Contact:
    def __init__(self, name, sex, cellphone, birthDate, email, adress, pkCustomerSort, qqnumber, wxnumber, otherPhone):
        self.name, self.sex, self.cellphone, self.birthDate, self.email, self.adress, \
        self.pkCustomerSort, self.qqnumber, self.wxnumber, self.otherPhone = name, sex, cellphone, birthDate, email, adress, pkCustomerSort, \
                                                                             qqnumber, wxnumber, otherPhone


class Subject:
    # 科目类 包含科目名称
    def __init__(self, subjectName):
        self.subjectName = subjectName
