#011128912, Student ID

#import necessary modules
import re
import csv
from datetime import datetime, timedelta, time

#HashMap Class
class HashMap:
    #init. instance vars
    def __init__(self):
        self.size = 64 #how many cells the hashmap has
        self.list = [[] for _ in range(self.size)] #hashmap storage using chaining with empty nested lists
        self.num_entries = 0 #counts how many entries the hashmap has

    #make a copy of the hashmap
    def copy(self):
        copied_map = HashMap()
        copied_map.list = [cell.copy() for cell in self.list]
        copied_map.num_entries = self.num_entries
        return copied_map

    #hashing function that returns an index
    #returns the remainder of ASCII sums divided by hash table size (64)
    def get_index(self, key):
        hash_val = 0
        for char in str(key):
            hash_val += ord(char)
        return hash_val % self.size

    #add entry to hashmap - chaining with nested lists
    def add(self, key, value):
        key = str(key)
        key_index = self.get_index(key)
        nested_list = [key, value]

        cell = self.list[key_index]

        if cell: #if the cell has entries, update an old value or add a new key-value pair
            for pair in cell: #update the value
                if pair[0] == key:
                    pair[1] = value
                    break
            else: #add a new pair
                cell.append(nested_list)
                self.num_entries += 1
        else: #if cell is empty, go straight to adding a new pair
            self.list[key_index] = [nested_list]
            self.num_entries += 1

        return True #entry added successfully

    # delete a key-val pair based on given key
    def delete(self, key):
        key_index = self.get_index(key)

        if not self.list[key_index]:  # if cell is empty, immediately return (no deletion)
            return False

        # iterate through cell entries to delete entry
        for i in range(len(self.list[key_index])):
            if str(self.list[key_index][i][0]) == str(key):
                self.list[key_index].pop(i)
                return True  # successful deletion

        return "Nothing Occurred"  # key was not found, nothing was deleted

    #return val of key
    def get(self, key):
        key_index = self.get_index(str(key))
        cell = self.list[key_index]

        key = str(key).strip()

        if cell:
            for pair in cell: #search cell for a matching key, return val if key found
                pair_key = str(pair[0]).strip()
                if pair_key == key:
                    return pair[1]

        return "Nothing Found" #value was not found

    #prints all non-empty cells
    def print(self):
        print("Print HashSet")
        for cell in self.list:
            if cell:
                print(str(cell))

#class of node objects that populate the adj. matrix
class Node:
    #init. instance vars
    def __init__(self, data):
        self.data = data

#adj. matrix
class Graph:
    def __init__(self, size=27):
        self.size = size #how many nodes the adj. matrix has
        #initialize adjacency matrix with -1 (no edges)
        self.adj_matrix = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        #list to store all nodes (integer representations of locations)
        self.nodes_list = []

    #can add nodes to the adj. matrix
    def add_node(self, new_node):
        self.nodes_list.append(new_node)

    #can add edges between nodes in adj. matrix
    def add_edge(self, src, dst, value):
        self.adj_matrix[src][dst] = value

    #if possible, return the value of an edge
    def check_edge(self, src, dst):
        if self.adj_matrix[src][dst] != -1:
            return self.adj_matrix[src][dst]
        else:
            return False

    #find the closest edge, and closest node, out of the available nodes to current node
    def closest_edge(self, src, node_set):
        results = []

        #check all elements in row src
        for x in range(self.size):
            if x in node_set:
                value = float(str(self.adj_matrix[src][x]).strip())
                if value > 0:
                    edge_value = self.check_edge(src, x)
                    results.append((x, edge_value))

        #check all elements in column src
        for y in range(self.size):
            if y in node_set:
                value = float(str(self.adj_matrix[y][src]).strip())
                if value > 0:
                    edge_value = self.check_edge(y, src)
                    results.append((y, edge_value))

        #calculate the closest edge
        closest_edge = float('inf')
        closest_node = -1
        for result in results:
            float_result = float(result[1])
            if float_result < closest_edge:
                closest_edge = float_result
                closest_node = result[0]

        #print closest edge and list of all edges that were in consideration
        #print("Considerations: " + str(results))
        #print("Closest Edge:", closest_edge)

        #return both the closest edge and the node corresponding to the closest edge
        return closest_node, closest_edge

    #print the adj.matrix
    def print(self):
        print(" ", end=" ")
        for vertex in self.nodes_list:
            print(vertex.data, end=" ")
        print()

        for x in range(self.size):
            if x < len(self.nodes_list):
                row = str(self.nodes_list[x].data) + " "
            else:
                row = str(x) + " "

            for y in range(self.size):
                row += str(self.adj_matrix[x][y]) + " "
            print(row)
        print()

