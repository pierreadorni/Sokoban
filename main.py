# -*- coding: utf-8 -*-
from sokoban import State
from sokoban import Sokoban
from sokoban import Visualizer

# a state is represented as a string of the following characters:
# '#' : a wall
# ' ' : a floor
# 'p' : the hero
# 'c' : a crate
# 'b' : a goal
# 'v' : a crate on a goal
# 'q' : the hero on a goal
# each line is separated by a newline character
init_state = \
"""  %%%%% 
%%%   % 
%bpc  % 
%%% cb% 
%b%%c % 
% % b %%
%c vccb%
%   b  %
%%%%%%%%
"""

if __name__ == '__main__':
    sokoban = Sokoban(initial_state=State(init_state))
    sokoban.execute('DhddbbbbgBDhhhhGGGdbDBdbbgGbggHHbD')
    Visualizer(sokoban).show_history()
