# This project creates a card game where first we have to write an intialize 
#                                                               function
# Then we have to write a display function 
# Then we have to make sure that all the moves a user makes are valid or not 
#   for that we have write validate functions for each of the moves
# then we have to have functions that will make the move 
# Then we have our main function where we combine everything make a cohesive 
#                                                               card game
# Solitaire: Seahaven
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same random number (needed to replicate tests)

MENU = '''     
Input options:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tableau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from end of Cell s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game       
'''

def initialize():
    ''' Used to initialize the game 
    Doesn't take any parameters
    returns the tableau, foundation and cells '''
    
    deck_type = cards.Deck() #defines the deck type 
    deck_type.shuffle() #shuffles the deck 
    
    foundation = [[], [], [], []] #initializes foundation
    tableau = [[], [], [], [], [], [], [], [], [], []] #initialize tableau
    for i in range(5): #inside foundation 
        for j in range(10): #in tableau
            #append tableau with cards from the deck
            tableau[j].append(deck_type.deal()) 
    #initialize all four cells 
    cells = [None, deck_type.deal(), deck_type.deal(), None]
    
    #returns the tableau, foundation and cells 
    return tableau, foundation, cells

def display(tableau, foundation, cells):
    '''Display the cell and foundation at the top.
       Display the tableau below.'''
       
    print("\n{:<11s}{:^16s}{:>10s}".format( "foundation","cell", "foundation"))
    print("{:>14s}{:>4s}{:>4s}{:>4s}".format( "1","2","3","4"))
    for i,f in enumerate(foundation):
        if f and (i == 0 or i == 1):
            print(f[-1],end=' ')  # print first card in stack(list) on foundation
        elif i == 0 or i == 1:
            print("{:4s}".format( " "),end='') # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '),end='')
    for c in cells:
        if c:
            print(c,end=' ')  # print first card in stack(list) on foundation
        else:
            print("[  ]",end='') # fill space where card would be so foundation gets printed in the right place
    print("{:3s}".format(' '),end='')
    for i,f in enumerate(foundation):
        if f and (i == 2 or i == 3):
            print(f[-1],end=' ')  # print first card in stack(list) on foundation
        elif i == 2 or i == 3:
            print("{}{}".format( " ", " "),end='') # fill space where card would be so foundation gets printed in the right place
        
    print()
    print("\ntableau")
    print("   ",end=' ')
    for i in range(1,11):
        print("{:>2d} ".format(i),end=' ')
    print()
    # determine the number of rows in the longest column        
    max_col = max([len(i) for i in tableau])
    for row in range(max_col):
        print("{:>2d}".format(row+1),end=' ')
        for col in range(10):
            # check that a card exists before trying to print it
            if row < len(tableau[col]):
                print(tableau[col][row],end=' ')
            else:
                print("   ",end=' ')
        print()  # carriage return at the end of each row
    print()  # carriage return after printing the whole tableau
    
        
def validate_move_within_tableau(tableau,src_col,dst_col):
    '''
        Validate if the movement of card with tableau is valid or not 
    '''
    try:
        src_card = tableau[src_col][-1] #try picking a card from tableau
    except IndexError: #except an error 
        return False
    if src_card == None: #if the tableau is empty 
        return False #not valid
         
    if tableau[dst_col] == []: #if tableau is empty 
        if src_card.rank() == 13: #and the picked up card is a king 
            return True #its a valid move 
        else: #if not 
            return False  #its invalid
        
    dst_card = tableau[dst_col][-1]  #defines where the card should be placed 
    if dst_card.suit() == src_card.suit(): #the suits of the card should match 
        if dst_card.rank() == src_card.rank()+1: #src card should be 1 rank lower 
            return True 
        else: 
            return False
    else:
        return False
    

def validate_move_cell_to_tableau(tableau,cells,cell_no,dst_col):
    '''
        Validate if the movement of the card from cell to tableau is valid or not 
    '''
    try:
        src_card = cells[cell_no]
    except IndexError:
        return False
    if src_card == None:
        return False
    
    if tableau[dst_col] == []: #if empty tableau column 
        if src_card.rank() == 13: #if card is a king 
            return True  #valid move 
        else:
            return False
    dst_card = tableau[dst_col][-1]
    if dst_card.suit() == src_card.suit(): #same suits 
        if dst_card.rank() == src_card.rank()+1: #src card ranks lower 
            return True #valid move 
        else:
            return False 
    else: 
        return False
        
def validate_move_tableau_to_cell(tableau,cells,src_col,cell_no):
    '''
        Validate if the movement of the card from tableau to cell is valid or not
    '''
    try:
        src_card = tableau[src_col][-1] #defines the src card 
    except IndexError:
        return False
    
    dst_card = cells[cell_no] #dst card is in the cells 
    if dst_card == None: #cell can only hold 1 card 
        return True 
    else:
        return False 

def validate_move_tableau_to_foundation(tableau,foundation,src_col,found_no):
    '''
    Validate if the movement of the card from tableau to foundation is valid or not
    '''
    try:
        src_card = tableau[src_col][-1] #defines src card 
    except IndexError: 
        return False 
    
    if src_col == None: #if empty col in tableau 
        return False
    
    if foundation[found_no] == []: #empty column in foundation 
        if src_card.rank() == 1: #if the card is an ace 
            return True  #valid move 
        else:
            return False 
    
    try:
        dst_card = foundation[found_no][-1] #only appends at the end in the foundation 
    except IndexError:
        return False 

    if dst_card.suit() == src_card.suit(): #if same suit 
        if dst_card.rank()+1 == src_card.rank(): #dst card one rank lower 
            return True #valid move 
        else:
            return False
    else:
        return False 
            
