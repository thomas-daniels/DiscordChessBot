"""Load and retrieve chess openings."""

import json
import pylev

class Opening():
    """A chess opening, wih ECO code, name, FEN and moves in the UCI format."""
    def __init__(self, eco, name, fen, uci):
        self.eco = eco
        self.name = name
        self.fen = fen
        self.uci = uci

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
            self._openings, key=lambda x: pylev.levenshtein(x.name.upper(), requested.upper())
        )[0]
