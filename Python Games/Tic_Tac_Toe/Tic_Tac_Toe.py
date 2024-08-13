import os

def clear_screen():
    os.system("cls")

class Player :
    def __init__(self):
        self.name = ""
        self.symbol = ""

    def choose_name(self):
        while True : 
            # player_number = int (input ("Player : "))
            # if player_number == 1 :
            #     print ("\n------------------------------------------------------------------------------------------------------------------------")
            #     print ("Player" , player_number) 
            # if player_number == 2 :
            #     print ("\n------------------------------------------------------------------------------------------------------------------------")
            #     print ("Player" , player_number) 
            name = input("\nEnter your name : ")
            if name.isalpha() :
                self.name = name
                break
            print("\nYou Enter Invalid Name")

    def choose_symbol(self):
        while True :
            symbol = input("\nEnter your Symbol : ")
            if symbol.isalpha() and len(symbol) == 1 :
                self.symbol = symbol.upper()
                break
            print("\nYou Enter Invalid Symbol")

class Menu :
    def game_menu(self):
        print("X-O Game")
        print("1.Start Game")
        print("2.Quit Game")
        choice = input("Enter Your Choice : ")
        return choice
        
    def end_game_menu(self):
        print("1.Restart Game")
        print("2.Quit Game")
        choice = input("Enter Your Choice : ")
        return choice
class Board : 
    def __init__(self):
        self.board = [' ' for _ in range(1,10)]

    def display_board(self):
        for i in range(0,9,3) : 
            row = [f" {self.board[j]} " for j in range(i, i + 3)]
            print ("|".join(row))
            if i < 6 :
              print ("-"*11)
    
    def update_board(self , choice , symbol):
        if self.is_valid_move(choice) :
            self.board[choice-1] = symbol
            return True
        return False

    def is_valid_move(self , choice):
        return self.board[choice-1] == ' ' 
    
    def reset_board(self):
        self.board = [' ' for _ in range(1,10)]      

class Game :
    def __init__(self):
        self.players = [Player() , Player()]
        self.board = Board()
        self.menu = Menu()
        self.current_player_index = 0

    def start_game(self):
        choice = self.menu.game_menu()
        if choice == '1' :
            self.setup_players()
            self.play_game()
        else:
            self.quit_game()
        
    def setup_players(self):
        for number , player in enumerate(self.players , start=1) :
            print ( "\n" , "-"*118 , f"Player {number}")
            player.choose_name()
            player.choose_symbol()
            clear_screen()
    
    def play_game(self):
        while True :
            self.play_turn()
            player = self.players[self.current_player_index - 1]
            if self.check_win() or self.check_draw() :
                if self.check_win() :
                    print ("-"*119 , f"{player.name} Win\n")
                if self.check_draw() :
                    print ("-"*119 , "Draw!\n")
                choice = self.menu.end_game_menu()
                if choice == '1' :
                   self.restart_game()
                else : 
                    self.quit_game()
                    break

    def play_turn(self):
        player = self.players[self.current_player_index]
        self.board.display_board()
        print (f"{player.name}'s Tuers ({player.symbol})")
        while True : 
            
         try :
            cell_choice = int (input ("Choose a Cell 1 - 9 : "))
            if 1<= cell_choice <=9 and self.board.update_board(cell_choice , player.symbol) :
                break
            else : 
                print ("Invalid Move , Try Again")
            
         except ValueError:
            print ("Please Enter a Number Between 1 and 9")
        self.switch_player()
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def check_win(self):
        win_compinations = [[0,1,2] , [3,4,5] , [6,7,8]
                           ,[0,3,6] , [1,4,7] , [2,5,8] , 
                            [0,4,8] ,[2,4,6] ]
        for compo in win_compinations :
            if self.board.board[compo[0]] == self.board.board[compo[1]] == self.board.board[compo[2]] and self.board.board[compo[0]] != ' ' :
                return True 
        return False
    def check_draw(self):
        win_compinations = [[0,1,2] , [3,4,5] , [6,7,8]
                           ,[0,3,6] , [1,4,7] , [2,5,8] , 
                            [0,4,8] ,[2,4,6] ]
        for compo in win_compinations :
            if self.board.board[compo[0]] == self.board.board[compo[1]] == self.board.board[compo[2]] and self.board.board[compo[0]] != ' ' :
                return False
                break
        return all (cell != ' ' and cell != win_compinations for cell in self.board.board)

    def restart_game(self):
        self.board.reset_board()
        self.current_player_index = 0
        self.play_game()

    def quit_game(self):
        print ("\n\nGame Ended :)\n\n")   

game = Game()
game.start_game()