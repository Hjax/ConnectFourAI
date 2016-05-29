import math, copy
from sys import stderr, stdin, stdout
import numpy

class Root_Node:
    def __init__(self, setup=True):
        self.threats = []
        self.side_to_move = 1
        self.board = numpy.zeros((6,7),dtype=int)
        self.levels = [0 for x in range(0, 7)]
    def make_move(self, move):
        self.board[5 - self.levels[move]][move] = self.side_to_move
        self.levels[move] += 1
        self.side_to_move *= -1
    def legal_moves(self):
        return [x for x in range(0, 7) if self.levels[x] < 7]
    def was_winning_move(S, P, current_row_idx,current_col_idx):
        #****** Column Win ******
        current_col = S[:,current_col_idx]
        if np.count_nonzero(current_col) > 3:
            P_idx= np.where(current_col== P)[0]
            #if the difference between indexes are one, that means they are consecutive.
            #we need at least 4 consecutive index. So 3 Ture value
            is_idx_consecutive = sum(np.diff(P_idx)==1)>=3
            if is_idx_consecutive:
                return 1000 * self.side_to_move * -1

        #****** Column Win ****** 
        current_row = S[current_row_idx,:]
        if np.count_nonzero(current_row) > 3:
            P_idx= np.where(current_row== P)[0]
            is_idx_consecutive = sum(np.diff(P_idx)==1)>=3
            if is_idx_consecutive:
                return 1000 * self.side_to_move * -1

        #****** Diag Win ****** 
        offeset_from_diag = current_col_idx - current_row_idx
        current_diag = S.diagonal(offeset_from_diag)
        if np.count_nonzero(current_diag) > 3:
            P_idx= np.where(current_diag== P)[0]
            is_idx_consecutive = sum(np.diff(P_idx)==1)>=3
            if is_idx_consecutive:
                return 1000 * self.side_to_move * -1
        #****** off-Diag Win ****** 
        #here 1) reverse rows, 2)find new index, 3)find offest and proceed as diag
        reversed_rows = S[::-1,:] #1
        new_row_idx = row_size - 1 - current_row_idx #2
        offeset_from_diag = current_col_idx - new_row_idx #3
        current_off_diag = reversed_rows.diagonal(offeset_from_diag)
        if np.count_nonzero(current_off_diag) > 3:
            P_idx= np.where(current_off_diag== P)[0]
            is_idx_consecutive = sum(np.diff(P_idx)==1)>=3
            if is_idx_consecutive:
                return 1000 * self.side_to_move * -1
        
