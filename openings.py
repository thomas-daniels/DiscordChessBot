"""Load and retrieve chess openings."""

import json
import re
import pylev
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

        only_alpha_search_words = only_alpha_search.split(" ")
        only_alpha_this_words = only_alpha_this.split(" ")
        if sorted(only_alpha_search_words) == sorted(only_alpha_this_words):
            return 0.1

        if only_alpha_search in only_alpha_this:
            return 0.2

        return pylev.levenshtein(only_alpha_search, only_alpha_this)

class Openings():
    """Collection of chess openings."""
    def __init__(self, path):
        with open(path, "r") as f:
            openings = json.load(f)
        self._openings = []
        for opening in openings:
            self._openings.append(Opening(opening["c"], opening["n"], opening["f"], opening["m"]))

    def closest_match(self, requested):
        """Finds the opening that's the closest match for the requested one."""
        return sorted(
            self._openings, key=lambda x: x.distance(requested)
        )[0]
