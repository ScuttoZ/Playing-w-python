# TO DO LIST ## Command Line # Focus: readable code
# v.1 is the classic if-giganest that you code in high school. Neither classy nor efficient, but works (on PC).

        
# Initialize at launch
import subprocess
import platform

usedNames = []
illegalChars = ['/','\\','|','<','>',':','?','*']
running = True

# Loops this while running.
while running:            
    action = input('_______________________________________________________________________________________________________\nWhat''s up?\nC = Create new list\nR = Read a list\nE = Edit a list\n')
    
    # Create
    if action.upper() == 'C':
        newList = input('How shall the new list be called?\n')    #add check on names already existing 
        if any(char in newList for char in illegalChars):
            print('An illegal character was used. I''m calling the police.')
        else:
            try:
                with open(f'{newList}.txt', 'a') as lst:
                    lst.write(f'--- {newList} ---\n')
                    print(f'New list created: {newList}\n')
                    action = ''
                    answer = input('Do you want to write in it?\nY / N')
                    if answer.upper() == 'Y':
                        action = 'E'
                    elif answer.upper() == 'N':
                        action = ''
            except:
                print('How did you get here?')
                action = ''
    
    # Read
    if action.upper() == 'S':
        selection = input('Which list do I open?\n')           # User must know which lists exist. Add list of lists to display when 
        try:
            with open(f'{selection}.txt') as lst:
                print(f'-----BEGIN TXT FILE-----')
                print(f'{lst.read()}')
                print('-----END TXT FILE-----')
                action = ''
        except:
            print('Couldn''t open soz\n')
            action = ''
    
    # Edit
    if action.upper() == 'E':
        selection = input('Which list ae we editing?\n')
        try:
            if platform.system() == "Windows":
                command = 'notepad'
            elif platform.system() == "Darwin":
                command = 'open'
            else:
                command = 'xdg-open'
            subprocess.run([command, f'{selection}.txt'], check=True)
            action = ''
        except:
            print('Are you running this on mobile??\n')
            action = ''
    
    # Close
    running = False if input('Are you done?\nY / N') == 'Y' else True
    print('Alright, back to the menu:\n')


## aggiungere possibilità di cifrare i file con una password che non viene salvata dallo script ma solo presa in input a ogni run
