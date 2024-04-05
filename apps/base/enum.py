from enum import Enum

class UserRol(Enum):
    CLIENT = 'client'
    SELLER = 'seller'
    ADMIN = 'admin'

    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)
    

class UserStep(Enum):
    SENT_EMAIL = 'sent_email'
    VERIFY_CODE = 'verify_code'
    COMPLATE = 'complate'

    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)


class Tariff(Enum):
    DEFAULT = 'default'
    SILVER = 'silver'
    GOLD = 'gold'
    PLATINUM = 'platinum'

    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)


class CommentType(Enum):
    NEW = 'new'
    REPLY = 'reply'

    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)

class ProductStatus(Enum):
    DRAFT = 'draft'
    BLOCK = 'block'
    PUBLISH = 'publish'

    @classmethod
    def choices(cls):
        return tuple((key.value, key.name) for key in cls)