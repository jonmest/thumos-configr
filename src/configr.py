import json
import pathlib
from typing import Any, Optional, List, MutableMapping

import toml
import xmltodict
import yaml


def _get_parts_(root_key: str, key: str, separator: Optional[str] = ".") -> List[str]:
    if root_key is None and key is not None:
        return key.split(separator)
    if root_key is not None and key is None:
        return root_key.split(separator)
    if root_key is None and key is None:
        return []

    root_parts: List[str] = root_key.split(separator)
    key_parts: List[str] = key.split(separator)
    return root_parts + key_parts


class Configr:
    __config__: dict
    __separator__: str
    __root_key__: str

    def __init__(self, path: str, root_key: Optional[str] = None, separator: Optional[str] = "."):
        extension: str = pathlib.Path(path).suffix
        with open(path, "r") as file:
            if extension == ".yaml" or extension == ".yml":
                self.__config__ = yaml.load(file, Loader=yaml.FullLoader)
            if extension == ".json":
                self.__config__ = json.load(file)
            if extension == ".toml":
                self.__config__: MutableMapping = toml.load(file)
            if extension == ".xml":
                self.__config__ = xmltodict.parse(file.read())
        self.path = path
        self.__separator__ = separator
        self.__root_key__ = root_key

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise ValueError("Key must be of type string.")

        parts: List[str] = _get_parts_(self.__root_key__, key, self.__separator__)
        current: dict = self.__config__
        for part in parts:
            if part not in current:
                raise Exception(f"Key does not exist in configuration at {self.path}.")
            current = current[part]
        return current

    def __contains__(self, key: str) -> bool:
        if not isinstance(key, str):
            raise ValueError("Key must be of type string.")

        parts: List[str] = _get_parts_(self.__root_key__, key, self.__separator__)
        current: dict = self.__config__
        for part in parts:
            if part not in current:
                return False
            current = current[part]
        return True
