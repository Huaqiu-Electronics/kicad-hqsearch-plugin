from pcbnew import GetBoard, LoadBoard
import wx
import os


class EmptyBoardException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BoardManager:
    def __init__(self, board) -> None:
        if board is None:
            raise EmptyBoardException("Empty kicad board")
        self._board = board

    @property
    def board(self):
        return self._board


def load_board_manager():
    try:
        GetBoard().GetFileName()
        board = GetBoard()
        if board:
            return BoardManager(board)
    except Exception as e:
        for fp in   ('C:\\Program Files\\demos\\flat_hierarchy\\flat_hierarchy.kicad_pcb',
                     'C:\\Program Files\\demos\\amulet_controller\\amulet_controller.kicad_pcb',
                    #  "C:\\Program Files\\demos\\video\\video.kicad_pcb",
                         ):
            if os.path.exists(fp):
                return BoardManager(LoadBoard(fp))
