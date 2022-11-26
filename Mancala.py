# Author: August Frisk
# GitHub username: @4N0NYM0U5MY7H
# Date: 2022, November 22
# Description: This program is loosely based on the U.S. commercial version of Mancala
#              game rules and mechanics.
#
# Mancala games rules are derived from the description created by Alycia Zimmerman.
# Mancala Rules:
# Zimmerman, A. (n.d.). Mancala Rules.
#     https://github.com/osu-cs162-f22/portfolio-4N0NYM0U5MY7H/blob/main/mancala_rules.pdf


class Player:
    """Represents a Player with a name."""

    def __init__(self, name=str):
        """Creates a Player with a name."""
        self._name = name

    def get_name(self):
        """Returns a Player name."""
        return self._name

    def set_name(self, name=str):
        """Sets a Player name."""
        self._name = name


class Game:
    """Represents a Game with a name and number of players."""

    def __init__(self, name=str, number_of_players=1):
        """Creates a Game with a name and number of players."""
        self._name = name
        self._number_of_players = number_of_players

    def get_name(self):
        """Returns a Game Name."""
        return self._name

    def set_name(self, name=str):
        """Sets the name of a game."""
        self._name = name

    def get_number_of_players(self):
        """Returns the number of Players in a game."""
        return self._number_of_players

    def set_number_of_players(self, number_of_players=int):
        """Sets the number of Players in a game."""
        self._number_of_players = number_of_players


