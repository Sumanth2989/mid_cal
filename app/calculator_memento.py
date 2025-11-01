from copy import deepcopy

class Memento:
    def __init__(self, state):
        self._state = deepcopy(state)
    def get_state(self):
        return deepcopy(self._state)

class Caretaker:
    def __init__(self):
        self._undo = []
        self._redo = []

    def snapshot(self, state):
        self._undo.append(Memento(state))
        self._redo.clear()

    def undo(self, current_state):
        if not self._undo: return current_state, False
        self._redo.append(Memento(current_state))
        m = self._undo.pop()
        return m.get_state(), True

    def redo(self, current_state):
        if not self._redo: return current_state, False
        self._undo.append(Memento(current_state))
        m = self._redo.pop()
        return m.get_state(), True
