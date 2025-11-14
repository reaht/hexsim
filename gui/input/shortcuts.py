# file: gui/input/shortcuts.py

def bind_shortcuts(root, state):
    root.bind("<Control-z>", lambda e: state.undo.undo(state))
    root.bind("<Control-y>", lambda e: state.undo.redo(state))
    root.bind("<Control-Z>", lambda e: state.undo.undo(state))
    root.bind("<Control-Y>", lambda e: state.undo.redo(state))