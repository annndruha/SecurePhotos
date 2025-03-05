import json
import os.path

# TODO: NOT DONE
class KeyValueDataBase(dict):
    def __init__(self):
        super().__init__()
        self.file_path = os.path.join(os.path.expanduser("~"), '.SecurePhotos', 'config.json')
        self.data: dict = {}

        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self._dump_to_disk()

    def is_key_exists(self, key) -> bool:
        return str(key) in self.data.keys()

    def __getitem__(self, key) -> str | None:
        if str(key) not in self.data.keys():
            return None
        return self.data[str(key)]

    def __setitem__(self, _id, token) -> None:
        assert isinstance(_id, int | str)
        assert isinstance(token, str)
        self.data[str(_id)] = token
        self._dump_to_disk()

    def __delitem__ (self, _id) -> None:
        if str(_id) in self.data.keys():
            del self.data[str(_id)]
            self._dump_to_disk()

    def _dump_to_disk(self):
        dirs, filename = os.path.split(self.file_path)
        os.makedirs(dirs, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)