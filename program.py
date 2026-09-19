"""
This is a Program of my library to see : - What books do i have
                                         - Where am I from reading it 
                
"""

from time import sleep as zz
from subprocess import call 
from pynput import keyboard
import sqlite3
from random import randint

#The Plan is : 
#Intro -> Menu   ->Select a Book (For search) 
#                ->library   -> Add a Book
#                            -> See all Books
#                            -> Edit library 
#                ->Quit 

#Semi Funcs : 


def sql_table_create(db_name = "library.db", table_name = 'Books'):
    try :
        db = sqlite3.connect(db_name)
        mouse = db.cursor()

        mouse.execute(f'CREATE TABLE IF NOT EXISTS {table_name}(id INTEGER, name TEXT, author TEXT, type TEXT,Year INTEGER)')

        db.commit()
        return True 
    
    except :
        return False
    finally :
        db.close()
    
def sql_table_controll( db_name,
                        table_name="Books",
                        task_type = 0,

                        # Type
                        sorting_column =0,
                        search_option =0,
                        order =0,
                        limit_row= 0,
                        limit_option= 0,

                        # ID
                        searching_num1 =0,
                        searching_num2 =0,

                        # Text
                        letter = '',

                        #Inserting
                        book_paramaters = []
                        ):
    
     
    
    table_columns = ('*','id', 'name', 'author', 'type', 'year')
    column = table_columns[sorting_column]

    main_search_options =   ['',
                            # NUMs                                                          
                            f'WHERE {column} = {searching_num1}',                              
                            f'WHERE {column} BETWEEN {searching_num1} AND {searching_num2}',
                            
                            #TXTs
                            f'WHERE {column} LIKE "%{letter}%"'                                
                            
                            ]
    order_search_style = ('ASC', 'DESC')

    order_search_options = (f'ORDER BY id {order_search_style[order]}',
                            f'ORDER BY {column} {order_search_style[order]}')

    limite_search_options =   ('', f'LIMIT {limit_row} ')  
                             
    db = sqlite3.connect(db_name)
    mouse = db.cursor()

    if sql_table_create() is False :
        call("clear")
        print("[ERROR table creating]")
        zz(1)
        return False
     
    else :
        
            match task_type :
                
                # SELECTION
                case 0 :            
                        try :
                            gear = (0 if sorting_column == 0 else 1 )   
                            return list(mouse.execute(
                            f'SELECT {column} FROM {table_name} {main_search_options[search_option]} {order_search_options[gear]} {limite_search_options[limit_option]}'))
                        except :
                            print("[THERE IS AN ERROR]")
                            zz(1)
                            call("clear")
                            return ""

                #INSERTING
                case 1 :    
                    try:
                        mouse.execute(f'INSERT INTO {table_name} VALUES(?,?,?,?,?)', book_paramaters)
                        db.commit()
                        
                        return True
                    except :
                        return False
                    finally : db.close()
                
                # ID Selection for Id detection
                case 2 : 
                    try : return list(mouse.execute(f'SELECT id FROM {table_name}'))
                    except : print("[ID SELECTION PROBLEM]"); zz(1); call("clear"); return ""
                    finally : db.close()
               
def sql_data_sorting_screen(datas, sorting_column, limit_row, limit_option):
    
    tall = line = head_line = 0
    
    if sorting_column == 0  :head_line = 67 
    else : head_line = 16



    columns = ("ID", "NAME", "AUTHOR", "NICHE", "YEAR")

    sorting_columns_option = (f"{columns[0]:7}|{columns[1]:16}|{columns[2]:16}|{columns[3]:16}|{columns[4]:7}|", #ALL
                              f"{columns[sorting_column-1]:16}|",  #ID
                              )
    
      
    print("All Books")
    print("=" * head_line, end="\n")

    if sorting_column == 0 : print(sorting_columns_option[0])
    else :print(sorting_columns_option[1])

    print("_" * head_line, end="\n")
    
    if limit_option == 0 :tall = len(datas)
    else : tall = limit_row
    
    for data in  datas :
        
        data = list(data)
        
                            
        
        if sorting_column == 0 :                                             # IN case if we want to print it all
            for x in range(1,4) :
                if len(data[x]) >= 10:
                    pp = str(data[x])
                    pp = pp.replace(pp[pp.find(" ")], "")
                    pp = pp.replace(pp[10:len(pp)], "")
                    data[x] = pp.replace(pp[7:10], "...") 
        else : 
            if sorting_column != 1 and sorting_column != 5 :                                                                           # IN case of a speacific condition
                if len(data[0]) >= 10:
                    pp = str(data[0])
                    pp = pp.replace(pp[pp.find(" ")], "")
                    pp = pp.replace(pp[10:len(pp)], "")
                    data[0] = pp.replace(pp[7:10], "...")
        
        if sorting_column == 0 :print(f"{data[0]:7}|{data[1]:16}|{data[2]:16}|{data[3]:16}|{data[4]:7}|")
        else : print(f"{data[0]:<16}|")
        
        line += 1
        
        if line != tall : print("-" * head_line, end="\n")
        #else : print("-" * head_line, end="\n")
    
    print("=" * head_line, end="\n")

    input("Press ...")




