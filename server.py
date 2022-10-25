

import binascii
import random
import socket
import sys
import threading

from tictactoe import *

class Server():
    """
    Server for TicTacToe game
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 1
        self.start()

    def conn_send(self, conn, string):
        bin_data = string.encode('utf-8')
        conn.sendall(bin_data)

    # for reading client move
    def conn_read(self, conn):
        bin_data = ''
        while True:
            bin_data += conn.recv(1024).decode('utf-8')
            try:
                bin_data.index(' end')
                break
            except ValueError:
                pass
        bin_data = bin_data.split(' ')
        u_row, u_col = int(bin_data[0]), int(bin_data[1])
        return u_row, u_col


    def start(self):
        # Init server socket to listen for connections
        try:
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.bind((self.host, self.port))
            server_sock.listen(self.backlog)
        except OSError as e:
            print ("Unable to open server socket: ", e)
            if server_sock:
                server_sock.close()
                sys.exit(1)
        # Wait for client connection
        while True:
            client_conn, client_addr = server_sock.accept()
            print ('Client with address has connected', client_addr)
            thread = threading.Thread(target = self.play, args = (client_conn, client_addr))
            thread.start()


    def play(self, conn, addr):
        # Fill out this function
        print('Play game here')
        # Create board on server end
        board_size_init = conn.recv(1024)
        board_size_temp = board_size_init.decode('utf-8')
        board_size = int(board_size_temp.split(' ')[0])
        t = TicTacToe(board_size)
        t.display("")

        # gameplay
        print("Play game")
        while not t.check_done():
            # Receive client move
            u_row, u_col = self.conn_read(conn)
            # display client move on server board
            t.move(u_row, u_col, "X")
            # Display user (client) move
            t.display("User Move")
            # Check state
            if t.check_done(): break
            # create server move
            s_row, s_col = t.server_choose()
            # implement server move on server board
            t.move(s_row, s_col, "O")
            # Display server move on server board
            t.display("Server move")
            # send server move to client, add flag
            self.conn_send(conn, str(s_row) + " " + str(s_col) + " end")
            # Check state
            if t.check_done(): break


def main():
    server_host = 'localhost'
    server_port = 50008

    if len(sys.argv) > 1:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])

    # Create ttt server object
    s = Server(server_host, server_port)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")
    except Exception:
        print("Other exception...")
