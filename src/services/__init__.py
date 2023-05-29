import json
from pyparsing import MutableMapping

from src.utils import get_build_directory


class StateMixin:
    def __init__(self):
        self._state = None

    @property
    def state(self) -> MutableMapping:
        if self._state is None:
            self._state = json.load(open(get_build_directory() / 'state.json', "r"))
        return self._state
    
    @property
    def state(self) -> MutableMapping:
        if self._state is None:
            self._state = json.load(open(get_build_directory() / 'state.json', "r"))
        return self._state
    
    @property
    def metadata(self) -> MutableMapping:
        return self.state["metadata"]
    

    def dump_state(self) -> None:
        """
        Dumps state to json file lacated in directory where build is
        """
        import json
        with open(get_build_directory() / 'state.json', 'w') as f:
            json.dump(self.state, f, indent=4, ensure_ascii=False)
