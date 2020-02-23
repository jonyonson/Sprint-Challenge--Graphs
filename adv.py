from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue:
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
player = Player(world.starting_room)

# Print an ASCII map
# world.print_rooms()

def find_nearest():
    q = Queue()
    visited = set()
    q.enqueue([player.current_room])
    q1 = [[]]
    found = False
    while q.size() > 0 and found is False:
        path = q.dequeue()
        node = path[-1]
        p1 = q1.pop(0)
        if node.id not in visited:
            visited.add(node.id)
            dirs = node.get_exits()
            random.shuffle(dirs)
            for direction in dirs:
                next_room = node.get_room_in_direction(direction)
                if found is False and next_room.id not in visited:
                    new_path = path[:]
                    next_added_path = list(p1)
                    if next_room.id not in v:
                        found = True
                        for d in next_added_path:
                            player.travel(d)
                            traversal_path.append(d)
                    else:
                        next_added_path.append(direction)
                        new_path.append(next_room)
                        q.enqueue(new_path)
                        q1.append(next_added_path)


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
v = {}
prev = None
opposite_direction = {"n":"s", "s":"n", "e":"w", "w":"e"}

while True:
    traveled = False
    if player.current_room.id not in v:
        v[player.current_room.id] = prev
    dirs = player.current_room.get_exits()
    random.shuffle(dirs)
    for direction in dirs:
        if traveled == False and player.current_room.get_room_in_direction(direction).id not in v:
            player.travel(direction)
            traversal_path.append(direction)
            prev = opposite_direction[direction]
            traveled = True

    if traveled is False:
        if len(v) < len(room_graph):
            if len(player.current_room.get_exits()) == 1:
                while len(player.current_room.get_exits()) <= 2:
                    traversal_path.append(v[player.current_room.id])
                    player.travel(v[player.current_room.id])
                    dirs = player.current_room.get_exits()
                    random.shuffle(dirs)
                    for direction in dirs:
                        if player.current_room.get_room_in_direction(direction).id not in v:
                            break
            else:
                find_nearest()
        else:
            break

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(traversal_path)
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
