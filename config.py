from colors import *

players_config = {
    "players": {
        "player-1": {
            "index": 0,
            "base_color": RED,
            "piece_color": DARK_RED,
            "max_pieces": 4,
            "playing": True,
        },
        "player-2": {
            "index": 1,
            "base_color": BLUE,
            "piece_color": DARK_BLUE,
            "max_pieces": 4,
            "playing": True,
        },
        "player-3": {
            "index": 2,
            "base_color": ORANGE,
            "piece_color": DARK_ORANGE,
            "max_pieces": 4,
            "playing": True,
        },
        "player-4": {
            "index": 3,
            "base_color": GREEN,
            "piece_color": DARK_GREEN,
            "max_pieces": 4,
            "playing": True,
        },
    }
}

is_piece_moving = False
mouse_clicked = False
change_to_button_cursor = False