def search_book():
    # The idea is to search with slecet : 
    # searching with all Columns ; 
    # using LIKE in Text, and Between in INTEGERS

    # Vars 
    search_options = {  "1":"Sort",
                        "2":"Parameters",
                        "3":"Quit"}
    search_parameter_options = {"1":"Sorted Columns",
                                "2":"Specific",
                                "3":"Direction",
                                "4":"Limit",
                                "5":"Quit"}
    spo_specific = {"1":"Column",
                    "2":"Value",
                    "3":"Quit"}
    
    search_columns = ''
    search_specific = ''
    *
    search_as = ''  
    exact_searching_value = -1 
    gap_searching_value = ( -1, -1)

    state = ("[T]", "[F]")
    table_columns = ('*','id', 'name', 'author', 'type', 'year')
    spp_columns={   "1":f"All     {state[0] if search_columns == table_columns[0] else state[1]}",
                                "2":f"ID      {state[0] if table_columns[1] in search_columns else state[1]}",
                                "3":f"Title   {state[0] if table_columns[2] in search_columns else state[1]}",
                                "4":f"Author  {state[0] if table_columns[3] in search_columns else state[1]}",
                                "5":f"Niche   {state[0] if table_columns[4] in search_columns else state[1]}",
                                "6":f"Year    {state[0] if table_columns[5] in search_columns else state[1]}",
                                "7":"Quit"}
    
    
    #Main 

    while True : 
                
        match Menu_printer(search_options, title="searche menu", shape="-", head_steps=len(max(search_options.values(), key=len))*2): 
            case 1 : # Sorting
                
                pass
            case 2 : # Para
                while True :
                    match Menu_printer(search_parameter_options, title="parameters", shape="-", head_steps=len(max(search_parameter_options.values(), key=len))*2) :
                        case 1 : #Columns
                            
                            while True :
                                spp_columns={   "1":f"All     {state[0] if search_columns == table_columns[0] else state[1]}",
                                "2":f"ID      {state[0] if table_columns[1] in search_columns else state[1]}",
                                "3":f"Title   {state[0] if table_columns[2] in search_columns else state[1]}",
                                "4":f"Author  {state[0] if table_columns[3] in search_columns else state[1]}",
                                "5":f"Niche   {state[0] if table_columns[4] in search_columns else state[1]}",
                                "6":f"Year    {state[0] if table_columns[5] in search_columns else state[1]}",
                                "7":"Quit"}
                                
                                n = Menu_printer(spp_columns, title="COLUMNS", shape="-", head_steps=len(max(spp_columns.values(), key=len))*2) - 1   
                                if n == 6 : 
                                    call("clear")
                                    print("[DONE]")
                                    zz(0.1)
                                    break
                                elif n == 0 :    
                                    search_columns = table_columns[0]
                                
                                else : 
                                    if table_columns[n] not in search_columns : search_columns += table_columns[n] + ","
                                
                                j = 0 
                                for i in table_columns :
                                    if i == '*' : continue 
                                    elif i in search_columns : j+=1
                                    if j == 5 : search_columns = '*'
                        
                        case 2 : #Specific
                            while True :
                                match Menu_printer(spo_specific, title="SPECIFIC PARAMETERS", shape="-", head_steps=len(max(spo_specific.values(), key=len))*2) :
                                    case 1 :
                                        spp_specific={  "1":f"ID      {state[0] if table_columns[1] == search_specific else state[1]}",
                                                        "2":f"Title   {state[0] if table_columns[2] == search_specific else state[1]}",
                                                        "3":f"Author  {state[0] if table_columns[3] == search_specific else state[1]}",
                                                        "4":f"Niche   {state[0] if table_columns[4] == search_specific else state[1]}",
                                                        "5":f"Year    {state[0] if table_columns[5] == search_specific else state[1]}",
                                                        "6":"Quit"}
                                        gear = Menu_printer(spp_specific.values(), title="COLUMN", shape="-", head_steps=len(max(spp_specific.values(), key=len))*2)
                                        if gear == 6 : 
                                            call("clear")
                                            print("[DONE]")
                                            zz(0.1)
                                            break
                                        else : search_specific = table_columns[gear]
                                    
                                    case 2 : 
                                        while True :
                                            spo_specific_value =   {"1":f"Exact {state[0] if exact_searching_value != -1 else state[1]}",
                                                                    "2":f"Gap   {state[0] if gap_searching_value[0] == -1 and gap_searching_value[1] == -1 else state[1]}",
                                                                    "3":"Quit"}
                                            
                                            # INTEGERS
                                            if search_specific == table_columns[1] or search_specific == table_columns[5] :
                                                match Menu_printer(spo_specific_value.values(), title="COLUMN", shape="-", head_steps=len(max(spo_specific_value.values(), key=len))*2):
                                                    case 1 :
                                                        call("clear")
                                                        try : exact_searching_value = int(input("New Exact Value = "))
                                                        except : print("ONLY INTEGER"); zz(1)

                                                    case 2 :
                                                        call("clear")
                                                        try : 
                                                            gap_searching_value[0] = int(input("First Gap Value = "))
                                                            gap_searching_value[1] = int(input("Second Gap Value = "))
                                                            
                                                        except : print("ONLY INTEGER"); zz(1)
                                                    
                                                    case 3 :
                                                        call("clear")
                                                        print("[DONE]")
                                                        zz(0.1)
                                                        break   
                                            
                                            #TEXT    
                                            else :
                                                try : search_as = str(input("Approximate Letters : "))
                                                except: print("[ONLY STRING VALUE]") 
                                            
                                    case 3 :
                                        call("clear")
                                        print("[DONE]")
                                        zz(0.1)
                                        break

                        case 3 :pass
                        case 4 :pass
                        case 5 :
                            call("clear")
                            print("[DONE]")
                            zz(0.1)
                            break
            case 3 :
                call("clear")
                print("[DONE]")
                zz(0.1)
                break


