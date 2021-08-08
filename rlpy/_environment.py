from copy import deepcopy
from itertools import product
from random import choice, choices

from rlpy._action import Action
from rlpy._cell import Cell
from rlpy._state import State


class Environment:
    """Class for environment where an agent move around."""

    def __init__(
        self,
        grid: list[list[Cell]],
        move_probability: float = 0.8,
        default_reward: float = -0.04,
    ):
        """Initialize environment where an agent move around.

        Parameters
        ----------
        grid : list[list[Cell]]
            Grid of 2d list of cells.
        move_probability : float, optional
            Probability that an agent can move toward its desired direction,
            by default 0.8
        default_reward : float, optional
            Default reward an agent receives each move.
        """
        self._grid = grid
        self._move_probability = move_probability
        self._default_reward = default_reward

        self._agent_state = State()

    @property
    def grid(self) -> list[list[Cell]]:
        """Return grid of 2d list of cells.

        Returns
        -------
        list[list[Cell]]
            Grid of 2d list of cells.
        """
        return deepcopy(self._grid)

    @property
    def num_rows(self) -> int:
        """Return number of rows of the grid.

        Returns
        -------
        int
            Number of rows of the grid.
        """
        return len(self._grid)

    @property
    def num_cols(self) -> int:
        """Return number of cols of the grid.

        Returns
        -------
        int
            Number of cols of the grid.
        """
        return len(self._grid[0])

    @property
    def possible_actions(self) -> list[Action]:
        """Return list of possible actions an agent can take.

        Returns
        -------
        list[Action]
            Possible actions an agent can take.
        """
        return [
            Action.UP,
            Action.DOWN,
            Action.LEFT,
            Action.RIGHT,
        ]

    @property
    def possible_states(self) -> list[State]:
        """Return list of possible states an agent can take.

        Returns
        -------
        list[State]
            Possible states an agent can take.
        """
        return [
            State(r, c) for r, c
            in product(range(self.num_rows), range(self.num_cols))
            if self._grid[r][c] != Cell.BLOCK
        ]

    def reset(self) -> State:
        """Reset an agent state and return its state.

        Returns
        -------
        State
            Initial state of an agent.
        """
        self._agent_state = State(self.num_rows - 1, 0)
        return self._agent_state.clone()

    def transition_function(
        self,
        state: State,
        action: Action,
    ) -> dict[State, float]:
        """Return probability to each state an agent can transition to.

        Parameters
        ----------
        state : State
            Current state of an agent.
        action : Action
            An action an agent take.

        Returns
        -------
        dict[State, float]
            Probability to each state an agent can transition to.
        """
        if not self.can_act_at(state):
            return {}  # No state to transition to.

        transition_probability = {}
        opposite_action = Action(tuple(a * -1 for a in action.value))
        for a in self.possible_actions:
            if a == action:
                probability = self._move_probability
            elif a != opposite_action:
                probability = (1 - self._move_probability) * 0.5
            else:
                probability = 0.

            next_state = self._move(state, action)
            if next_state not in transition_probability:
                transition_probability[next_state] = probability
            else:
                transition_probability[next_state] += probability
        return transition_probability

    def can_act_at(self, state: State) -> bool:
        """Return true if an agent can take action at the given state.

        Parameters
        ----------
        state : State
            State of an agent.

        Returns
        -------
        bool
            True if an agent can take action at the state, otherwise false.
        """
        return self._grid[state.row][state.col] == Cell.NORMAL

    def _is_inside_of_grid(self, state: State) -> bool:
        if state.row < 0:
            return False
        if state.row >= self.num_rows:
            return False
        if state.col < 0:
            return False
        if state.col >= self.num_cols:
            return False
        return True

    def _move(self, state: State, action: Action) -> State:
        if not self.can_act_at(state):
            raise Exception(f'Cannot move from {state}')

        next_state = state.act(action)
        if not self._is_inside_of_grid(next_state):
            next_state = state.clone()
        if self._grid[next_state.row][next_state.col] == Cell.BLOCK:
            next_state = state.clone()
        return next_state

    def reward_function(self, state: State) -> float:
        """Return reward an agent receives at the given state.

        Parameters
        ----------
        state : State
            State of an agent.

        Returns
        -------
        float
            Reward an agent receives at the state.
        """
        cell = self._grid[state.row][state.col]
        if cell == Cell.REWARD:
            return 1.
        if cell == Cell.DAMAGE:
            return -1.
        return self._default_reward

    def is_game_end(self, state: State) -> bool:
        """Return true if the game has come to an end otherwise false.

        Parameters
        ----------
        state : State
            State of an agent.

        Returns
        -------
        bool
            True if the game has come to an end otherwise false.
        """
        cell = self._grid[state.row][state.col]
        return cell in (Cell.REWARD, Cell.DAMAGE)

    def step(self, action: Action) -> tuple[State, float, bool]:
        """Move an agent give an action.

        Parameters
        ----------
        action : Action
            An action an agent want to take.

        Returns
        -------
        tuple[State, float, bool]
            - Next state of an agent after move.
            - Reward an agent receives.
            - Flag whether the game has come to an end.
        """
        next_state, reward, is_game_end = self._transit(
            self._agent_state, action)
        if next_state is not None:
            self._agent_state = next_state.clone()
        return next_state, reward, is_game_end

    def _transit(
        self,
        state: State,
        action: Action,
    ) -> tuple[State, float, bool]:
        transition_probability = self.transition_function(state, action)
        if len(transition_probability) == 0:
            return None, None, True
        next_states = []
        probabilities = []
        for state, probability in transition_probability.items():
            next_states.append(state)
            probabilities.append(probability)
        next_state = choices(next_states, weights=probabilities)[0]
        reward = self.reward_function(next_state)
        is_game_end = self.is_game_end(next_state)
        return next_state, reward, is_game_end


if __name__ == '__main__':
    class Agent:
        """Agent class."""

        def __init__(self, env) -> None:
            """Initialize an agent."""
            self._possible_actions = env.possible_actions

        def policy(self, state: State) -> Action:
            """Return an agent action according to its policy."""
            return choice(self._possible_actions)

    grid = [
        [Cell.NORMAL, Cell.NORMAL, Cell.NORMAL, Cell.REWARD],
        [Cell.NORMAL,  Cell.BLOCK, Cell.NORMAL, Cell.DAMAGE],
        [Cell.NORMAL, Cell.NORMAL, Cell.NORMAL, Cell.NORMAL],
    ]
    env = Environment(grid)
    agent = Agent(env)

    for i in range(10):
        state = env.reset()
        total_reward = 0.
        done = False

        while not done:
            action = agent.policy(state)
            next_state, reward, done = env.step(action)
            total_reward += reward
            state = next_state.clone()

        print(f"Episode {i:2d}, Agent gets {total_reward} reward")
