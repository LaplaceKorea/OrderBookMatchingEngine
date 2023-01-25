from faker import Faker
from numpy.random import Generator, default_rng


def get_random_generator(seed: int = None) -> Generator:
    return default_rng(seed=seed)


def get_faker(seed: int = None) -> Faker:
    faker = Faker()
    faker.seed_instance(seed)
    return faker
