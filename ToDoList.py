# TO DO LIST ## Command Line # Focus: readable code
# v.1 is the classic if-giganest that you code in high school. Neither classy nor efficient, but works.

#class myList():
#    def __init__(self) -> None:
#        self.name = input('What''s it called?')
#        self.all_done = False
#        self.itemsStored = {}                                                          [WORK IN PROGRESS] I want to upgrade the code 
#        print(f'New list created: {self.name}')                                            to allow for multiple lists to exist without 
#                                                                                           the need for multiple text files.
#    def addItem(self, item):
#        self.itemsStored = self.itemsStored.update({item.id : item})
#        print(f'item added: {item.content}')
#                  
#class myItem:
#    def __init__(self, content) -> None:
#        self.id = len(a.itemsStored)
#        self.content = content
#        self.done = False
        
#used_names = []
illegalChars = ['/','\\','|','<','>',':','?','*']
action = input('What''s up?\nC = Create new list\nS = Show lists list\nE = Edit a list\n')

#while action.upper() != '':            implement a loop to perform more actions for each run
if action.upper() == 'C':
    newList = input('How shall the new list be called?\n')    #add check on names already existing 
    if any(char in newList for char in illegalChars):
        print('An illegal character was used. I''m calling the police.')
    else:
        try:
            with open(f'{newList}.txt', 'a') as lst:
                lst.write(f'--- {newList} ---\n')
                print(f'New list created: {newList}\n')
                #answer = input('Do you want to add items to it?')   [WORK IN PROGRESS]
        except:
            print('How did you get here?')

