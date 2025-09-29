from typing import Dict, Set


class BiDict:
    """A bidirectional dictionary allowing lookups from key to value and value to key."""

    def __init__(self, **kwargs: str) -> None:
        self._dictionary: dict[str, str] = {}
        self._keys: set[str] = set()
        self._values: set[str] = set()
        for key, value in kwargs.items():
            self[key] = value

    def __setitem__(self, key: str, value: str) -> None:
        if key in self._dictionary or value in self._dictionary.values():
            raise ValueError(
                f"Duplicate key or value: {key}, {value}. To update, delete first."
            )
        if key == value:
            raise ValueError(f"The key and value cannot be the same: {key}")
        self._dictionary[key] = value
        self._dictionary[value] = key
        self._keys.add(key)
        self._values.add(value)

    def __getitem__(self, key: str) -> str:
        return self._dictionary[key]

    def __delitem__(self, key: str) -> None:
        self._keys.remove(key)
        self._values.remove(self._dictionary[key])
        del self._dictionary[self._dictionary[key]]
        del self._dictionary[key]

    def __len__(self) -> int:
        return len(self._dictionary) // 2

    def __contains__(self, key: str) -> bool:
        return key in self._dictionary

    def keys(self) -> set[str]:
        """
        Get the set of keys in the dictionary.

        Returns:
            The set of keys in the dictionary.
        """
        return self._keys

    def values(self) -> set[str]:
        """
        Get the set of values in the dictionary.

        Returns:
            The set of values in the dictionary.
        """
        return self._values

    def items(self) -> dict[str, str]:
        """
        Get the dictionary items (key-value pairs) in the dictionary.

        Returns:
            A dictionary containing the items in the dictionary.
        """
        return {k: v for k, v in self._dictionary.items() if k in self._keys}

    def __str__(self) -> str:
        return str({k: v for k, v in self._dictionary.items() if k in self._keys})
