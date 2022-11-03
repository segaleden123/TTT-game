

import binascii
import random
import socket
import sys

from tictactoe import *

class Client:

    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.start(server_host, server_port)

    def start(self, host, port):

        # Fill this out
        print("Start game")
        # Try to connect to ttt server
        try:
            server_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((host, port))
        except OSError as e:
            print ('Unable to connect to socket: ', e)
            if server_sock:
                server_sock.close()
            sys.exit(1)

        # Start the game
        self.play(server_sock)

    # strvar.encode(’utf-8’) and strvar.decode(’utf-8’).

    def sock_send(self, sock, string):
        bin_data = string.encode('utf-8')
        sock.sendall(bin_data)

    # for reading server move
    def sock_read(self, sock):
        bin_data = ''
        while True:
            bin_data += sock.recv(1024).decode('utf-8')
            try:
                bin_data.index(' end')
                break
            except ValueError:
                pass
        bin_data = bin_data.split(' ')
        s_row, s_col = int(bin_data[0]), int(bin_data[1])
        return s_row, s_col


    def play(self, sock):
        # Create board
        board_size = int(input("Enter number of rows in TicTacToe board: "))
        # Send board size to server
        self.sock_send(sock, str(board_size) + ' end')
        # Create board on client end
        t = TicTacToe(int(board_size))
        t.display("")

        # gameplay
        print("Play game")
        while not t.check_done():
            # Client move
            u_row, u_col = t.query_user()
            while not t.valid_move(u_row, u_col):
                u_row, u_col = t.query_user()
            # make move on client board
            t.move(u_row, u_col, "X")
            # Display User move
            t.display("User Move")
            # send move to server
            self.sock_send(sock, str(u_row) + " " + str(u_col) + " end")
            # Check state
            if t.check_done(): break
            # Server move
            s_row, s_col = self.sock_read(sock)
            # put server move onto client board
            t.move(s_row, s_col, "O")
            # Show new client board with server move
            t.display("Server Move")
            # Check state
            if t.check_done(): break
            

def main():
    server_host = 'localhost'
    server_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    client = Client(server_host, server_port)

if __name__ == '__main__':
    main()

