"""Tests for ChessBot."""

import openings

def test_openings():
    """Tests the openings module."""
    ops = openings.Openings("eco/eco.json")
    selected = ops.closest_match("kingspawn")
    assert selected.name == "King's Pawn"
    assert selected.eco == "B00"
    assert selected.uci == "e2e4"
    assert selected.fen == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq"
