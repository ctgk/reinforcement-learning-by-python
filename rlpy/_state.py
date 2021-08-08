from __future__ import annotations

from rlpy._action import Action


class State:
    """Class for an agent state."""

    def __init__(self, row: int = -1, col: int = -1):
        """Initialize an agent state.

        Parameters
        ----------
        row : int, optional
            Row-axis of location of an agent, by default -1
        col : int, optional
            Col-axis of location of an agent, by default -1
        """
        self._row = row
        self._col = col

    @property
    def row(self) -> int:
        """Return row-axis of an agent location.

        Returns
        -------
        int
            Row-axis of an agent location.
        """
        return self._row

    @property
    def col(self) -> int:
        """Return col-axis of an agent location.

        Returns
        -------
        int
            Col-axis of an agent location.
        """
        return self._col

    def __repr__(self) -> str:
        """Return representation of an agent state.

        Returns
        -------
        str
            Representation of an agent state.
        """
        return f'<State: [r={self.row}, c={self.col}]>'

    def clone(self) -> State:
        """Return clone of the agent state.

        Returns
        -------
        State
            Clone of the agent state.
        """
        return State(self.row, self.col)

    def __hash__(self) -> int:
        """Return hash value of the agent state.

        Returns
        -------
        int
            Hash value of the agent state.
        """
        return hash((self._row, self._col))

    def act(self, action: Action) -> State:
        """Act an agent given an action and return its next state.

        Parameters
        ----------
        action : Action
            Action an agent take.

        Returns
        -------
        State
            Next state of the agent after action.
        """
        return State(
            *tuple(
                p + a for p, a
                in zip((self.row, self.col), action.value)
            ),
        )