#truck class that represents the trucks that packages will be delivered on
class Truck:
    #class var
    speed = 18

    #init. instance vars
    def __init__(self, name):
        self.name = name
        self.packages_set = set() #packages loaded in the truck

    #how much time passed in a certain distance travelled
    @staticmethod
    def time_passed(distance):
        minutes = (distance/Truck.speed) * 60
        return minutes

    #remove package from truck and update package status to delivered
    def remove_package(self, key, status_dictionary, delivery_time):
        #creates a new set w/out the package
        self.packages_set = {package for package in self.packages_set if package[0] != key}
        status_dictionary[key] = ("Delivered", delivery_time)

    #add packages at the hub
    def add_package(self, key, hashmap):
        value = hashmap.get(key)
        if value:
            value = tuple(value)
            #convert to tuples to prevent type errors
            new_entry = (key, value)
            self.packages_set.add(new_entry)
            hashmap.delete(key) #remove package from hub, it is now loaded in the truck

    #deliver all packages in truck to their respective locations
    #returns total distance driven by truck
    def deliver_packages(self, start_time):
        distance = 0 #set initial distance
        current_node = 0 #start node
        current_time = datetime.combine(datetime.today(), start_time)
        #matched_indices = node values and package ids of packages going to those node values
        matched_indices = find_matching_indices(self.packages_set)
        #set of only the nodes the truck will visit
        node_set = set()
        for pair in matched_indices:
            node_set.add(pair[1])

        #print when deliveries started
        print("\033[1m" + self.name + " Started Deliveries At: "
              + current_time.strftime('%H:%M:%S\033[0m'))

        #status of packages in truck changed to en route when truck begins deliveries
        packages_to_en_route(self.packages_set, start_time, self.name)

        update_flag = False #once package 9 address is changed, it won't continuously be updated

        #for all nodes (locations to visit)
        while node_set:
            #start at current node and finds the closest node and edge from available options
            current_node, closest_edge = adj_matrix.closest_edge(current_node, node_set)

            #update distance after travelling to next node
            distance += closest_edge
            distance = round(distance, 2)
            #print("Distance Driven " + str(distance))

            #update time after travelling to next node
            time_passed = Truck.time_passed(closest_edge)
            tdelta = timedelta(minutes=time_passed)
            current_time = current_time + tdelta

            #grab the location name so it is known where the package is being shipped
            location_line = "" #used to hold the location name when found

            #grab location names, will be used to print with package delivery message
            try:
                with open('WGUPS Distance Table.csv', 'r') as distance_table_file:
                    distance_csv_reader = csv.reader(distance_table_file)

                    #location nodes are equivalent to indices of the CSV file
                    #grab location name if node maps to CSV index
                    for i, row in enumerate(distance_csv_reader):
                        if i == current_node:
                            combined_row = "".join(row)
                            #no address info (numbers, digits), only location names
                            location_line = re.split(r'\d+', combined_row)[0].strip()
                            break

            except FileNotFoundError:
                print("File Not Found")

            #update address for package 9 at the specified time
            update_time = time(10, 20, 0)  #time for the update
            id_to_update = 9  #package ID to update
            new_delivery_node = 19 #new delivery address
            #ensure update is not already done and it’s the right time
            if (update_flag == False
                    and current_time.time() >= update_time):
                #find package to update and update it
                for package in matched_indices:
                    if package[0] == id_to_update:
                        print("\033[92mPackage 9 Address Updated At: "
                                + str(update_time) + "\033[0m")
                        matched_indices.discard(package) #discard old package information
                        matched_indices.add((id_to_update, new_delivery_node)) #add new package info
                        update_flag = True #update has occurred

            #remove package(s) as corresponding nodes are visited (also updates package status)
            #And print package(s) delivered with delivery time
            for package in matched_indices:
                if current_node == package[1]:
                    #print package delivered with delivery time
                    #easy to print here while already iterating through packages
                    print("Package " + str(package[0]) + ": "
                          + current_time.strftime('%H:%M:%S') + ", " + location_line)
                    self.remove_package(package[0], delivered_status_dict, current_time)

            #remove most recent visited node from consideration of nodes to visit next
            node_set.remove(current_node)
            #print("Node Set: " + str(node_set))

            # if there are no nodes left to visit, return to start node
            if len(node_set) == 0:
                #find distance to hub
                last_edge = adj_matrix.closest_edge(current_node, {0})[1]
                #update distance after travelling back to hub
                distance += last_edge
                distance = round(distance, 2)
                #update time after retuning to hub
                time_passed = Truck.time_passed(last_edge)
                tdelta = timedelta(minutes=time_passed)
                current_time = current_time + tdelta
                print("\033[1m" + self.name + " Returned to Hub At: "
                      + current_time.strftime("%H:%M:%S\033[0m"))
                #final print showing total distance a truck drove
                print("\033[1m" + self.name + " Drove " + str(distance) + " Miles\033[0m\n")

        #helps to calculate total distance driven by trucks
        return distance

