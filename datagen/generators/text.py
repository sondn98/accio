from typing import List, Optional, Literal
from pydantic import BaseModel, model_validator

from utils.assertions import assert_gt
from datagen.generators.base import Generator


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


class TextConfig(BaseModel):
    type: Literal["text"]
    max_length: int = 100
    nullable: Optional[bool] = False
    unique: Optional[bool] = False
    allowed_values: List[str] = None
    const: Optional[str] = None
    dialect: Optional[str] = None

    @model_validator(mode="after")
    def validate_params(self):
        if self.max_length:
            assert_gt(self.max_length, 0, 'Param "max_length" must be a positive number')
        return self


class TextGenerator(Generator):

    def generate(self) -> str:
        cfg = self._cfg
        if not cfg.dialect:
            if cfg.const:
                return cfg.const

            if cfg.allowed_values:
                return self._rd.choice(cfg.allowed_values)

            max_length = cfg.max_length
            cur_len = 0
            chosen_words = []
            while True:
                chosen = self._rd.choice(LOREM_IPSUM_WORDS)
                if cur_len + len(chosen) > max_length:
                    break
                chosen_words.append(chosen)
                cur_len += len(chosen) + 1

            return " ".join(chosen_words)
        if cfg.dialect == "name":
            return self._faker.name()
        if cfg.dialect == "first_name":
            return self._faker.first_name()
        if cfg.dialect == "last_name":
            return self._faker.last_name()
        if cfg.dialect == "middle_name":
            return self._faker.middle_name()
        if cfg.dialect == "address":
            return self._faker.address()
        if cfg.dialect == "address_detail":
            return self._faker.address_detail()
        if cfg.dialect == "road_address":
            return self._faker.road_address()
        if cfg.dialect == "street_address":
            return self._faker.street_address()
        if cfg.dialect == "city":
            return self._faker.city()
        if cfg.dialect == "phone_number":
            return self._faker.phone_number()
        if cfg.dialect == "company":
            return self._faker.company()
        if cfg.dialect == "country":
            return self._faker.country()
        if cfg.dialect == "province":
            return self._faker.province()
        if cfg.dialect == "district":
            return self._faker.district()
        if cfg.dialect == "credit_card_number":
            return self._faker.credit_card_number()
        if cfg.dialect == "color_name":
            return self._faker.color_name()
        if cfg.dialect == "language_name":
            return self._faker.language_name()
        else:
            raise ValueError(f"Dialect {cfg.dialect} has not been supported in text generator")