def See_All_Books(db_name = "library.db", table_name = "Books") :
    
    #Vars 
    
    sorting_column= 0
    search_option= 0
    order = 0
    limit_row = 0
    limit_option = 0

    # ID
    searching_num1 =0
    searching_num2 =0
    # Text
    letter = ""

    Data_state = ["[> T <]", "[> F <]"]

    opts_sorting = {"1":"Sort",
                    "2":"Parameters",
                    "3":"Quit"}
    
    
    #Main
    
    
    
    while True :
        
        call("clear")
        
        # Books 
        
        
        #sql_data_sorting_screen(datas)

        match Menu_printer(opts_sorting, title = "SORTING", shape = "_", head_steps= 10 * len(max(opts_sorting.values()))) :
                case 1 :
                    """=========================== Printing Data ================================="""
                    datas = sql_table_controll( db_name,
                                                table_name=table_name,
                                                sorting_column=sorting_column,
                                                search_option=search_option,
                                                order=order,
                                                searching_num1=searching_num1,
                                                searching_num2=searching_num2,
                                                letter=letter,
                                                limit_row=limit_row,
                                                limit_option=limit_option)
                    
                    sql_data_sorting_screen(datas=datas, limit_row=limit_row, sorting_column=sorting_column, limit_option=limit_option)
                case 2 :
                    """=========================== Referances ================================="""

                    ref = True
                    while ref :

                        sorting_data_options= {         "1":"Coloumn   ",
                                                        "2":"Reverse   ",
                                                        "3":"Limitted  ",
                                                        "4":"Quit"}
                        
                        sorting_orders_option = {   "1":f"Regular {Data_state[0] if  order == 0 else Data_state[1]}",
                                                    "2":f"Reverse {Data_state[0] if  order == 1 else Data_state[1]}",
                                                    "3":"Quit"}
                        
                        sorting_limits_option=    { "1":f"ALL     {Data_state[0] if  order          == 0 else Data_state[1]:^5}",
                                                    "2":f"Limited {Data_state[0] if  order          == 1 else Data_state[1]:^5}  by ({limit_row:^3})  ",
                                                    "3":"Quit"}
                        
                        sorting_columns_option= {   "1": f"All      {Data_state[0] if  sorting_column   == 0 else Data_state[1]}",
                                                    "2": f"ID       {Data_state[0] if  sorting_column   == 1 else Data_state[1]}",
                                                    "3": f"Name     {Data_state[0] if  sorting_column   == 2 else Data_state[1]}",
                                                    "4": f"Author   {Data_state[0] if  sorting_column   == 3 else Data_state[1]}",
                                                    "5": f"Niche    {Data_state[0] if  sorting_column   == 4 else Data_state[1]}",
                                                    "6": f"Year     {Data_state[0] if  sorting_column   == 5 else Data_state[1]}",
                                                    "7": f"Quit"}
                        
                        match Menu_printer(opts=sorting_data_options, title="SORTING PARAMETERS", shape="_", head_steps= 6 * len(max(sorting_data_options.values()))) :
                            case 1:
                                """ == TYPE == """
                                sorting_column_cache = Menu_printer(opts=sorting_columns_option, title ="SORTING COLUMN", shape="_", head_steps= 6 * len(max(sorting_columns_option.values())))
                                
                                if sorting_column_cache == 7 : pass
                                else : sorting_column = sorting_column_cache - 1

                            case 2:
                                """ == REV == """
                                order_cache = Menu_printer(opts=sorting_orders_option, title="SORTING REFERANCE", shape="_", head_steps= 6 *len(max(sorting_orders_option.values()))) - 1
                                if order_cache == 2 : continue
                                else : order = order_cache 
                                
                                    

                            case 3:
                                """ == LIM == """
                                limite_option_cache = Menu_printer(opts=sorting_limits_option, title= "SORTING LIMITAION", shape="_", head_steps= 6 * len(max(sorting_limits_option.values())))
                                match limite_option_cache :
                                    case 1 :
                                        limit_row = 0
                                        limit_option = 0
                                    case 2 :
                                        limit_option = 1
                                        call("clear")
                                        try: limit_row = int(input("Limitng by - Number of Columns To Be Limited - : "))
                                        except : print("[ERROR ROWS IN INTEGER ONLY]")
                                        zz(0.1)

                                    case 3 :
                                        continue
                                    
                            case 4:
                                call("clear")
                                print("[DONE]")
                                zz(0.1)
                                ref = False
                
                case 3 :
                    call("clear")
                    print("[DONE]")
                    zz(0.1)
                    return True

