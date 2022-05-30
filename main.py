# -*- coding: utf-8 -*-
from sokoban.functional import *
import inspect as i


init_state = """  %%%%% 
%%%   % 
%bpc  % 
%%% cb% 
%b%%c % 
% % b %%
%c vccb%
%   b  %
%%%%%%%%
"""

init_state_simple = """%%%%
%p %
%c %
%b %
%%%%
"""

init_state_simple_2 = """%%%%%
%p  %
%ccb%
%b  %
%%%%%
"""

if __name__ == "__main__":
    state = load_from_string(init_state)
    sol = solve_bfs(state, debug=True)

    print(save_to_string(state))
    for action in sol:
        state = execute(state, action)
        print(save_to_string(state))
