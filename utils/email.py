import re


class Email:
    pattern = r""

    @classmethod
    def is_valid(cls, email: str) -> bool:
        if re.fullmatch(cls.pattern, email):
            return True
        return False

    @classmethod
    def is_email(cls, string: str) -> bool:
        return cls.is_valid(string)
