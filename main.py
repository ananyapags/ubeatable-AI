#This AI uses a game tree to map out all possibilities of a games, and uses the minimax algorithm to determine the best path through the tree
#the minimax algorithm was used instead of a "single shortest path" algo because it significanlty reduces time and space complexity
import math
import time


#building the node class of the gmae tree, each node represents a state in a tic tac toe game. In other words a state tree of every possible move

class node:

#each node will have a state, with a certain player at hand (either x or o)
  def __init__(self, board, player):
    self.board = board
    self.player = player
    self.score = 0
    #linking the current state of the game to all of the possible states that follow it
    self.children = []
    #a way to keep track of with of the follwoing children of the node is the optimal move for the computer to take
    self.best_child = None

    #add a child to the current node, what is a possible next move?
  def add_child(self, child):
    self.children.append(child)

#print function to allow for more fluid testing and code effiency  
  def print_board(self):
    print("  ", end = "")
    for i in range(len(self.board)):
      print(str(i) + " ", end = "")
    print()
    for i in range(len(self.board)):
      print(str(i) + " ", end = "")
      for j in range(len(self.board[i])):
        print(self.board[i][j] + " ", end = "")
      print()


  def check_win(self):
    # check each row for a winner
    if self.board[0][0] == self.board[0][1] == self.board[0][2] and self.board[0][0] != '-':
      return self.board[0][0], True
    elif self.board[1][0] == self.board[1][1] == self.board[1][2] and self.board[1][0] != '-' :
      return self.board[1][0], True
    elif self.board[2][0] == self.board[2][1] == self.board[2][2] and self.board[2][0] != '-':
      return self.board[2][0], True

    # check each column for a winner
    if self.board[0][0] == self.board[1][0] == self.board[2][0] and self.board[0][0] != '-':
      return self.board[0][0], True
    elif self.board[0][1] == self.board[1][1] == self.board[2][1] and self.board[0][1] != '-':
      return self.board[0][1], True
    elif self.board[0][2] == self.board[1][2] == self.board[2][2] and self.board[0][2] != '-':
      return self.board[0][2], True

    # check each diagonal for a winner
    if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '-':
      return self.board[0][0], True
    elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '-':
      return self.board[0][2], True

    # check for a draw (no winners and board is full)
    for row in self.board:
      for space in row:
        if space == "-":
          return None, False
    
    # game is a draw
    return "draw", True

    #below is the minimax algorithm:
    #works by recursivley assigning a score to each possible node in the tree, and building back up the tree to get teh score of a branch
  def set_best_child(self):
    winner, gameover = self.check_win()
    if gameover and winner == "O":
      self.score = 10
      self.best_child = None
      return
    
    elif gameover and winner == "X":
      self.score = -10
      self.best_child = None
      return

    elif winner == "draw":
      self.score = 0
      self.best_child = None
      return

    for child in self.children:
      child.set_best_child()

    best_child = None
    if self.player == "O":
      best_score = -math.inf
      for child in self.children:
        if child.score > best_score:
          best_score = child.score
          best_child = child
    elif self.player == "X":
      best_score = math.inf
      for child in self.children:
        if child.score < best_score:
          best_score = child.score
          best_child = child

    self.best_child = best_child
    self.score = best_score


class Tree:

  def __init__(self, rootNode):
    self.root = rootNode
    self.build_tree(self.root)#constucts the whole stte graph
    root.set_best_child()

    #make for an easier build tree function by allwoing to duplcate, rather than create from scratch
  def copy_board(self, board):
    new_board = []
    for i in range(len(board)):
      row = []
      for j in range(len(board[i])):
        row.append(board[i][j])
      new_board.append(row)
    return new_board

    #recusively build a tree by making copies of of the board and appending them as a child. Each child will be then be filled in with the next possible move for the game
  def build_tree(self, node):
    if node.check_win()[1] == True:
      return

    child_player = ""
    if node.player == "X":
      child_player = "O"
    else:
      child_player = "X"

    for i in range(len(node.board)):
      for j in range(len(node.board[i])):
        if node.board[i][j] == '-':
          copy = self.copy_board(node.board)
          copy[i][j] = node.player
          child = node(copy, child_player)
          node.add_child(child)

    for child in node.children:
      self.build_tree(child)

#game function
  def play_game(self):
    input("Welcome to the Tic Tac Toe AI Game, where you can play Tic Tac Toe against an unbeatable AI. You will be player 'X' and the computer with be player 'O'. Press Enter to start")
    curr = self.root
    print()
    curr.print_board()


    while True:
      print()
      print("It is now your turn.")

#building the user interactivness
      while True:
        row = int(input("Which row would you like to place your X? "))
        col = int(input("Which column would you like to place your X? "))
        if row < 0 or row > 2 or col < 0 or col > 2 or curr.board[row][col] != '-':
          print("Your row and column values are invalid. Please enter them again.")
        else:
          break
      
      for child in curr.children:
        if child.board[row][col] == curr.player:
          curr = child
          break

      print()
      curr.print_board()
        #making sure that the program understand stha the end of a tree is when a the check_win function discovers a win or tie
      winner, gameover = curr.check_win()
      if gameover:
        break

      print()
      print("Now it's the AI's turn!")
      time.sleep(1)
      curr = curr.best_child
      print()
      curr.print_board()
      winner, gameover = curr.check_win()
      if gameover:
        break

    print()
    if winner == "draw":
      print("Game Over! It was a draw!")
    elif winner == "X":
      print("Game over! You won!")
    else:
      print("Game over! The AI has won!")


#managing the board using a 3x3 matirx
start_board = [
  ['-', '-', '-'],
  ['-', '-', '-'],
  ['-', '-', '-']
]

#main gameplay
root = node(start_board, "X")
tree = Tree(root)
tree.play_game()