def add_books(): 
    
    lop = True
    name = author = niche = "NULL"
    year = 0
    
    id_book = randint(0,10000)

    id_list= sql_table_controll(db_name="library.db", task_type=2)
    
    while id_book in id_list : id_book = randint(0,10000)

    book_paramaters = [
            id_book,
            name,
            author,
            niche,
            year,
        ]

    
    
    opts_table = ("Name", "Author", "Niche", "Year")
    
    #>Funcs 
    while lop :
            
        opts_add = {"1": f"Name     [> {book_paramaters[1]:10} <]",
                    "2": f"Author   [> {book_paramaters[2]:10} <]",
                    "3": f"Niche    [> {book_paramaters[3]:10} <]",
                    "4": f"Year     [> {book_paramaters[4]:10} <]",
                    "5": "Submit",
                    "6": "Quit"}
        
        pos= Menu_printer(opts_add,title="Book Parameters", head_steps= 30, shape="-" )
        call("clear")
        
        #pos -=1 
        if pos == 6 : 
            print("[DONE]")
            zz(0.1)
            lop = False
        
        elif pos == 5 :
            #Submit 
            
            try :
                sql_table_controll(db_name="library.db", task_type=1, book_paramaters=book_paramaters) 
                print("[SUBMITION SECCUSSED!]");zz(1)
                lop = False
            except :
                print("[SUBMITION Has probleme]"); zz(1)
        
        elif pos == 4 : 
            
            try : book_paramaters[pos] = int(input(f"Change {book_paramaters[pos]} to : "))
            except : print("[NUMBERS ONLY]"); zz(1)

        else :  
            parameter = str(input(f"Change {book_paramaters[pos]} to : ")) 
            
            try :
                if parameter.find(" ") != -1 : parameter = parameter.replace(parameter[parameter.find(" ")], "")
                if parameter == "Null" : book_paramaters[pos] = "Null"
                else : book_paramaters[pos] = parameter
                    
            except : book_paramaters[pos] = "Null"

