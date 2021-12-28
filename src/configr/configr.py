import json
import pathlib
from typing import Any, Optional, List, MutableMapping

import toml
import xmltodict
import yaml


def _get_parts_(key: str, separator: Optional[str] = ".") -> List[str]:
    if key is None or not isinstance(key, str):
        raise ValueError("Invalid key!")
    return key.split(separator)


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
        if root_key:
            self.__config__ = self.__getitem__(root_key)
            self.__root_key__ = root_key

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise ValueError("Key must be of type string.")

        parts: List[str] = _get_parts_(key, self.__separator__)
        current: dict = self.__config__
        for part in parts:
            if part not in current:
                raise Exception(f"Key does not exist in configuration at {self.path}.")
            current = current[part]
        return current

    def __contains__(self, key: str) -> bool:
        if not isinstance(key, str):
            raise ValueError("Key must be of type string.")

        parts: List[str] = _get_parts_(key, self.__separator__)
        current: dict = self.__config__
        for part in parts:
            if part not in current:
                return False
            current = current[part]
        return True
