# file: gui/undo_manager.py

from core.command import Command, CompositeCommand


class UndoManager:
    """
    GUI-scoped undo stack.
    Replaces the old core.undo_stack.UndoStack so that
    GUI tools and interaction are properly encapsulated.
    """

    def __init__(self):
        self.past = []
        self.future = []
        self.current_transaction = None

    # -------------------------
    # Transaction support
    # -------------------------

    def begin(self):
        if self.current_transaction is None:
            self.current_transaction = []

    def add(self, cmd: Command):
        if self.current_transaction is not None:
            self.current_transaction.append(cmd)
        else:
            # Immediate command application
            self.do(cmd, None)

    def commit(self, state):
        if self.current_transaction is None:
            return

        if len(self.current_transaction) == 1:
            cmd = self.current_transaction[0]
        else:
            cmd = CompositeCommand(self.current_transaction)

        self.current_transaction = None
        self.do(cmd, state)

    def rollback(self):
        self.current_transaction = None

    # -------------------------
    # Core undo/redo logic
    # -------------------------

    def do(self, cmd, state):
        """Execute a command and push onto undo history."""
        cmd.do(state)
        self.past.append(cmd)
        self.future.clear()

        # GUI redraw
        if state is not None:
            state.events.publish("grid_changed")

    def undo(self, state):
        if not self.past:
            return

        cmd = self.past.pop()
        cmd.undo(state)
        self.future.append(cmd)

        # GUI redraw
        state.events.publish("grid_changed")

    def redo(self, state):
        if not self.future:
            return

        cmd = self.future.pop()
        cmd.do(state)
        self.past.append(cmd)

        # GUI redraw
        state.events.publish("grid_changed")

    def clear(self):
        self.past.clear()
        self.future.clear()
        self.current_transaction = None