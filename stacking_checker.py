class Container:

  def __init__(self, id:int = -1, arrival_time:int = 0, leave_time:int = 0):
    self.id = id
    self.arrival_time = arrival_time
    self.leave_time = leave_time
    self.location = None

  def __eq__(self, other: 'Container'):
    return self.id == other.id

  def update_location(self, stack: 'Stack' = None) -> None:
    self.location = stack


class Stack:

  def __init__(self, id:int = -1, height_in:int = 1):
    self.id = id
    self.container_list = []
    self.max_height = height_in

  def place_container(self, container: Container = None) -> bool:
    # Verify that the stack is not full
    if len(self.container_list)==self.max_height:
      return False

    # Place the container on top of the stack
    self.container_list.append(container)
    container.update_location(stack=self)
    return True

  def take_container(self, container: 'Container'=None) -> bool:
    #verify that the container is on top
    top_container = self.container_list[-1]
    if container != top_container:
      return False

    # Remove the last container from the stack
    self.container_list.pop(-1)
    container.update_location(stack=None)
    return True

class StackingChecker:
  inf = 99999999
  
  def __init__(self, 
               instance_path: str = "",
               solution_str: str = ""):
    
    self.instance_path = instance_path             
    [self.nr_stacks, self.max_height] = self.get_dimensions_from_path()
    self.in_out_events = self.get_event_order()
    self.stack_list = [Stack(id=j, height_in=self.max_height) for j in range(self.nr_stacks)]
    self.container_list = []
    self.solution = self.read_solution(solution_str)
    self.log = "Simulating a solution to " + instance_path + "\r\n"
    self.score = 0

  def get_dimensions_from_path(self) -> list:
    f = open(self.instance_path, "r")
    line = f.readline()
    [part1, rest] = line.split(",")
    [part2, trash] = rest.split("\n")
    f.close()
    return [int(part1), int(part2)]

  def get_event_order(self):
    f = open(self.instance_path, "r")
    first_line = f.readline() #throwaway
    second_line = f.readline()
    f.close()
    
    split_str = second_line.split(",")
    event_list = []
    time = 0
    in_list = []

    for c in split_str:
      id = int(c)
      if id in in_list:
        event_list.append({
          'id': id,
          'is_arriving': False,
          'is_leaving': True,
          'time': time
        })
      else:
        event_list.append({
          'id': id,
          'is_arriving': True,
          'is_leaving': False,
          'time': time
        })
        in_list.append(id)
      time += 1
    return event_list

  def read_solution(self, solution_str) -> list:
    try:
      lines = solution_str.split("\r\n")
      solution_events = []
      for line in lines:
        [part1, rest] = line.split(":")
        [part2, part3] = rest.split("->")

        id = int(part1)
        if part2 == "I":
          to_stack_id = int(part3)
          solution_events.append({
            'container_id': id,
            'type': "in",
            'origin': None,
            'destination': to_stack_id
          })
        elif part3 == "U":
          from_stack_id = int(part2)
          solution_events.append({
            'container_id': id,
            'type': "out",
            'origin': from_stack_id,
            'destination': None
          })
        else:
          from_stack_id = int(part2)
          to_stack_id = int(part3)
          solution_events.append({
            'container_id': id,
            'type': "move",
            'origin': from_stack_id,
            'destination': to_stack_id
          })
        
      return solution_events
    except:
      self.log_message("Error reading solution")
      return []

  def simulate_solution(self) -> int:
    # Check parsing of the input file
    if self.solution == []:
      self.log_message("FAIL: solution was not correctly read")
      return self.inf
      
    for event in self.solution:
      self.score += 1

      if event['type'] == "move":
        try:
          container = self.container_list[event['container_id']-1]
        except:
          self.log_message("FAIL: can't find container")
          return self.inf

        if not (container.location.id + 1)== event['origin']:
          self.log_message("FAIL: can't take container form the desired stack")
          return self.inf

        if not container.location.take_container(container):
          self.log_message("FAIL: Container is not on top")
          return self.inf

        if not self.stack_list[event['destination']-1].place_container(container):
          self.log_message("FAIL: Destinationstack is full")
          return self.inf

        self.log_message("Move succeeded. Current state of the system:")
        # self.print_state()
          
      elif event['type'] == "in":
        container = Container(event['container_id'])
        if container in self.container_list:
          self.log_message("FAIL: container already exists")
          return self.inf
        else: 
          self.container_list.append(container)

        next_event = self.in_out_events.pop(0)

        if next_event['id'] != container.id:
          self.log_message("FAIL: This container should not be input next")
          return self.inf

        if not next_event['is_arriving']:
          self.log_message("FAIL: This container is not arriving")
          return self.inf
          
        try:
          if not self.stack_list[event['destination']-1].place_container(container):
            self.log_message("FAIL: Destinationstack is full")
            return self.inf
        except:
          self.log_message("FAIL: cannot find stack")
          return self.inf

        self.log_message("Arrival succeeded. Current state of the system:")
        self.log_state()
      
      elif event['type'] == "out":
        try:
          container = self.container_list[event['container_id']-1]
        except:
          self.log_message("FAIL: cannot find container")
          return self.inf

        # Take the next event from the front of the list
        next_event = self.in_out_events.pop(0)

        if next_event['id'] != container.id:
          self.log_message("FAIL: This container should not leave next")
          return self.inf

        if not next_event['is_leaving']:
          self.log_message("FAIL: This container is not leaving")
          return self.inf

        if not container.location.take_container(container):
          self.log_message("FAIL: Container is not on top")
          return self.inf
        
        self.log_message("Departure succeeded. Current state of the system:")
        self.log_state()
        
      else:
          self.log_message("FAIL: event type invalid")
          return self.inf

    if len(self.in_out_events)==0:
      return self.score
    else:
      self.log_message("FAIL: There are still containers in the terminal")
      return self.inf

  def log_message(self, message:str = "") -> None:
    self.log = self.log + message + "\r\n"

  def log_state(self):
    self.log_message("Score = " + str(self.score))
    for s in self.stack_list:
      self.log_message(str([c.id for c in s.container_list]))
    self.log_message()
  
  