# -- MAIN PROGRAM -- #

#converts destination names from truck packages into indices that align with nodes in the adjacency matrix
def find_matching_indices(truck_packages):
    exclude_term = 'Salt Lake City'  #term to exclude to avoid incorrect results from overly broad matches
    matched_indices = set()  #stores tuples of package IDs and their corresponding node indices based on package locations

    #iterates through package locations and an array mapping location names to indices (node values).
    #saves the index (node value) if a location name in the truck matches a name in the location array.
    for key, package_val in truck_packages:
        for i, location in enumerate(location_list):
            if any(len(part) >= 10 and part in location and part != exclude_term for part in package_val):
                if 0 <= i < len(location_list):
                    matched_indices.add((key, i))

    #returns a set containing all corresponding node values for locations of packages in the truck passed in
    return matched_indices

def load_trucks():
    #define package IDs for each truck
    truck1_packages = [1, 13, 14, 16, 20, 22, 29, 30, 31, 34, 37, 40, 15, 19]
    truck2_packages = [3, 18, 36, 38, 6, 25, 28, 32, 26, 27, 23, 24]
    truck3_packages = [33, 35, 39, 21, 2, 4, 5, 7, 8, 9, 10, 11, 12, 17]

    #manually load the trucks
    #load truck1 - contains mostly packages that must arrive by 9 or 10:30
    for pkg_id in truck1_packages:
        truck1.add_package(pkg_id, packages)

    for pkg_id in truck2_packages:  #load truck2 - leaves at 9:05, delays truck
        truck2.add_package(pkg_id, packages)

    for pkg_id in truck3_packages:  #load truck3 - contains all EOD (end of day) packages
        truck3.add_package(pkg_id, packages)

#change package statuses from "At The Hub" to "En Route"
def packages_to_en_route(loaded_packages_set, start_time, truck_name):
    #keep track of truck number by extracting truck number from truck name and saving it in dict
    match_num = re.search(r'\d', truck_name)
    truck_number = match_num.group(0)
    for key, val in loaded_packages_set:
        en_route_status_dict[key] = ("En Route", start_time, truck_number)

#create a hashmap that will act to store all packages at the hub
packages = HashMap()

#import package file and fill hashmap with packages information (key: package ID, value: list of package info)
try:
    with open('WGUPS Package File.csv', 'r') as package_file:
        csv_reader = csv.reader(package_file)

        for line in csv_reader:
            packages.add(line[0], line[1:])
except FileNotFoundError:
    print("File Not Found")

#create a copy of the original hashmap, this way package data is preserved
packages_original = packages.copy()

#create the adjacency matrix that will be used to run nearest neighbor algorithm for delivery drivers
adj_matrix = Graph()

#import distance table
adj_matrix_size = 27 #size of adj. matrix
location_list = list(range(adj_matrix_size)) #list to hold all location names

