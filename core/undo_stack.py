# file: core/undo_stack.py

from core.command import Command, CompositeCommand


class UndoStack:
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
            self.do(cmd, None)   # state supplied later

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
        """Execute a command and push to undo stack."""
        cmd.do(state)
        self.past.append(cmd)
        self.future.clear()

    def undo(self, state):
        if not self.past:
            return
        cmd = self.past.pop()
        cmd.undo(state)
        self.future.append(cmd)

    def redo(self, state):
        if not self.future:
            return
        cmd = self.future.pop()
        cmd.do(state)
        self.past.append(cmd)

    def clear(self):
        self.past.clear()
        self.future.clear()
        self.current_transaction = None