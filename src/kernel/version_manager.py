"""
AI Architecture Studio
Kernel - Version Manager

Foundation 1.7
"""


class VersionManager:
    APP_NAME = "AI Architecture Studio"

    MAJOR = 0
    MINOR = 5
    PATCH = 0

    CODENAME = "Foundation"

    @classmethod
    def version(cls):
        return f"{cls.MAJOR}.{cls.MINOR}.{cls.PATCH}"

    @classmethod
    def full_version(cls):
        return f"{cls.APP_NAME} {cls.version()} ({cls.CODENAME})"

    @classmethod
    def build_string(cls):
        return (
            f"{cls.APP_NAME}\n"
            f"Version: {cls.version()}\n"
            f"Codename: {cls.CODENAME}"
        )