try:
    with open('WGUPS Distance Table.csv', 'r') as distance_file:
        csv_reader = csv.reader(distance_file)

        #populate location list
        distance_counter = 0
        for line in distance_file:
            if distance_counter < len(location_list):
                location_list[distance_counter] = line.strip()
                distance_counter += 1
                #file will only be read up to the end of the location names
                if distance_counter == len(location_list):
                    break

        #populate matrix w/ location nodes
        nodes = [Node(i) for i in range(adj_matrix.size)]
        for node in nodes:
            adj_matrix.add_node(node)

        #create edges (distances in miles) between nodes
        line_counter = 0
        for line in distance_file:
            section_counter = 0
            sections = line.split(',')
            for section in sections:
                adj_matrix.add_edge(line_counter, section_counter, section)
                section_counter += 1
            line_counter += 1

        #prove each node value corresponds to its index in location list
        #node_data = [str(node.data) for node in adj_matrix.nodes_list]
except FileNotFoundError:
        print("File Not Found")

#define the time when trucks start deliveries
day_start_time = time(8, 0, 0)

#define the time that marks the start of a new day
new_day_time = time(0, 0, 0)

#all 3 dictionaries - key: package ID, value: (status, status last updated timestamp)
#all packages start off at the hub and w/ the default timestamp of midnight
hub_status_dict = {key: ("At The Hub", new_day_time) for key in range(1, packages.num_entries + 1)}

#package entries are added in here when packages begin being delivered
en_route_status_dict = {}

#package entries are added in here when packages are delivered
delivered_status_dict = {}

#create trucks
truck1 = Truck("Truck 1")
truck2 = Truck("Truck 2")
truck3 = Truck("Truck 3")

#load the trucks w/ the packages
load_trucks()

#define what time the trucks will begin delivering packages
delay_start = time(9, 5, 0)

truck1_start = datetime.combine(datetime.today(), day_start_time)
truck2_start = datetime.combine(datetime.today(), delay_start)

truck1_return_time = time(10, 9, 40)

truck3_start = datetime.combine(datetime.today(), truck1_return_time)

# -- Enter Program Here -- #
#program starts here
print("\n\033[96mPackage Delivery Simulation Started.\033[0m")
print("\n\033[1;35mWelcome\033[0m to the Single-Day Route Optimization Program!"
      "\nThis tool helps optimize the delivery routes for packages in Salt Lake City for a specific day. "
      "\nThe program ensures all deliveries meet their deadlines and keeps the total travel distance within a specified limit for the trucks, "
      "\nwhile accommodating package-specific requirements and address corrections.")

end_program = False #flag becomes true when program is terminated by user

