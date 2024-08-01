from enum import Enum

class LinkedinLinks(Enum):
    BASE = "https://www.linkedin.com"
    LOGIN = "login"
    SEARCH_JOB = "jobs"

    @classmethod
    def get_url(cls, link):
        return f"{cls.BASE.value}/{link.value}"