class Mancala(Game):
    """Represents the U.S. commercial version of Mancala game rules and mechanics."""

    def __init__(self, name="Mancala", number_of_players=2):
        """"""
        super().__init__(name, number_of_players)
        self._players = []
        self._initial_seed_count = 4

        self._player_2_pits = ('L', 'K', 'J', 'I', 'H', 'G')
        self._player_1_pits = ('A', 'B', 'C', 'D', 'E', 'F')

        self._player_pit_id = self.get_player_pit_id()  # key: value {1-12: A-L}
        self._next_pit = self.get_next_pit()            # key: value {pit: next pit}
        self._opposite_pit = self.get_opposite_pit()    # key: value {p1 pit: p2 pit}
        self._game_board = self.get_new_board()         # key: value {pit: num of seeds}

    def create_player(self, name=""):
        """Creates a Mancala Player with a name."""
        player_name = name

        if player_name == "":
            if len(self._players) < 1:
                player_name = "Player 1"
                new_player = Player(player_name)
            if len(self._players) == 1:
                player_name = "Player 2"
                new_player = Player(player_name)

        new_player = Player(player_name)
        self._players.append(new_player)

    def print_board(self):
        """Prints the current state of the board to the screen."""
        player_1_seeds = []
        for pit in self._player_1_pits:
            seeds_in_pit = str(self._game_board[pit])
            player_1_seeds.append(seeds_in_pit)

        print(f"player1:\n store: {self._game_board['1']}\n {player_1_seeds}")

        player_2_seeds = []
        for pit in self._player_2_pits:
            seeds_in_pit = str(self._game_board[pit])
            player_2_seeds.append(seeds_in_pit)

        print(f"player2:\n store: {self._game_board['2']}\n {player_2_seeds}")

    def return_winner(self):
        """
        Returns the winner of Mancala if the Game has ended, determined by the number of
        seeds in the Player's stores.
        """
        if self.game_has_ended() is False:
            return "Game has not ended"

        if self._game_board['1'] > self._game_board['2']:
            return f"Winner is player 1: {self._players[0].get_name()}"

        if self._game_board['2'] > self._game_board['1']:
            return f"Winner is player 2: {self._players[1].get_name()}"
        else:
            return "It's a tie"

    def play_game(self, player_turn, player_pit):
        """"""
        if player_pit > 6 or player_pit <= 0:
            return "Invalid number for pit index"

        if self.game_has_ended() is True:
            return "Game is ended"

        if player_turn == 2:
            player_pit += 6                             # adjust pit index for player 2

        current_pit = self._player_pit_id[player_pit]   # get the current pit
        seeds_to_sow = self._game_board[current_pit]    # get the number of seeds
        self._game_board[current_pit] = 0               # empty pit into "hand"

        while seeds_to_sow > 0:
            current_pit = self._next_pit[current_pit]   # get the next pit
            if (player_turn == 1 and current_pit == '2') \
                    or (player_turn == 2 and current_pit == '1'):
                continue                                # skip over opponent's store
            self._game_board[current_pit] += 1          # place 1 seed in pit
            seeds_to_sow -= 1                           # remove seed from "hand"

        #                                               Special Rule #1
        if current_pit == str(player_turn) == '1':      # if player 1 ends in store 1
            print("player 1 take another turn")
        if current_pit == str(player_turn) == '2':      # if player 2 ends in store 2
            print("player 2 take another turn")

        #                                                            Special Rule #2
        if player_turn == 1 and current_pit in self._player_1_pits \
                and self._game_board[current_pit] == 1:              # player 1 ends in an empty
            #                                                          player 1 pit
            self._game_board['1'] += self._game_board[current_pit]   # add seed to player 1 store
            self._game_board[current_pit] = 0                        # empty current pit

            opposite_pit = self._opposite_pit[current_pit]           # get opposite pit
            self._game_board['1'] += self._game_board[opposite_pit]  # add seeds to player 1 store
            self._game_board[opposite_pit] = 0                       # empty opposite pit

        elif player_turn == 2 and current_pit in self._player_2_pits \
                and self._game_board[current_pit] == 2:              # player 2 ends in an empty
            #                                                          player 2 pit
            self._game_board['2'] += self._game_board[current_pit]   # add seed to player 2 store
            self._game_board[current_pit] = 0                        # empty current pit

            opposite_pit = self._opposite_pit[current_pit]           # get opposite pit
            self._game_board['2'] += self._game_board[opposite_pit]  # add seeds to player 2 store
            self._game_board[opposite_pit] = 0                       # empty opposite pit

        self.game_has_ended()
        current_game_state = []
        for key, value in self._game_board.items():
            current_game_state.append(value)

        return f"{current_game_state}"

    def get_player_pit_id(self):
        """
        Represents player selected pits.
        Returns a dictionary whose keys are an integer 1-12 and values are a letter A-L.
        """
        return {
            1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F',
            7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L'
        }

    def get_next_pit(self):
        """Returns a dictionary whose keys pits and values are the next pit."""
        return {
            'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'G', 'G': 'H', 'H': 'I', 'I': 'J', 'J': 'K', 'K': 'L',
            'L': '2', '2': 'A'
        }

    def get_opposite_pit(self):
        """Returns a dictionary whose keys are pits and values the opposite pit."""
        return {
            'A': 'L', 'B': 'K', 'C': 'J', 'D': 'I', 'E': 'H', 'F': 'G',
            'G': 'F', 'H': 'E', 'I': 'D', 'J': 'C', 'K': 'B', 'L': 'A'
        }

    def get_new_board(self):
        """Returns the initial state of the Mancala board."""
        seeds = self._initial_seed_count
        return {
            'A': seeds, 'B': seeds, 'C': seeds, 'D': seeds, 'E': seeds, 'F': seeds, '1': 0,
            'G': seeds, 'H': seeds, 'I': seeds, 'J': seeds, 'K': seeds, 'L': seeds, '2': 0
        }

    def game_has_ended(self):
        """Returns whether the game has ended or not."""
        seeds_in_player_1_pits = 0
        seeds_in_player_2_pits = 0

        for pit in self._player_1_pits:
            seeds_in_player_1_pits += self._game_board[pit]

        for pit in self._player_2_pits:
            seeds_in_player_2_pits += self._game_board[pit]

        if seeds_in_player_1_pits == 0:
            self._game_board['2'] += seeds_in_player_2_pits
            for pit in self._player_2_pits:
                self._game_board[pit] = 0
            return True

        elif seeds_in_player_2_pits == 0:
            self._game_board['1'] += seeds_in_player_1_pits
            for pit in self._player_1_pits:
                self._game_board[pit] = 0
            return True

        else:
            return False


if __name__ == "__main__":

    game = Mancala()
    player1 = game.create_player("Lily")
    player2 = game.create_player("Lucy")
    print(game.play_game(1, 3))
    game.play_game(1, 1)
    game.play_game(2, 3)
    game.play_game(2, 4)
    game.play_game(1, 2)
    game.play_game(2, 2)
    game.play_game(1, 1)
    game.print_board()
    print(game.return_winner()) 

    game = Mancala()
    player1 = game.create_player("Lily")
    player2 = game.create_player("Lucy")
    print(game.play_game(1, 1))
    print(game.play_game(1, 2))
    print(game.play_game(1, 3))
    print(game.play_game(1, 4))
    print(game.play_game(1, 5))
    print(game.play_game(1, 6))
    game.print_board()
    print(game.return_winner())