def evaluate_game_state(game):
    return game.player_sods - game.computer_sods

def generate_moves(game):
    moves = []
    non_locked_buttons = [button for button in game.buttons if button not in game.locked_buttons]
    for button1 in non_locked_buttons:
        for button2 in non_locked_buttons:
            if button1 != button2:
                moves.append((button1, button2))
    return moves

def minimax(game, depth, maximizing_player):
    if depth == 0 or game.n - len(game.locked_buttons) < 2:
        return evaluate_game_state(game)

    if maximizing_player:
        max_eval = float('-inf')
        for move in generate_moves(game):
            game.selected_buttons = list(move)
            game.locked_buttons.extend(list(move))
            eval = minimax(game, depth - 1, False)
            max_eval = max(max_eval, eval)
            game.selected_buttons.clear()
            game.locked_buttons = game.locked_buttons[:-2]
        return max_eval
    else:
        min_eval = float('inf')
        for move in generate_moves(game):
            game.selected_buttons = list(move)
            game.locked_buttons.extend(list(move))
            eval = minimax(game, depth - 1, True)
            min_eval = min(min_eval, eval)
            game.selected_buttons.clear()
            game.locked_buttons = game.locked_buttons[:-2]
        return min_eval

def get_best_move(game):
    best_score = float('-inf')
    best_move = None
    for move in generate_moves(game):
        game.selected_buttons = list(move)
        game.locked_buttons.extend(list(move))
        eval = minimax(game, 3, False)
        if eval > best_score:
            best_score = eval
            best_move = move
        game.selected_buttons.clear()
        game.locked_buttons = game.locked_buttons[:-2]
    return best_move