# import factory
# from django.utils import timezone
# from core.models import CustomUser, Employee, Service

# class ServiceFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Service

#     code = factory.Sequence(lambda n: f'SRV{n}')
#     description = factory.Faker('company')

# class EmployeeFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Employee

#     code = factory.Sequence(lambda n: f'EMP{n:03d}')
#     nom = factory.Faker('last_name')
#     prenom = factory.Faker('first_name')
#     date_naissance = factory.Faker('date_of_birth')
#     date_embauche = factory.Faker('date_this_decade')
#     service = factory.SubFactory(ServiceFactory)