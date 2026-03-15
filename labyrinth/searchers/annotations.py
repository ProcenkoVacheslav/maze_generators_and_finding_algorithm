from collections import namedtuple
from typing import Literal

Names = Literal['dfs', 'bfs', 'lee']
Position = namedtuple('Position', ['x', 'y'])