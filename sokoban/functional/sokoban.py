""" functional programming version of the Sokoban solver"""
from typing import Set, Tuple, Callable, NamedTuple, Dict, Optional, List
import inspect as i


class PreconditionUnmetException(Exception):
    """Custom Exception thrown when an action with an unmet precondition was going to be executed"""

    pass


class NoSolutionException(Exception):
    """Custom Exception thrown when there is no solution for a given state"""

    pass


Position = Tuple[int, int]
PositionCollection = Tuple[Position]
State = NamedTuple(
    "State",
    [
        ("walls", PositionCollection),
        ("goals", PositionCollection),
        ("crates", PositionCollection),
        ("hero", Position),
        ("map_size", Tuple[int, int]),
    ],
)
PreCondition = Callable[[State], bool]
PostCondition = Callable[[State], State]
Action = NamedTuple(
    "Action",
    [("preconditions", Set[PreCondition]), ("postconditions", List[PostCondition])],
)


def left(pos: Position) -> Position:
    """returns the position on the left of the given position"""
    return pos[0] - 1, pos[1]


def right(pos: Position) -> Position:
    """returns the position on the right of the given position"""
    return pos[0] + 1, pos[1]


def top(pos: Position) -> Position:
    """returns the position on top of the given position"""
    return pos[0], pos[1] - 1


def bottom(pos: Position) -> Position:
    """returns the position on the bottom of the given position"""
    return pos[0], pos[1] + 1


def move_crate(state: State, old_pos: Position, new_pos: Position):
    """returns a new state in which the crate at pos old_pos has been moved to new_pos"""
    new_crates = tuple(
        (x, y) if (x, y) != old_pos else new_pos for x, y in state.crates
    )
    new_state = State._make(
        [state.walls, state.goals, new_crates, state.hero, state.map_size]
    )
    return new_state


def move_hero(state: State, pos: Position):
    """returns a new state in which the hero has been moved to position pos"""
    new_state = State._make(
        [state.walls, state.goals, state.crates, pos, state.map_size]
    )
    return new_state


move_left = Action(
    {
        lambda state: left(state.hero) not in state.walls,
        lambda state: left(state.hero) not in state.crates,
    },
    [
        lambda state: move_hero(state, left(state.hero)),
    ],
)

move_right = Action(
    {
        lambda state: right(state.hero) not in state.walls,
        lambda state: right(state.hero) not in state.crates,
    },
    [
        lambda state: move_hero(state, right(state.hero)),
    ],
)

move_up = Action(
    {
        lambda state: top(state.hero) not in state.walls,
        lambda state: top(state.hero) not in state.crates,
    },
    [
        lambda state: move_hero(state, top(state.hero)),
    ],
)

move_down = Action(
    {
        lambda state: bottom(state.hero) not in state.walls,
        lambda state: bottom(state.hero) not in state.crates,
    },
    [
        lambda state: move_hero(state, bottom(state.hero)),
    ],
)

push_left = Action(
    {
        lambda state: left(state.hero) in state.crates,
        lambda state: left(left(state.hero)) not in state.walls,
        lambda state: left(left(state.hero)) not in state.crates,
    },
    [
        lambda state: move_crate(state, left(state.hero), left(left(state.hero))),
        lambda state: move_hero(state, left(state.hero)),
    ],
)

push_right = Action(
    {
        lambda state: right(state.hero) in state.crates,
        lambda state: right(right(state.hero)) not in state.walls,
        lambda state: right(right(state.hero)) not in state.crates,
    },
    [
        lambda state: move_crate(state, right(state.hero), right(right(state.hero))),
        lambda state: move_hero(state, right(state.hero)),
    ],
)

push_up = Action(
    {
        lambda state: top(state.hero) in state.crates,
        lambda state: top(top(state.hero)) not in state.walls,
        lambda state: top(top(state.hero)) not in state.crates,
    },
    [
        lambda state: move_crate(state, top(state.hero), top(top(state.hero))),
        lambda state: move_hero(state, top(state.hero)),
    ],
)

