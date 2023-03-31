from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    MAX_ACTIONS = 10000

    def __init__(self) -> None:
        """
        Instantiates instance variables:

        self.tracker: an Array Stack with the size of MAX_ACTIONS
        self.undone: an Array Stack with the size of MAX_ACTIONS

        Complexity: O(n)
        n: MAX_ACTIONS
        """

        self.tracker = ArrayStack(self.MAX_ACTIONS)
        self.undone = ArrayStack(self.MAX_ACTIONS)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.

        Complexity: O(1)
        """
        if not self.tracker.is_full(): # If it's not full add a new action to the tracker
            self.tracker.push(action)
            self.undone.clear() # Clear undone so we can't redo actions after we undo then paint 
        return None

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        Complexity: O(nm . special) 
        Case when action done is special
        n: The horizontal length of the grid
        m: The vertical length of the grid
        Special because the time complexity may differ depending on the type of layer store
        """
        if not self.tracker.is_empty(): # Check whether there's any actions to undo
            action = self.tracker.pop()
            action.undo_apply(grid) # Undo the action
            self.undone.push(action) # Add the action to self.undone so we can redo it later on
            return action
        return None
    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        Complexity: O(nm . special) 
        Case when action done is special
        n: The horizontal length of the grid
        m: The vertical length of the grid
        Special because the time complexity may differ depending on the type of layer store

        """
        if not self.undone.is_empty(): # Check whether there are any actions to redo
            action = self.undone.pop() 
            action.redo_apply(grid) # Redo the action
            self.tracker.push(action) # Add the action to the tracker
            return action
        return None
if __name__ == "__main__":
    x = PaintAction()