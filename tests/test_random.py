from order_matching.random import get_faker, get_random_generator


def test_get_faker() -> None:
    faker = get_faker()
    number_of_ids = 100

    assert len({faker.uuid4() for _ in range(number_of_ids)}) == number_of_ids

    faker1, faker2 = get_faker(seed=42), get_faker(seed=42)

    for _ in range(number_of_ids):
        assert faker1.uuid4() == faker2.uuid4()


def test_get_random_generator() -> None:
    rng = get_random_generator()
    number_of_random_numbers = 100

    assert len({rng.normal() for _ in range(number_of_random_numbers)}) == number_of_random_numbers

    rng1, rng2 = get_random_generator(seed=42), get_random_generator(seed=42)

    for _ in range(number_of_random_numbers):
        assert rng1.normal() == rng2.normal()
