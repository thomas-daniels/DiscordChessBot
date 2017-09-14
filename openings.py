"""Load and retrieve chess openings."""

import json
import re
import chess
import chess.pgn

class Opening():
    """A chess opening, wih ECO code, name, FEN and moves in the UCI format."""
    def __init__(self, eco, name, fen, uci):
        self.eco = eco
        self.name = name
        self.fen = fen
        self.uci = uci

    def as_pgn_moves(self):
        """Gets the PGN representation of the UCI moves."""
        board = chess.Board()
        for move in self.uci.split(" "):
            board.push_uci(move)
        exporter = chess.pgn.StringExporter(headers=False, comments=False)

        return chess.pgn.Game().from_board(board).accept(exporter).strip(" *")

    def distance(self, search):
        """Calculates the distance between this opening's name and a search query."""
        search = search.upper()
        this = self.name.upper()

        if search == this or search == self.eco:
            return 0

        only_alpha_search = re.sub("[^A-Z ]", "", search)
        only_alpha_this = re.sub("[^A-Z ]", "", this)
        if only_alpha_search == only_alpha_this:
            return 0

        only_alpha_search_words = list(filter(None, only_alpha_search.split(" ")))
        only_alpha_this_words = list(filter(None, only_alpha_this.split(" ")))
        if sorted(only_alpha_search_words) == sorted(only_alpha_this_words):
            return 0.1

        if only_alpha_search in only_alpha_this:
            return 0.2

        same_words = 0
        for search_word in only_alpha_search_words:
            if search_word in only_alpha_this_words:
                same_words += 1
            if search_word in only_alpha_this:
                same_words += 0.75
        if same_words == 0:
            return 10
        return 1 + 1.0 / same_words

class Openings():
    """Collection of chess openings."""
    def __init__(self, path):
        with open(path, "r") as file_obj:
            openings = json.load(file_obj)
        self._openings = []
        for opening in openings:
            self._openings.append(Opening(opening["c"], opening["n"], opening["f"], opening["m"]))

    def closest_match(self, requested):
        """Finds the opening that's the closest match for the requested one."""
        if requested == "":
            return None

        result = sorted(
            self._openings, key=lambda x: x.distance(requested)
        )
        if result[0].distance(requested) == 10:
            return None
        return result[0]
