from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self) -> None:
        self.tracker = ArrayStack(10000)
        self.undone = ArrayStack(10000)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Complexity: O(1)
        """
        if not self.tracker.is_full():
            self.tracker.push(action)
            self.undone.clear()
        return None

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        Complexity: O(1)
        """
        if not self.tracker.is_empty():
            action = self.tracker.pop()
            action.undo_apply(grid)
            self.undone.push(action)
            return action
        return None
    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        Complexity: O(1)
        """
        if not self.undone.is_empty():
            action = self.undone.pop()
            action.redo_apply(grid)
            self.tracker.push(action)
            return action
        return None
if __name__ == "__main__":
    x = PaintAction()
