import json
import os

from jsonconfig.utils import system_path


class JSONConfig(object):
    """
    Singleton that stores and retrieves JSON format config files and config objects.
    """

    __configs = {}
    DEFAULT_NAME = 'DEFAULT'

    @classmethod
    def config(cls, name=None, path=None):
        """
        Returns, and possibly create with a storage path if provided, a named config object.

        :param name: optional string (will use the default if omitted)
        :param path: optional string (will be an in-memory config object until a path is given)
        """
        if name is None:
            name = cls.DEFAULT_NAME

        if name not in cls.__configs:
            cls.__configs[name] = cls.__JSONConfig(path)

        return cls.__configs[name]

    @classmethod
    def delete(cls, name):
        """
        Delete the named config object.

        :param name: string
        """
        del cls.__configs[name]

    @classmethod
    def names(cls):
        """
        Return the names of all config objects.
        """
        return cls.__configs.iterkeys()

    class __JSONConfig(object):
        """
        Config object that stores the data in JSON format.
        """

        def __init__(self, path):
            self.__path = None
            self.__json = {}

            if path:
                self.__set_path(path)
                self.load()

        def __set_path(self, path):
            self.__path = system_path(path)

        def get(self, key):
            """
            Get the value of a named config property.

            :param key: string
            """
            if key not in self.__json:
                raise ValueError('Key does not exist.')

            return self.__json[key]

        def set(self, key, value):
            """
            Set the value of a named config property.

            :param key: string
            :param value: * any data type or object * (that can be converted to json format)
            """
            self.__json[key] = value

        def keys(self):
            """
            Returns the config keys as a generator.
            """
            return self.__json.iterkeys()

        def load(self, path=None):
            """
            Loads the config file from storage.

            :param path: optional string (will use stored value in self.__path if omitted)
            """
            if not (path and self.__path and (os.path.exists(path) or os.path.exists(self.__path))):
                raise IOError('Path does not exist or is not set.')
            elif path and os.path.exists(path):
                self.__set_path(path)

            with open(self.__path, 'rb') as json_file:
                self.__json = json.load(json_file)

        def save(self, path=None):
            """
            Saves the config file to storage.

            :param path: optional string (will use stored value in self.__path if omitted)
            """
            if not (self.__json and self.__path):
                raise IOError('Empty config data or invalid path.')

            if path:
                self.__set_path(path)

            if not os.path.exists(self.__path):
                os.makedirs(os.path.dirname(self.__path))

            with open(self.__path, 'wb') as json_file:
                json_file.write(json.dumps(self.__json))

        def defaults(self, default_json):
            """
            Set the defaults for the config.

            :param default_json: dict
            """
            for key, value in default_json.iteritems():
                if key not in self.__json:
                    self.__json[key] = value

        def path(self, path=None):
            """
            Set or return the stored path in self.__path

            :param path: optional string (will return stored value in self.__path if omitted)
            """
            if not path:
                return self.__path

            self.__set_path(path)
