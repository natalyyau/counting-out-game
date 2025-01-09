import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class CircularLinkedList:

    def __init__(self):
        #the "start" of the linked list
        self.head = Node(None)

        #the "end" of the linked list
        self.tail = Node(None)

    def add_num(self, value):
        new_num = Node(value)

        #if list is empty, the value added is the head, and the node points back to itself
        if self.head.value is None:
            self.head = new_num
            self.tail = new_num
            new_num.next = self.head

        #if the list isn't empty, the value is added to the "end" of the list and the node points back to the head
        else:
            self.tail.next = new_num
            self.tail = new_num
            self.tail.next = self.head

    def remove_num(self, node):
        #start from the beginning of the linked list
        current = self.head

        #if the first node is the element needed to be removed
        if current == node:

            #update the head to skip the removed node
            self.head = current.next

            #update the tail to point to the new head
            if self.head == node:
                self.tail = None
            else:
                self.tail.next = self.head
            return
        
        #else, traverse through the list until we find the node we are looking for
        while current.next != self.head:

            #if the next node is the one we are looking for
            if current.next == node:

                #remove the node by skipping it in the linked list
                current.next = node.next

                #update the tail if the removed node was the tail
                if self.tail == node:
                    self.tail = current
                return
            
            #continue to the next node
            current = current.next

    def print_list(self):
        #start from the beginning of the linked list
        current = self.head

        #traverse through the entire linked list
        while True:

            #print the value of the current node
            print(current.value, end=" ")

            #move to the next node
            current = current.next

            #if we have reached the head again, break the loop
            if current == self.head:
                break

    def potato_game(self, k, start_num):
        #start from the beginning of the linked list
        if start_num != self.head:
            current_num = start_num
        else:
            current_num = self.head

        #controls when each round of the game ends
        for i in range(k - 1):
            current_num = current_num.next

        #save the next node
        next_num = current_num.next

        #saves and removes the current node
        deleted_node = current_num
        self.remove_num(current_num)

        #move to the next node for the next round
        current_num = next_num

        #return the value of the deleted node and next node
        return deleted_node.value, current_num
    
    def list_len(self):
        len = 0

        #start from the beginning of the linked list
        current = self.head

        #traverse through the entire linked list
        while True:
            len += 1

            #move to the next node
            current = current.next

            #if we have reached the head again, break the loop
            if current == self.head:
                break
        return len
    
class CountingOutGame:
    #Class attributs
    n = 0
    k = 0
    game = CircularLinkedList()
    start_num = game.head
    round_count = 0

    #GUI setup
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("counting out game")
        self.root.geometry("1000x500")
        self.root.configure(bg="pink")
        self.gui_setup()
    
    #GUI setup
    def gui_setup(self):

        #Creates N entry
        self.label = tk.Label(self.root, text="Enter N", font=("arial", 20))
        self.label.pack(padx=1, pady=1)
        self.entry_n = tk.Entry(self.root)
        self.entry_n.pack(padx=1, pady=1)

        #Creates K entry
        self.label2 = tk.Label(self.root, text="Enter K", font=("arial", 20))
        self.label2.pack(padx=1, pady=1)
        self.entry_k = tk.Entry(self.root)
        self.entry_k.pack(padx=1, pady=1)

        #Creates start button
        self.start_button = tk.Button(self.root, text="Start", command=self.start_game)
        self.start_button.pack(padx=1, pady=1)

        #Creates textbox at the bottom of the screen
        self.game_info = tk.Text(self.root, height=15)
        self.game_info.pack(side=tk.BOTTOM, fill=tk.BOTH)

        #Creates eliminate button
        self.eliminate_button = tk.Button(self.root, text="Eliminate", command=self.eliminate)

    def start_game(self):
        #Checks the Values of N and K
        try:
            CountingOutGame.n = int(self.entry_n.get())
            CountingOutGame.k = int(self.entry_k.get())

        except ValueError:
            messagebox.showinfo(message="Allowed values:\n1<n<12\nk>=1")
            return

        if not (1 < CountingOutGame.n < 12 and CountingOutGame.k >= 1):
            messagebox.showinfo(message="Allowed values:\n1<n<12\nk>=1")
            return
        
        self.game_info.insert(tk.INSERT, f"Game Started. N={CountingOutGame.n} K={CountingOutGame.k} \n")

        #Creates the player icons in a line
        self.button = []
        for i in range(CountingOutGame.n):
            self.button.append(tk.Button(self.root, text=f"{i}", width=4, height=2))
            self.button[i].place(y=200, x=20 + (i*80))

        #Makes the elimination button show up on screen
        self.eliminate_button.pack()
        
        #Creates the linked list
        for i in range(CountingOutGame.n):
            CountingOutGame.game.add_num(i)

    def eliminate(self):
        #keeps track of the rounds
        CountingOutGame.round_count += 1

        #plays each round of the counting out game until last two numbers are left
        if (CountingOutGame.game.list_len() > 2):

            #first round there is no "next number" so the game starts at the beginning of linked list
            if self.round_count == 1:
                result, CountingOutGame.start_num = CountingOutGame.game.potato_game(CountingOutGame.k, CountingOutGame.game.head)
                self.game_info.insert(tk.INSERT, f"Round {self.round_count}: Player {result} has been eliminated!\n")
                self.button[result].destroy()

            #after the first round, the next round begins from the next number after the number that got eliminated
            else:
                result, CountingOutGame.start_num = CountingOutGame.game.potato_game(CountingOutGame.k, CountingOutGame.start_num)
                self.game_info.insert(tk.INSERT, f"Round {self.round_count}: Player {result} has been eliminated!\n")
                self.button[result].destroy()

        #When the last two numbers are left, one of the numbers is eliminated and the last one remaining is the winner
        else:
            result, CountingOutGame.start_num = CountingOutGame.game.potato_game(CountingOutGame.k, CountingOutGame.start_num)
            self.game_info.insert(tk.INSERT, f"Round {self.round_count}: Player {result} has been eliminated!\n")
            self.button[result].destroy()
            messagebox.showinfo(message=f"Winner: Player {CountingOutGame.start_num.value}")

            #resets the game at the end of end of the game
            self.reset_game()
            
    def reset_game(self):
            # Reset game-related variables
            CountingOutGame.game = CircularLinkedList()
            CountingOutGame.start_num = CountingOutGame.game.head
            CountingOutGame.round_count = 0

            # Reset GUI
            for button in self.button:
                button.destroy()
            self.eliminate_button.pack_forget()
            self.game_info.delete('1.0', tk.END)


    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = CountingOutGame()
    game.run()

        

        