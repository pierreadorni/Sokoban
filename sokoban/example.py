# -*- coding: utf-8 -*-
""" Example usage of the Sokoban MVC """

from Sokoban.State import State
from Sokoban.Sokoban import Sokoban
from Sokoban.Visualizer import Visualizer


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

if __name__ == '__main__':
    sokoban = Sokoban(initial_state=State(init_state))
    sokoban.execute('DhddbbbbgBDhhhhGGGdbDBdbbgGbggHHbD')
    Visualizer(sokoban).show_history()