push_down = Action(
    {
        lambda state: bottom(state.hero) in state.crates,
        lambda state: bottom(bottom(state.hero)) not in state.walls,
        lambda state: bottom(bottom(state.hero)) not in state.crates,
    },
    [
        lambda state: move_crate(state, bottom(state.hero), bottom(bottom(state.hero))),
        lambda state: move_hero(state, bottom(state.hero)),
    ],
)

actions = [
    move_left,
    move_right,
    move_up,
    move_down,
    push_left,
    push_right,
    push_up,
    push_down,
]


def is_win(state: State) -> bool:
    """Returns True if all crates are on a goal, False otherwise"""
    for crate in state.crates:
        if crate not in state.goals:
            return False
    return True


def load_from_string(state_string: str) -> State:
    """Charge un état à partir d'une chaîne de caractères"""
    murs, buts, caisses, personnage_pos = set(), set(), set(), (0, 0)
    lines = [line for line in state_string.split("\n") if line != ""]
    w, h = len(lines[0]), len(lines)
    for y in range(h):
        for x in range(w):
            if lines[y][x] == "%":
                murs.add((x, y))
            elif lines[y][x] == "b":
                buts.add((x, y))
            elif lines[y][x] == "c":
                caisses.add((x, y))
            elif lines[y][x] == "p":
                personnage_pos = (x, y)
            elif lines[y][x] == "v":
                buts.add((x, y))
                caisses.add((x, y))
            elif lines[y][x] == "q":
                personnage_pos = (x, y)
                buts.add((x, y))
    return State(tuple(murs), tuple(buts), tuple(caisses), personnage_pos, (w, h))


def save_to_string(state: State) -> str:
    """Sauvegarde un état sous forme d'une chaîne de caractères"""
    text = ""
    for y in range(state.map_size[1]):
        line = ""
        for x in range(state.map_size[0]):
            if (x, y) == state.hero and (x, y) in state.goals:
                line += "q"
            elif (x, y) in state.crates and (x, y) in state.goals:
                line += "v"
            elif (x, y) == state.hero:
                line += "p"
            elif (x, y) in state.crates:
                line += "c"
            elif (x, y) in state.goals:
                line += "b"
            elif (x, y) in state.walls:
                line += "%"
            else:
                line += " "
        text += line + "\n"
    return text


def execute(state: State, action: Action) -> State:
    """returns a new state onto which the specified action has been executed"""
    new_state = State._make(state)
    for precondition in action.preconditions:
        if not precondition(new_state):
            raise PreconditionUnmetException(i.getsource(precondition))
    for postcondition in action.postconditions:
        new_state = postcondition(new_state)
    return new_state


def build_path(
    initial_state: State,
    current_state: State,
    precedents: Dict[State, Optional[Tuple[Action, State]]],
):
    """Builds a path from the current state to the initial state"""
    path = []
    while current_state != initial_state:
        action, state = precedents[current_state]
        path.append(action)
        current_state = state
    return path[::-1]


def solve_bfs(state: State, max_depth=0, debug=False) -> List[Action]:
    """returns a list of actions that solve the specified state"""
    queue = [(state, 0)]  # store the current depth of the search
    initial_state = state
    precedents: Dict[State, Optional[Tuple[Action, State]]] = {state: None}
    if debug:
        print("[i] Start of Breadth-First Search")
        i = 0
    while queue and (max_depth == 0 or queue[0][1] < max_depth):
        current_state, current_depth = queue.pop(0)
        if debug:
            print(f"\r[i] {i} states traversed", end="")
            i += 1
        if is_win(current_state):
            return build_path(initial_state, current_state, precedents)
        for action in actions:
            try:
                new_state = execute(current_state, action)
            except PreconditionUnmetException:
                continue
            if new_state not in precedents:
                queue.append((new_state, current_depth + 1))
                precedents[new_state] = (action, current_state)
    raise NoSolutionException()


def solve_iterative_deepening(state: State, max_depth=40, debug=False) -> List[Action]:
    """returns a list of actions that solve the specified state"""
    if debug:
        print("[i] Start of iterative deepening uninformed search")
    for depth in range(1, max_depth):
        if debug:
            print("\r[-] Depth:", depth, end="")
        try:
            solution = solve_bfs(state, depth)
            return solution
        except NoSolutionException:
            continue
    raise NoSolutionException()
