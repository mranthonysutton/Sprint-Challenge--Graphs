from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


def reverse_direction(directions):
    if directions is None:
        return None

    potential_dirs = ["n", "e", "s", "w"]
    return potential_dirs[(potential_dirs.index(directions) + 2) % 4]


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

traversal_path = []

prev_directions = []
possible_directions = {}
max_directions = {}

prev_directions.append((player.current_room, None, None, 0))

while len(prev_directions) > 0:
    node = prev_directions[-1]
    room = node[0]
    last_direction = node[1]

    if room.id not in possible_directions:
        possible_directions[room.id] = set()

    if last_direction is not None:
        possible_directions[room.id].add(last_direction)

    if len(possible_directions) == len(room_graph):
        break

    room_exists = room.get_exits()
    possible_exists = [i for i in room_exists if i not in possible_directions[room.id]]

    if len(possible_exists) > 0:
        direction = random.choice(possible_exists)
        room_to = room.get_room_in_direction(direction)
        possible_directions[room.id].add(direction)
        prev_directions.append((room_to, reverse_direction(direction)))
        traversal_path.append(direction)
    else:
        traversal_path.append(last_direction)
        prev_directions.pop(-1)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######

"""
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""

