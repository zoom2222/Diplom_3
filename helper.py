from faker import Faker

faker = Faker('ru_RU')

def generate_user_data():
    return {
        'name': faker.first_name(),
        'email': faker.email(),
        'password': faker.password(length=10)
    }