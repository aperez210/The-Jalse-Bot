import random

SIZE = 9 
cursor = [4,4]

def make_grid():
    y = []
    for d in range(SIZE):
        y.append([0,0,0,0,0,0,0,0,0])
    return y

grid = make_grid()

def edit_grid(x,y,value):
    grid[y][x] = value
        
def print_grid():
    for line in grid:
        print(line)

def query_grid(x,y):
    return grid[y][x]

def get_cursor_room():
    return [cursor[0],cursor[1]]
    
def get_room_north():
    return [cursor[0],cursor[1]-1]

def get_room_south():
    return [cursor[0], cursor[1]+1] 

def get_room_east():
    return [cursor[0] + 1,cursor[1]]

def get_room_west():
    return [cursor[0] - 1,cursor[1]]

def get_combination(number):
    if number < 0 or number > 15:
        return "Invalid number"
    
    binary = bin(number)[2:].zfill(4)
    combination = ""
    if binary[0] == '1':
        combination += "North "
    if binary[1] == '1':
        combination += "South "
    if binary[2] == '1':
        combination += "East "
    if binary[3] == '1':
        combination += "West"
    
    return combination.strip()

def randomize_close_rooms():
    north = get_room_north()
    south = get_room_south()
    east = get_room_east()
    west = get_room_west()
    match query_grid(cursor[0],cursor[1]):
        case 15:
            randomize_north(north)
            randomize_south(south)
            randomize_east(east)
            randomize_west(west)
        case 14:
            randomize_north(north)
            randomize_south(south)
            randomize_east(east)
        case 13:
            randomize_north(north)
            randomize_south(south)
            randomize_west(west)
        case 12:
            randomize_north(north)
            randomize_south(south)
        case 11:
            randomize_north(north)
            randomize_south(south)
            randomize_west(west)
        case 10:
            randomize_north(north)
            randomize_east(east)
        case 9:
            randomize_north(north)
            randomize_west(west)
        case 8:
            randomize_north(north)
        case 7:
            randomize_south(south)
            randomize_east(east)
            randomize_west(west)
        case 6:
            randomize_south(south)
            randomize_east(east)
        case 5:
            randomize_south(south)
            randomize_west(west)
        case 4:
            randomize_south(south)
        case 3:
            randomize_east(east)
            randomize_west(west)
        case 2:
            randomize_east(east)
        case 1:
            randomize_west(west)    
            
def randomize_south(north):
    current = query_grid(north[0],north[1])
    if current == 0:
        edit_grid(north[0],north[1], pick_random_room([4,5,6,7,12,13,14,15]))
    
def randomize_north(south):
    current = query_grid(south[0],south[1])
    if current == 0:
        edit_grid(south[0],south[1], pick_random_room([4,5,6,7,12,13,14,15]))

def randomize_west(east):
    current = query_grid(east[0],east[1])
    if current == 0:
        edit_grid(east[0],east[1], pick_random_room([2,3,6,7,10,11,14,15]))
    
def randomize_east(west):
    current = query_grid(west[0],west[1])
    if current == 0:
        edit_grid(west[0],west[1], pick_random_room([1,3,5,7,9,11,11,13,15]))
            
def pick_random_room(possibilities:list[int]):
    return random.choice(possibilities)
            
edit_grid(4,4,15)
y = 0
for line in grid:
    x = 0
    for numb in line:
        cursor[0] = x
        cursor[1] = y
        try:
            randomize_close_rooms()
        except:
            print("whoops!")
        x+=1
    y+=1
    

print_grid()