def validate_move_cell_to_foundation(cells,foundation,cell_no,found_no):
    '''
        Validate if the movement of the card from cell to foundation is valid or not
    '''
    try:
        src_card = cells[cell_no]
    except IndexError:
        return False 
    
    if src_card == None:
        return False 
    
    if foundation[found_no] == []: #empty column in foundation 
        if src_card.rank() == 1:  #if the card is an ace 
            return True  #valid move
        else: 
            return False 
        
    try:
        dst_card = foundation[found_no][-1] #only appends at the end in the foundation 
    except IndexError:
        return False 
    
    if dst_card.suit() == src_card.suit(): #if same suit
        if dst_card.rank()+1 == src_card.rank(): #dst card one rank lower 
            return True #valid move 
        else:
            return False
    else:
        return False 
    
def move_within_tableau(tableau,src_col,dst_col):
    '''
        Moves card from one col to the other within the tableau 
    '''
    #check if the move is valid
    mwt = validate_move_within_tableau(tableau, src_col, dst_col)
    if mwt == True: #if valid move 
        src_card = tableau[src_col] #pop the card from the src col 
        s_card = src_card.pop()
        tableau[dst_col].append(s_card) #append to the dst col 
        return True
    else:
        return False  

def move_tableau_to_cell(tableau,cells,src_col,cell_no):
    '''
        Moves card from tableau to cell
    '''
    #check if the move is valid 
    mtc = validate_move_tableau_to_cell(tableau, cells, src_col, cell_no)
    if mtc == True: #if valid move 
        src_card = tableau[src_col]
        s_card = src_card.pop() #pop the card 
        cells[cell_no] = s_card #and add it to the empty cell column 
        return True 
    else:
        return False
    
    
def move_cell_to_tableau(tableau,cells,cell_no,dst_col):
    '''
        Moves card from cell to tableau
    '''
    #check if the move is valid
    mct = validate_move_cell_to_tableau(tableau, cells, cell_no, dst_col)
    if mct == True:
        src_card = cells[cell_no]
        cells[cell_no] = None
        tableau[dst_col].append(src_card)
        return True
    else:
        return False

def move_cell_to_foundation(cells,foundation,cell_no,found_no):
    '''
        Moves card from cell to foundation
    '''
    #check if the move is valid
    mcf = validate_move_cell_to_foundation(cells, foundation, cell_no, found_no)
    if mcf == True: #if valid move 
        src_card = cells[cell_no]
        cells[cell_no] = None  #remove the card from cell #empty cell = None 
        foundation[found_no].append(src_card) #append it to the foundation 
        return True
    else:
        return False 
            
def move_tableau_to_foundation(tableau,foundation,src_col,found_no):
    '''
        Moves card from tableau to foundation
    '''
    #check if the move is valid
    mtf = validate_move_tableau_to_foundation(tableau, foundation, src_col, found_no)
    if mtf == True: #if valid move 
        src_card = tableau[src_col] 
        s_card = src_card.pop() #pop the card from the src col 
        foundation[found_no].append(s_card) #append to the foundation col 
        return True 
    else:
        return False 
                    
def check_for_win(foundation):
    '''
        Checks if the user won or not 
    '''
    #if all the 4 list in foundation has 13 cards the user wins 
    if len(foundation[0]) == 13:
        if len(foundation[1]) == 13:
            if len(foundation[2]) == 13:
                if len(foundation[3]) == 13:
                    return True 
    else:
        return False
        
         

def get_option():
    '''Prompt the user for an option and check that the input has the 
       form requested in the menu, printing an error message, if not.
       Return:
    MTT s d: Move card from end of Tableau column s to end of column d.
    MTC s d: Move card from end of Tableau column s to Cells d.
    MCT s d: Move card from Cells s to end of Tablenleau column d.
    MTF s d: Move card from end of Tableau column s to Foundation d.
    MCF s d: Move card from Cells s to Foundation d.
    R: Restart the game (after shuffling)
    H: Display this menu of choices
    Q: Quit the game        
    '''
    option = input( "\nInput an option (MTT,MTC,MCT,MTF,MCF,R,H,Q): " )
    option_list = option.strip().split()
    
    opt_char = option_list[0][0].upper()
    
    if opt_char in 'RHQ' and len(option_list) == 1:  # correct format
        return [opt_char]

    if opt_char == 'M' and len(option_list) == 3 and option_list[1].isdigit() \
        and option_list[2].isdigit():
        opt_str = option_list[0]
        if opt_str in ['MTT','MTC','MCT','MTF','MCF']:
            return [opt_str,int(option_list[1]),int(option_list[2])]

    print("Error in option:", option)
    return None   # none of the above
 
def main():
    print("\nWelcome to Seahaven Solitaire.\n")
    tableau, foundation, cells = initialize()
    display(tableau, foundation, cells)
    print(MENU)
    
    option = get_option()
    while option != "Q":
        if option == "MTT":
            move_within_tableau(tableau, src_col, dst_col)
        elif option == "MTC":
            move_tableau_to_cell(tableau, cells, src_col, cell_no)
        elif option == "MCT":
            move_cell_to_tableau(tableau, cells, cell_no, dst_col)
        elif option == "MTF":
            move_tableau_to_foundation(tableau, foundation, src_col, found_no)
        elif option == "MCF":
            move_cell_to_foundation(cells, foundation, cell_no, found_no)
        elif option == "R": 
            continue
        elif option == "H":
            print(MENU)
        elif option == "Q":
            break
        elif check_for_win(foundation) == True:
            display(tableau, foundation, cells)
            print("\n- - - - New Game. - - - -")
            continue
            display(tableau, foundation, cells)
            print(MENU)
        else:
            print("Error in option:", option)
        
        
    print("Thank you for playing.")

if __name__ == '__main__':
    main()
