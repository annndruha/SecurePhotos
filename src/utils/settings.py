import json
import os


class DBJsonFile:
    def __init__(self):
        self.filename = os.path.join(os.path.expanduser("~"), '.SecurePhotos', 'config.json')
        self._version = 'v1'
        self._load()

    def _load_defaults(self):
        self.store = {
            "action_rotate_left": True,
            "action_rotate_right": True,
            "action_delete": True,
            "action_fit_view": True,
            "action_fullscreen": True,
            "action_encrypt_decrypt": True,
            "copy_to_target": False,
        }

    def _load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                try:
                    self.store = json.load(f)[self._version]
                except KeyError:
                    self._load_defaults()
                except json.JSONDecodeError:
                    self._load_defaults()
        else:
            self._load_defaults()

    def _save(self):
        dirs, filename = os.path.split(self.filename)
        os.makedirs(dirs, exist_ok=True)
        with open(self.filename, "w", encoding="utf-8") as f:
            v_store = {self._version: self.store}
            json.dump(v_store, f, indent=4, ensure_ascii=False)

    def __getitem__(self, key: str):
        key = str(key)
        if key not in self.store:
            return False
        return self.store[key]

    def __setitem__(self, key: str, value):
        key = str(key)
        self.store[key] = value
        self._save()

    def __delitem__(self, key: str):
        key = str(key)
        if key in self.store:
            del self.store[key]
            self._save()

    def __contains__(self, key: str):
        key = str(key)
        return key in self.store

    def keys(self):
        return self.store.keys()

    def values(self):
        return self.store.values()

    def items(self):
        return self.store.items()

    def get(self, key: str, default=None):
        key = str(key)
        if key not in self.store:
            return False
        return self.store.get(key, default)

    def pop(self, key: str, default=None):
        key = str(key)
        value = self.store.pop(key, default)
        self._save()
        return value

    def clear(self):
        self.store.clear()
        self._save()

    def __repr__(self):
        return repr(self.store)
