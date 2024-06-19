from typing import Any, Dict
from generators.base import BaseGenerator
from utils.assertions import assert_types, assert_gt


LOREM_IPSUM_WORDS = [
    "Praesent",
    "bibendum",
    "ligula",
    "leo",
    "et",
    "auctor",
    "nisl",
    "varius",
    "in",
    "Vestibulum",
    "eleifend",
    "arcu",
    "id",
    "turpis",
    "efficitur",
    "finibus",
    "Pellentesque",
    "suscipit",
    "vitae",
    "gravida",
    "scelerisque",
    "ipsum",
    "magna",
    "porta",
    "nunc",
    "at",
    "fringilla",
    "nulla",
    "elit",
    "ut",
    "Donec",
    "nec",
    "facilisis",
    "lectus",
    "Sed",
    "hendrerit",
    "orci",
    "luctus",
    "congue",
    "feugiat",
    "commodo",
    "velit",
    "egestas",
    "libero",
    "mollis",
    "quis",
    "hac",
    "habitasse",
    "platea",
    "dictumst",
    "Aliquam",
    "pulvinar",
    "mauris",
    "erat",
    "pretium",
    "a",
    "mattis",
    "non",
    "neque",
    "Maecenas",
    "massa",
    "venenatis",
    "aliquet",
    "risus",
    "Curabitur",
    "accumsan",
    "dui",
    "Morbi",
    "tellus",
    "lorem",
    "sapien",
    "dapibus",
    "Quisque",
    "tincidunt",
    "eros",
    "volutpat",
    "blandit",
    "augue",
    "pharetra",
    "quam",
    "eu",
    "odio",
    "maximus",
    "fermentum",
    "dictum",
    "consequat",
    "Integer",
    "tempus",
    "diam",
    "ac",
    "nisi",
    "lacinia",
    "justo",
    "iaculis",
    "molestie",
    "placerat",
    "dolor",
    "cursus",
    "consectetur",
    "viverra",
    "ornare",
    "faucibus",
    "vulputate",
    "nibh",
    "laoreet",
    "sit",
    "amet",
    "tortor",
    "Suspendisse",
    "potenti",
    "est",
    "ultrices",
    "tempor",
    "metus",
    "ex",
    "interdum",
    "Etiam",
    "porttitor",
    "condimentum",
    "sollicitudin",
    "eget",
    "ullamcorper",
    "Nullam",
    "posuere",
    "sodales",
    "vel",
    "sem",
    "sagittis",
    "mi",
    "rutrum",
    "Fusce",
    "vehicula",
    "Vivamus",
    "semper",
    "Aenean",
    "Duis",
    "lacus",
    "ultricies",
    "euismod",
    "adipiscing",
    "purus",
    "Proin",
    "rhoncus",
    "felis",
    "malesuada",
    "convallis",
    "dignissim",
    "fames",
    "ante",
    "primis",
    "urna",
    "tristique",
    "Cras",
    "lobortis",
    "elementum",
    "cubilia",
    "curae",
    "Phasellus",
    "Nam",
    "habitant",
    "senectus",
    "netus",
    "facilisi",
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]


class TextGenerator(BaseGenerator):

    def __init__(self, seed: int = None, **kargs):
        super().__init__(seed, **kargs)

    @property
    def default_params(self) -> Dict[str, Any]:
        return dict(length=100, allowed_values=None, const=None)

    def validate_params(self, params):
        assert_types(int, params["length"])
        assert_types(list, params["allowed_values"])
        if params["allowed_values"]:
            assert_types(str, *params["allowed_values"])
        assert_types(str, params["const"])

        if params["length"]:
            assert_gt(params["length"], 0, 'Param "length" must be a positive number')

    def generate(self) -> str:
        if self._params["const"]:
            return self._params["const"]

        if self._params["allowed_values"]:
            return self._rd.choice(self._params["allowed_values"])

        length = self._params["length"]
        cur_len = 0
        chosen_words = []
        while cur_len < length:
            chosen = self._rd.choice(LOREM_IPSUM_WORDS)
            chosen_words.append(chosen)
            cur_len += len(chosen) + 1

        return " ".join(chosen_words)

    def generate_by_dialect(self, dialect: str) -> str:
        if dialect == "name":
            return self._faker.name()
        if dialect == "first_name":
            return self._faker.first_name()
        if dialect == "last_name":
            return self._faker.last_name()
        if dialect == "middle_name":
            return self._faker.middle_name()
        if dialect == "address":
            return self._faker.address()
        if dialect == "address_detail":
            return self._faker.address_detail()
        if dialect == "road_address":
            return self._faker.road_address()
        if dialect == "street_address":
            return self._faker.street_address()
        if dialect == "city":
            return self._faker.city()
        if dialect == "phone_number":
            return self._faker.phone_number()
        if dialect == "company":
            return self._faker.company()
        if dialect == "country":
            return self._faker.country()
        if dialect == "province":
            return self._faker.province()
        if dialect == "district":
            return self._faker.district()
        if dialect == "credit_card_number":
            return self._faker.credit_card_number()
        if dialect == "color_name":
            return self._faker.color_name()
        if dialect == "language_name":
            return self._faker.language_name()
        else:
            raise ValueError(f"Dialect {dialect} has not been supported in text generator")
