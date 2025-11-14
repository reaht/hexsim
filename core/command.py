# file: core/command.py

class Command:
    """Base command."""
    def do(self, state):
        raise NotImplementedError

    def undo(self, state):
        raise NotImplementedError


class CompositeCommand(Command):
    """A group of commands, used for drag operations."""
    def __init__(self, commands):
        self.commands = commands

    def do(self, state):
        for c in self.commands:
            c.do(state)

    def undo(self, state):
        # Undo in reverse order
        for c in reversed(self.commands):
            c.undo(state)


class ChangeBiomeCommand(Command):
    """Change biome on a single hex."""
    def __init__(self, coord, old_biome, new_biome):
        self.coord = coord
        self.old = old_biome
        self.new = new_biome

    def do(self, state):
        state.grid.set_biome(self.coord, self.new)
        state.events.publish("tile_changed", self.coord)
        state.events.publish("grid_changed")

    def undo(self, state):
        state.grid.set_biome(self.coord, self.old)
        state.events.publish("tile_changed", self.coord)
        state.events.publish("grid_changed")


class SetTrailCommand(Command):
    """Set or clear a specific trail direction for a tile."""
    def __init__(self, coord, direction, old_value, new_value):
        self.coord = coord
        self.direction = direction
        self.old = old_value
        self.new = new_value

    def do(self, state):
        state.grid.set_trail(self.coord, self.direction, self.new)
        state.events.publish("trail_changed", self.coord, self.direction)
        state.events.publish("grid_changed")

    def undo(self, state):
        state.grid.set_trail(self.coord, self.direction, self.old)
        state.events.publish("trail_changed", self.coord, self.direction)
        state.events.publish("grid_changed")


class MovePartyCommand(Command):
    """Undoable party movement."""
    def __init__(self, old_pos, new_pos):
        self.old = old_pos
        self.new = new_pos

    def do(self, state):
        state.party.position = self.new
        state.events.publish("party_moved", self.new)
        state.events.publish("grid_changed")

    def undo(self, state):
        state.party.position = self.old
        state.events.publish("party_moved", self.old)
        state.events.publish("grid_changed")