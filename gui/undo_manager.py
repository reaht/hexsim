# file: gui/undo_manager.py

from core.command import Command, CompositeCommand

class UndoManager:
    """
    GUI-level undo manager with command transactions.
    Tools expect:
        - begin()
        - add(cmd)
        - commit(state)
        - undo(state)
        - redo(state)
    """

    def __init__(self):
        self.past = []
        self.future = []
        self.current_transaction = None

    # ---------------------------------------------------------
    # Transactions
    # ---------------------------------------------------------
    def begin(self):
        if self.current_transaction is None:
            self.current_transaction = []

    def add(self, cmd: Command):
        """Collect a command or execute immediately if not in a transaction."""
        if self.current_transaction is not None:
            self.current_transaction.append(cmd)
        else:
            # Immediate do
            self.do(cmd, None)

    def commit(self, state):
        if self.current_transaction is None:
            return

        # single or composite
        if len(self.current_transaction) == 1:
            cmd = self.current_transaction[0]
        else:
            cmd = CompositeCommand(self.current_transaction)

        self.current_transaction = None
        self.do(cmd, state)

    def rollback(self):
        """Drop changes made during drag before commit."""
        self.current_transaction = None

    # ---------------------------------------------------------
    # Core undo/redo
    # ---------------------------------------------------------
    def do(self, cmd, state):
        cmd.do(state)
        self.past.append(cmd)
        self.future.clear()

        if state:
            state.events.publish("grid_changed")

    def undo(self, state):
        if not self.past:
            return

        cmd = self.past.pop()
        cmd.undo(state)
        self.future.append(cmd)

        state.events.publish("grid_changed")

    def redo(self, state):
        if not self.future:
            return

        cmd = self.future.pop()
        cmd.do(state)
        self.past.append(cmd)

        state.events.publish("grid_changed")

    def clear(self):
        self.past.clear()
        self.future.clear()
        self.current_transaction = None