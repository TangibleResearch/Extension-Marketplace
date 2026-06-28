"""Helpers for creating Tangible Research extensions."""

__all__ = ["ExtensionSpec", "create_extension"]


def __getattr__(name: str):
    if name in __all__:
        from .creator import ExtensionSpec, create_extension

        return {"ExtensionSpec": ExtensionSpec, "create_extension": create_extension}[name]
    raise AttributeError(name)
