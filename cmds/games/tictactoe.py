import random
import asyncio


EMPTY_BOARD = (None, None, None, None, None, None, None, None, None)
PLAYERS = (':x:', ':o:')
CACHED_MOVES = {
    ':x:': {
        (None, None, None, None, None, None, None, None, None):
            ((None, None, None, None, ':x:', None, None, None, None), None),
        (':o:', None, None, None, None, None, None, None, None):
            ((':o:', None, None, None, ':x:', None, None, None, None), None),
        (None, ':o:', None, None, None, None, None, None, None):
            ((':x:', ':o:', None, None, None, None, None, None, None), None),
        (None, None, ':o:', None, None, None, None, None, None):
            ((None, None, ':o:', None, ':x:', None, None, None, None), None),
        (None, None, None, ':o:', None, None, None, None, None):
            ((':x:', None, None, ':o:', None, None, None, None, None), None),
        (None, None, None, None, ':o:', None, None, None, None):
            ((':x:', None, None, None, ':o:', None, None, None, None), None),
        (None, None, None, None, None, ':o:', None, None, None):
            ((None, None, ':x:', None, None, ':o:', None, None, None), None),
        (None, None, None, None, None, None, ':o:', None, None):
            ((None, None, None, None, ':x:', None, ':o:', None, None), None),
        (None, None, None, None, None, None, None, ':o:', None):
            ((None, ':x:', None, None, None, None, None, ':o:', None), None),
        (None, None, None, None, None, None, None, None, ':o:'):
            ((':x:', None, None, None, None, None, None, None, ':o:'), None),
    },
    ':o:': {
        (None, None, None, None, None, None, None, None, None):
            ((None, None, None, None, ':o:', None, None, None, None), None),
        (':x:', None, None, None, None, None, None, None, None):
            ((':x:', None, None, None, ':o:', None, None, None, None), None),
        (None, ':x:', None, None, None, None, None, None, None):
            ((':o:', ':x:', None, None, None, None, None, None, None), None),
        (None, None, ':x:', None, None, None, None, None, None):
            ((None, None, ':x:', None, ':o:', None, None, None, None), None),
        (None, None, None, ':x:', None, None, None, None, None):
            ((':o:', None, None, ':x:', None, None, None, None, None), None),
        (None, None, None, None, ':x:', None, None, None, None):
            ((':o:', None, None, None, ':x:', None, None, None, None), None),
        (None, None, None, None, None, ':x:', None, None, None):
            ((None, None, ':o:', None, None, ':x:', None, None, None), None),
        (None, None, None, None, None, None, ':x:', None, None):
            ((None, None, None, None, ':o:', None, ':x:', None, None), None),
        (None, None, None, None, None, None, None, ':x:', None):
            ((None, ':o:', None, None, None, None, None, ':x:', None), None),
        (None, None, None, None, None, None, None, None, ':x:'):
            ((':o:', None, None, None, None, None, None, None, ':x:'), None),
    },
}

