from api.ContactForCorp import Contact
import factory


class ContactFac(factory.Factory):
    class Meta:
        model = Contact

    name = factory.Faker(  )



