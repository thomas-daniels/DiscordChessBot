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

    amar_gambit = ops.closest_match("Amar Gambit")
    assert amar_gambit.as_pgn_moves() == "1. Nh3 d5 2. g3 e5 3. f4 Bxh3 4. Bxh3 exf4"