board_index = lambda col, row: row * 3 + col
index_to_col_row = lambda idx: (idx % 3, idx // 3)
opponent = lambda player: ':o:' if player == ':x:' else ':x:'
get_available_moves = lambda board: [index_to_col_row(idx) for idx, item in enumerate(board) if item is None]


class IllegalMove(Exception):
    pass


class IllegalBoard(Exception):
    pass


def play(board, player, col, row):
    if not board_is_valid(board):
        raise IllegalBoard
    if not 0 <= col <= 2 or not 0 <= row <= 2 or player not in PLAYERS or board[board_index(col, row)] is not None:
        raise IllegalMove
    board = board[0:board_index(col, row)] + (player,) + board[board_index(col, row) + 1:]
    return board, board_winner(board)


def board_is_valid(board):
    if len(board) != 9:
        return False

    for mark in board:
        if mark is not None and mark not in PLAYERS:
            return False

    return True


def board_winner(board):
    if not board_is_valid(board):
        raise IllegalBoard

    for row in range(0, 3):
        if board[board_index(0, row)] == board[board_index(1, row)] == board[board_index(2, row)]:
            return board[board_index(0, row)]

    for col in range(0, 3):
        if board[board_index(col, 0)] == board[board_index(col, 1)] == board[board_index(col, 2)]:
            return board[board_index(col, 0)]

    if board[board_index(0, 0)] == board[board_index(1, 1)] == board[board_index(2, 2)] or \
            board[board_index(2, 0)] == board[board_index(1, 1)] == board[board_index(0, 2)]:
        return board[board_index(1, 1)]

    if None not in board:
        return 'T'

    return None


def minimax(board, player):
    return _minimax(board, player, player, 0)


def _minimax(board, active_player, turn_player, depth):
    scores = []
    moves = []

    available_moves = get_available_moves(board)
    for available_move in available_moves:
        next_board, next_winner = play(board, turn_player, *available_move)
        if next_winner is not None:
            scores.append(_minimax_score(next_winner, active_player, depth + 1))
        else:
            scores.append(_minimax(next_board, active_player, opponent(turn_player), depth + 1))
        moves.append(available_move)

    if depth == 0:
        return moves[scores.index(max(scores))]
    elif active_player == turn_player:
        return max(scores)
    else:
        return min(scores)


def _minimax_score(winner, active_player, depth):
    if winner == active_player:
        return 10 - depth
    elif winner == 'T':
        return 0
    else:
        return depth - 10


def play_random_move(board, player):
    move = random.choice(get_available_moves(board))
    return play(board, player, *move)


def play_best_move(board, player):
    if board in CACHED_MOVES[player]:
        return CACHED_MOVES[player][board]
    return play(board, player, *minimax(board, player))


def get_printable_board(board):
    if not board_is_valid(board):
        raise IllegalBoard

    output = '**'
    for row in range(0, 3):
        for col in range(0, 3):
            mark = board[board_index(col, row)]
            if mark is None:
                output += '      '
            else:
                output += mark

            if col != 2:
                output += '|'

        if row != 2:
            output += '**\n**-+-+-+-+-+-**\n**'
    output += '**'
    return output

async def play_game(bot, ctx, chance_for_error=0.0):
    def check(m):
        return m.author == ctx.author

    board, winner = EMPTY_BOARD, None
    await ctx.send("輸入由逗號分隔的行和列編號`,`")
    await ctx.send("e.g.: 輸入由逗號分隔的行和列編號`1,2` 即在第一行第二列。\n`exit` 以結束遊戲")
    smsg = await ctx.send(get_printable_board(board))
    while winner is None:
        await smsg.edit(content=get_printable_board(board))
        while True:
            try:
                msg  = await bot.wait_for('message', check=check, timeout=20.0)
                if msg.content == 'exit':
                    await ctx.send("已退出")
                    return
                row, col = msg.content.split(',')
                col, row = int(col) - 1, int(row) - 1
                board, winner = play(board, ':x:', col, row)
                break
            except (IllegalMove, ValueError):
                await ctx.send("這是被禁止的行為！", delete_after=1.0)
                await msg.delete()
            except KeyboardInterrupt:
                return
            except asyncio.TimeoutError:
                await ctx.send("你花的時間太久了 :hourglass:")
                await smsg.delete()
                return

        if winner is None:
            if random.random() < chance_for_error:
                board, winner = play_random_move(board, ':o:')
            else:
                board, winner = play_best_move(board, ':o:')
        try:
            await msg.delete()
        except Exception:
            continue
    await smsg.delete()
    await ctx.send(get_printable_board(board))
    if winner == 'T':
        await ctx.send("**平手！ :ribbon:**")
    elif winner == ':o:':
        await ctx.send('**我贏了! :robot:**')
    else:
        await ctx.send('**你贏了! :trophy:**')