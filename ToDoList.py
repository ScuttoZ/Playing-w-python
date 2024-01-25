# TO DO LIST ## Command Line # Focus: readable code
# v.1 is the classic if-giganest that you code in high school. Neither classy nor efficient, but works (on PC).

        
# Initialize at launch                  [BUG]: the script doesn't save files in the directory you're running it from instead of a specific one. [FIX]: I need to start saving lists in a separate dir from where stuff like usedNames is stored in txt.
import subprocess
import platform
import os

action = ''
usedNames = ()
illegalChars = ['/','\\','|','<','>',':','?','*']
running = True

# Loops this while running.
def Create():
    newList = input('How shall the new list be called?\n')
    if any(char in newList for char in illegalChars):
        print('An illegal character was used. I''m calling the police.')
    else:
        try:
            global usedNames
            if newList not in usedNames:                                # If the input name was not used yet,
                with open('usedNames.txt', 'a') as ope:           #  
                    ope.write(usedNames.append(newList))          #  save it and 
                with open(f'{newList}.txt', 'a') as lst:                #
                    lst.write(f'--- {newList} ---\n')                   #  create a list.txt
                    print(f'New list created: {newList}\n')
                    answer = input('''
                                   Do you want to write in it?
                                   Y / N
                                   ''')
                    if answer.upper() == 'Y':
                        Edit(newList)
                    elif answer.upper() == 'N':
                        Close()
            else:
                answer = input(f'''
                               The list {newList} already exist, what do you want to do?
                               1) Change name
                               2) Open that one
                               
                               1 / 2
                               ''')
                if answer == 1:
                    pass
                elif answer == 2:
                    Edit(newList)
        except:
            print('How did you get here?')
            Close()

def Read(selection):
    selection = input('Which list do I open?\n') if selection == None else selection          # User must know which lists exist. Add list of lists to display when 
    try:
        with open(f'{selection}.txt') as lst:
            print(f'''
                  -----BEGIN TXT FILE-----
                  {lst.read()}
                  -----END TXT FILE-----
                  ''')
            Close()
    except:
        print('Couldn''t open soz\n')
        Close()

def Edit(selection = None):
    selection =  input('Which list ae we editing?\n') if selection == None else selection
    try:
        if platform.system() == "Windows":
            command = 'notepad'
        elif platform.system() == "Darwin":
            command = 'open'
        else:
            command = 'xdg-open'
        subprocess.run([command, f'{selection}.txt'], check=True)
        Close()
    except:
        print('Are you running this on mobile??\n')
        Close()

def Close():
    global running 
    running = False if input('Are you done?\nY / N\n').upper() == 'Y' else print('Alright, back to the menu:\n')   
    
while running:            
    if action.upper() == 'C': Create()
    if action.upper() == 'R': Read()
    if action.upper() == 'E': Edit()
    action = input('_______________________________________________________________________________________________________\nWhat''s up?\nC = Create new list\nR = Read a list\nE = Edit a list\n')






## aggiungere possibilità di cifrare i file con una password che non viene salvata dallo script ma solo presa in input a ogni run
