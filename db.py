from tkinter import *
def tictactoe():
    theBoard = {'1': ' ' , '2': ' ' , '3': ' ' ,
                '4': ' ' , '5': ' ' , '6': ' ' ,
                '7': ' ' , '8': ' ' , '9': ' ' }

    board_keys = []  

    for key in theBoard:
        board_keys.append(key)
    
    def printBoard(board):
        print('\t' '\t     '+board['1'] + '\t|' +'      ' + board['2'] + '\t|' + '     ' +board['3'])
        print('\t' '\t--------------+------------+------------')
        print('\t' '\t     '+board['4'] + '\t|' +'      ' + board['5'] + '\t|' + '     ' +board['6'])
        print('\t''\t--------------+------------+------------')
        print('\t' '\t     '+board['7'] + '\t|' +'      ' + board['8'] + '\t|' + '     ' +board['9'])

    # Now we'll write the main function which has all the gameplay functionality.
    def game(win_x,win_o,player1,player2):

        turn = 'X'
        count = 0          # count turns


        for i in range(10):
            printBoard(theBoard)
            if(i!=9):
                print("It's your turn," + turn + ".Move to which place?")

            move = input()

            if theBoard[move] == ' ':
                theBoard[move] = turn
                count += 1
            else:
                print("That place is already filled.\nMove to which place?")
                continue

            # Now we will check if player X or O has won,for every move after 5 moves. 
            if count >= 5:
                if theBoard['7'] == theBoard['8'] == theBoard['9'] != ' ': # across the top
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['7']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")                
                    break
                elif theBoard['4'] == theBoard['5'] == theBoard['6'] != ' ': # across the middle
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['4']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['2'] == theBoard['3'] != ' ': # across the bottom
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['1']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['4'] == theBoard['7'] != ' ': # down the left side
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['4']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['2'] == theBoard['5'] == theBoard['8'] != ' ': # down the middle
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['5']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['3'] == theBoard['6'] == theBoard['9'] != ' ': # down the right side
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['6']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break 
                elif theBoard['7'] == theBoard['5'] == theBoard['3'] != ' ': # diagonal
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['3']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break
                elif theBoard['1'] == theBoard['5'] == theBoard['9'] != ' ': # diagonal
                    printBoard(theBoard)
                    print("\nGame Over.\n")
                    if(theBoard['9']=='X'):
                        win_x=win_x+1
                    else:
                        win_o=win_o+1
                    print(" **** " +turn + " won. ****")
                    break 

            # If neither X nor O wins and the board is full, we'll declare the result as 'tie'.
            if count == 9:
                print("\nGame Over.\n")                
                print("It's a Tie!!")

            # Now we have to change the player after every move.
            if turn =='X':
                turn = 'O'
            else:
                turn = 'X'        

        print("win_x",win_x)
        print("win_o",win_o)
        # Now we will ask if player wants to restart the game or not.
        restart = input("Do want to play Again?(y/n)")
        if restart == "y" or restart == "Y":  
              for key in board_keys:
                 theBoard[key] = " "
              game(win_x,win_o,player1,player2)
        elif restart=="n" or restart=="N":
            import mysql.connector as sql
            mydb=sql.connect(host="localhost",user="root",password="yash",database="information")
            cur=mydb.cursor()
            b="insert into tictactoe values(' "+player1+" ',' "+c1+" ',' " +str(win_x)+ " ')"
            cur.execute(b)
            c="insert into tictactoe values(' "+player2+" ',' "+c2+" ',' " +str(win_o)+ " ')"
            cur.execute(c)
            mydb.commit()
            print("succesfully entered the value in table")
        else:
            print("you entered wrong choice")
    win_x=0
    win_o=0
    c1="X"  
    c2="O" 
    #ENTER THE PLAYER NAME BY THE USER.
    player1=input("enter the name of player 1")
    player2=input("enter the name of player 2")
    print("THE CHARACTER OF PLAYER 1 IS X AND PLAYER 2 IS O")
    game(win_x,win_o,player1,player2)


#INFORMATION ABOUT THOSE WHO PLAYED THIS GAME AND HOW MANY TIME THEY WINS.
def information():
         import mysql.connector as sql
         mydb=sql.connect(host="localhost",user="root",password="yash",database="information")
         cur=mydb.cursor()
         c="select * from tictactoe"
         
         cur.execute(c)
         result=cur.fetchall()
         print('[Name,symbol,wins]')
         for a in result:
            print(a)


# how to play the game
def help1():
    print("PRESS 1 FOR INSTRUCTIONS.")
    print("PRESS 2 FOR ABOUT THE GAME")
    print("PRESS 3 FOR  EXIT.")
    while True:
        n=int(input("Enter the choice which is give above"))
        
def leaderboard():
    
         import mysql.connector as sql
         mydb=sql.connect(host="localhost",user="root",password="yash",database="information")
         cur=mydb.cursor()
         c="select * from tictactoe order by win desc"
         
         cur.execute(c)
         result=cur.fetchall()
         print('[Name,symbol,wins]')
         for a in result:
            print(a)
    
#EXIT FROM GAME
def exitt():
        while True:            
            print("The game is quit")
            break