#user can choose to run the package delivery simulation or immediately quit the program
while not end_program:
    user_input = input("\nEnter \033[31m'y'\033[0m if you would like to deliver packages. "
                       "Enter \033[31m'q'\033[0m to quit: ").strip().lower()

    if user_input == 'y': #start program if input is y
        print("\n\033[1mDelivering Packages:\033[0m\n")

        #have the trucks deliver the packages
        total_distance = round(
            truck1.deliver_packages(datetime.time(truck1_start)) +
            truck2.deliver_packages(datetime.time(truck2_start)) +
            truck3.deliver_packages(datetime.time(truck3_start)), 2)

        #print total distance driven by all trucks
        print("\033[1mTotal Distance Driven by Trucks: " + str(total_distance) + " Miles\033[0m")

    elif user_input == 'q': #end program if input is q
        print("\n\033[1;91mProgram Terminated.\033[0m")
        break

    else: #make sure input is valid
        print("\n\033[1;91mInput is invalid.\033[0m Please enter a valid input.")
        continue

    #user can view the delivery status (including the delivery time) of any package at any time
    while not end_program:
        status_input = input(
            "\033[93m\nOptions:\033[0m"
            "\nType a \033[31mtime in 24-hour format (e.g., 13:05)\033[0m to check package delivery status, "
            "\nType a \033[31mpackage ID\033[0m to view package information, "
            "\nType \033[31m'p'\033[0m to re-run the package delivery simulation, "
            "\nType \033[31m'q'\033[0m to quit: "
        )

        status_input = status_input.strip() #whitespace in user input will have no negative effect

        if status_input.lower() == 'p': #go back to package delivery simulation screen
            packages = packages_original.copy() #packages are at the hub again
            load_trucks() #packages are loaded into the trucks again
            break

        #print package information by key
        if status_input.isdigit() and 1 <= int(status_input) <= packages_original.num_entries:
            package_info = packages_original.get(status_input) #grab package info from key

            #define meaningful names for the fields in the CSV file
            #assign these names to corresponding indices in the package value list
            field_names = ["Address", "City", "State", "Zip", "Delivery Deadline", "Weight (Kilo)"]

            print("\n\033[1mPackage " + status_input + " Information:\033[0m")

            #print the standard fields
            for i, field in enumerate(field_names):
                print(f"{field}: {package_info[i]}")

            #print special notes if available
            if len(package_info) > len(field_names):
                print("Special Notes: " + package_info[6])

            continue

        if status_input.lower() == 'q': #quit the entire program
            print("\n\033[1;91mProgram Terminated.\033[0m")
            end_program = True
            break

        #convert user input into time object
        try:
            user_time = datetime.strptime(status_input, "%H:%M").time()
        except ValueError:
            print("\n\033[1;91mInput is invalid.\033[0m Please choose an option from the list.")
            continue

        #print statement that introduces list of package statuses
        print("\n\033[1mStatus of Packages at "
              + user_time.strftime("%H:%M") + "\033[0m")

        #print status of all packages based on time input
        for package_id in range(1, packages_original.num_entries + 1):
            #all packages are at the hub by default
            package_status = hub_status_dict[package_id]
            #flags indicate which status statement to print
            at_hub = True #print the package at hub statement if True
            en_route = False #print the package en route statement if True

            #times when package statuses were updated
            en_route_time = en_route_status_dict[package_id][1]
            delivered_time = delivered_status_dict[package_id][1]

            #if en_route_time is a datetime, extract the time part
            if isinstance(en_route_time, datetime):
                en_route_time = en_route_time.time()

            #if delivered_time is a datetime, extract the time part
            if isinstance(delivered_time, datetime):
                delivered_time = delivered_time.time()

            #update package status to en route
            if user_time >= en_route_time >= package_status[1]:
                package_status = en_route_status_dict[package_id]
                at_hub = False
                en_route = True

            #update package status to delivered
            if user_time >= delivered_time >= package_status[1]:
                package_status = delivered_status_dict[package_id]
                en_route = False

            #define important package status information that will be used in the print statements
            package_info_list = packages_original.get(package_id) #list of all important package info
            address = package_info_list[0] #package address
            city = package_info_list[1] #package city
            state = package_info_list[2] #package state
            zip_code = package_info_list[3] #package zipcode
            deadline = package_info_list[4] #package delivery deadline
            truck_num = en_route_status_dict[package_id][2] #number of truck

            #define ASCII color and formatting codes
            BOLD = '\033[1m'
            RESET = '\033[0m'
            LIGHT_BLUE = '\033[94m'
            YELLOW = '\033[93m'
            GREEN = '\033[92m'
            MAGENTA = '\033[35m'
            RED = '\033[91m'
            LIGHT_GRAY = '\033[1;37m'
            ITALIC = '\033[3m'

            #change package 9 print status based on time
            package_update_time = time(10, 20, 0) #time package 9 address is updated
            #print normal package address unless it is package 9 and package 9 address has been changed
            if user_time >= package_update_time and package_id == 9:
                address = location_list[19] #package 9 new address
                #only save the address part of the location
                first_digit_position = re.search(r'\d', address).start()
                address = address[first_digit_position:]

            #print package status based on the current status flags
            #the output varies depending on whether the package is at the hub, en route, or delivered
            if at_hub:
                print(
                    f"{BOLD}{package_id}{RESET}: {LIGHT_BLUE}{package_status[0]}{RESET} to Be Delivered to {ITALIC}{address}, {city}, {state}, {zip_code}{RESET} "
                    f"for {RED}{deadline}{RESET} on Truck {LIGHT_GRAY}{truck_num}{RESET}")
            elif en_route:
                print(
                    f"{BOLD}{package_id}{RESET}: {YELLOW}{package_status[0]}{RESET} to {ITALIC}{address}, {city}, {state}, {zip_code}{RESET} "
                    f"for {RED}{deadline}{RESET} on Truck {LIGHT_GRAY}{truck_num}{RESET}")
            else:
                print(
                    f"{BOLD}{package_id}{RESET}: {GREEN}{package_status[0]}{RESET} to {ITALIC}{address}, {city}, {state}, {zip_code}{RESET} "
                    f"at {MAGENTA}{delivered_time}{RESET} Before Deadline of {RED}{deadline}{RESET} on Truck {LIGHT_GRAY}{truck_num}{RESET}")