def Intro(Title, shape = "-", head_steps = 10, time_out = 1 ): 
    
    call("clear")
    
    if (head_steps - len(Title)) < 0 : head_steps = (len(Title) * 2) 
    if head_steps == 1000 :
        print("[HIGH TITLE]")
        zz(2) 
        return False
    else :
        #while (head_steps - len(Title)) < 0 :
        #    head_steps += 1 
        #    if head_steps == 1000 : 
        #        return False


        # First Line : 
        print(shape * head_steps, end="\n")
        # Title Print
        print(Title.center(head_steps))
        #Second Line 
        print(shape * head_steps, end="", flush=True)

        zz(time_out)

        return True
 
def Menu_printer(opts,title = "", shape = "=", space_line = True, head_steps = 0) : 
     
    realtime_value = ""
    lop = True
    realtime_position = 1
    free_flicker = []
    

    def on_press(key) : 
        
        nonlocal realtime_position, lop 
        
        if key == key.esc :
            realtime_position = -1 
            lop = False
            return False
         
        elif key == key.down : # and realtime_position != len(opts.values()) :
            realtime_position += 1
            if realtime_position == len(opts.values()) + 1 : realtime_position = 1

        elif key == key.up  :#and realtime_position !=1 : 
            realtime_position -= 1
            if realtime_position == 0 : realtime_position = len(opts.values()) 

        elif key == key.enter : 
            lop = False
            return False  
        else : 
            pass
     
    # Making the Head line lenght 
    if head_steps == 0 : 
        head_steps = round(len(max(opts.values(), key=len)) * 2 )
    
    # Key Hooker
    listener = keyboard.Listener(on_press=on_press)       
    listener.start()
    
    while lop :
        
        option_positon = 0
        spacer = 0
        space = ("","  ")

        print(title.upper())
        print(shape * head_steps, end="\n")

        if space_line :
            for key, value in opts.items() :
                option_positon += 1 
                spacer = ( 1 if option_positon == realtime_position else 0 )
                print(f"{key} {space[spacer]})> {value}")
            print(shape * head_steps, end="\n")     
        else : 
            for key, value in opts.items() :
                option_positon += 1 
                spacer = ( 1 if option_positon == realtime_position else 0 )
                print(f"|{space[spacer]}{key} )> {value}")
            print("\n",shape * head_steps, end="\n") 
        
        #value = 1
        #for v in opts.values() :
        #    if value == realtime_position  : realtime_value = v; break
        #    else : value+=1  
        #print(f"[> {realtime_value} <]")
        
        zz(0.016)

        if free_flicker[::-1] != realtime_position :
            call("clear")
            free_flicker.append(realtime_position)
        elif len(free_flicker) == 2 : 
            free_flicker.clear()
            free_flicker.append(realtime_position)
        else : 
            continue
        
    print("[DONE]")
    zz(0.1)
    call("clear")
    input()
    return realtime_position
            
def About() :
    pass

def View_library() :
    
    # Vars
    pos = 0
    opts_lib = {"1" : "All      ",
                "2" : "Search   ",
                "3" : "Add      ",
                "4" : "Edit     ",
                "5" : "Quit     "}
    #Funcs

    #Main
    
    while True :
        
        match Menu_printer(opts_lib,title="Library Menu", shape="_", head_steps= 2 * len(max(opts_lib.values(), key=len))) :
            case 1:
                See_All_Books()
            
            case 2:
                search_book()
                
            case 3:
                add_books()
            
            case 4:
            
                pass
            
            case 5 | -1 :
                print("[DONE]")
                zz(0.1)
                break
                


    
    
    
# Main program =======================================================================================================================

menu_opts= {"1" : "Select a Book",
            "2" : "View library",
            "3" : "Quit"}


Loop = Intro("BooKy", shape="=", head_steps=70, time_out=1)

while Loop :
     
    match Menu_printer(menu_opts, title="Main Menu", space_line= True) : 
        case 1 :
            View_library()
        
        case 2 :
            About()
        
        case 3 | -1 :
            call("clear")
            print("[DONE]")
            zz(0.1)
            Loop = False

