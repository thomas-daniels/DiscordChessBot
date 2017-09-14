"""Tests for ChessBot."""

import commands
import openings

def test_openings():
    """Tests the openings module."""
    ops = openings.Openings("eco/eco.json")
    selected = ops.closest_match("kings pawn")
    assert selected.name == "King's Pawn"
    assert selected.eco == "B00"
    assert selected.uci == "e2e4"
    assert selected.fen == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq"

    amar_gambit = ops.closest_match("Amar Gambit")
    assert amar_gambit.as_pgn_moves() == "1. Nh3 d5 2. g3 e5 3. f4 Bxh3 4. Bxh3 exf4"


def test_commands():
    """Tests the commands module."""
    cmds = commands.Commands()
    assert cmds.opening("kings pawn") == \
        "**B00 King's Pawn**. Moves: `1. e4`. " \
        "Board: <https://lichess.org/analysis/rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR_b_KQkq>"

    assert cmds.opening("king pawn nimzowitsch defense wheeler gambit") == \
        cmds.execute("opening King's Pawn Game: Nimzowitsch Defense: Wheeler Gambit")
