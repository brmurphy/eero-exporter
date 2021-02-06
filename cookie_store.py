from yaml import load, dump, SafeDumper, SafeLoader
import eero


class CookieStore(eero.SessionStorage):
    def __init__(self, yaml_file):
        from os import path
        self.yaml_file = path.abspath(yaml_file)

        with open(self.yaml_file, 'r') as stream:
            try:
                res = load(stream, Loader=SafeLoader)
                self.__cookie = res['session']
            except IOError:
                self.__cookie = None

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, cookie):
        self.__cookie = cookie
        out = {'session': cookie}
        with open(self.yaml_file, 'w+') as f:
            f.write(dump(out, Dumper=SafeDumper))
