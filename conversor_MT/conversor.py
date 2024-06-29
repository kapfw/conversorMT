
import os
import sys

class Transition:
    def __init__(self, current_state, symbol_read, symbol_write, movement, dest_state):
        self.current_state = current_state
        self.symbol_read = symbol_read
        self.symbol_write = symbol_write
        self.movement = movement
        self.dest_state = dest_state

def read_input_file(file_path):
    transitions = []
    with open(file_path, 'r') as input_file:
        type_ = input_file.readline().strip()
        for line in input_file:
            parts = line.split()
            current_state = parts[0]
            symbol_read = parts[1]
            symbol_write = parts[2]
            movement = parts[3]
            dest_state = parts[4]
            transitions.append(Transition(current_state, symbol_read, symbol_write, movement, dest_state))
    return type_, transitions

def write_output_file(transitions, type_, input_file_name):
    output_file_name = input_file_name[:-4] + '.out'  # Assuming input_file_name ends with '.txt'
    with open(output_file_name, 'w') as output_file:
        if type_[1] == 'S':
            output_file.write(";I\n")
        else:
            output_file.write(";S\n")
        for transition in transitions:
            output_file.write(f"{transition.current_state} {transition.symbol_read} {transition.symbol_write} {transition.movement} {transition.dest_state}\n")

def find_transition(transitions, current_state, symbol_read, symbol_write, movement, dest_state):
    for t in transitions:
        if (t.current_state == current_state and
            t.symbol_read == symbol_read and
            t.symbol_write == symbol_write and
            t.movement == movement and
            t.dest_state == dest_state):
            return True
    return False

def rename_state(transitions, old_name, new_name):
    for t in transitions:
        if t.current_state == old_name:
            t.current_state = new_name
        if t.dest_state == old_name:
            t.dest_state = new_name

def add_transition(transitions, current_state, symbol_read, symbol_write, movement, dest_state):
    if find_transition(transitions, current_state, symbol_read, symbol_write, movement, dest_state):
        return
    transitions.append(Transition(current_state, symbol_read, symbol_write, movement, dest_state))

def sipser_to_standard_setup(transitions):
    rename_state(transitions, "0", "0_old")
    add_transition(transitions, "0", '*', '*', 'l', "1_aux")
    add_transition(transitions, "1_aux", '_', '#', 'r', "0_old")

def left_delimiter(transitions):
    for t in transitions:
        if t.movement == 'l' and t.current_state != "0":
            add_transition(transitions, t.dest_state, '#', '#', 'r', t.dest_state)

def sipser_to_standard(transitions):
    sipser_to_standard_setup(transitions)
    left_delimiter(transitions)

def standard_to_sipser_setup(transitions):
    rename_state(transitions, "0", "0_old")
    add_transition(transitions, "0", '0', '#', 'r', "1_aux")
    add_transition(transitions, "0", '1', '#', 'r', "2_aux")
    add_transition(transitions, "1_aux", '0', '0', 'r', "1_aux")
    add_transition(transitions, "1_aux", '_', '0', 'r', "3_aux")
    add_transition(transitions, "1_aux", '1', '0', 'r', "2_aux")
    add_transition(transitions, "2_aux", '0', '1', 'r', "1_aux")
    add_transition(transitions, "2_aux", '1', '1', 'r', "2_aux")
    add_transition(transitions, "2_aux", '_', '1', 'r', "3_aux")
    add_transition(transitions, "3_aux", '_', '&', 'l', "4_aux")
    add_transition(transitions, "4_aux", '*', '*', 'l', "4_aux")
    add_transition(transitions, "4_aux", '#', '#', 'r', "0_old")

def state_without_diversion(current_state, dest_state):
    if not ("right_delim" in current_state or "right_delim" in dest_state or
            "shift" in current_state or "shift" in dest_state or
            "aux" in current_state or "aux" in dest_state or
            "halt" in current_state or "halt" in dest_state):
        return True
    return False

def exists_diversion(transitions, initial_state, diversion_type):
    for t in transitions:
        if t.current_state == initial_state and diversion_type in t.dest_state:
            return True
    return False

def left_delimiter_standard(transitions):
    for i, t in enumerate(transitions):
        if (t.movement == 'l' and state_without_diversion(t.current_state, t.dest_state) and
            not exists_diversion(transitions, t.dest_state, "shift")):
            
            num = str(i)
            shift_right = f"shift_right_{num}"
            shift_1 = f"shift_1_{num}"
            shift_2 = f"shift_2_{num}"
            shift_3 = f"shift_3_{num}"
            shift_4 = f"shift_4_{num}"
            shift_final = f"shift_final_{num}"
            
            add_transition(transitions, t.dest_state, '#', '#', 'r', shift_right)
            add_transition(transitions, shift_right, '_', '_', 'r', shift_1)
            add_transition(transitions, shift_right, '0', '_', 'r', shift_2)
            add_transition(transitions, shift_right, '1', '_', 'r', shift_3)
            add_transition(transitions, shift_1, '_', '_', 'r', shift_1)
            add_transition(transitions, shift_1, '0', '_', 'r', shift_2)
            add_transition(transitions, shift_1, '1', '_', 'r', shift_3)
            add_transition(transitions, shift_1, '&', '_', 'r', shift_4)
            add_transition(transitions, shift_2, '_', '0', 'r', shift_1)
            add_transition(transitions, shift_2, '0', '0', 'r', shift_2)
            add_transition(transitions, shift_2, '1', '0', 'r', shift_3)
            add_transition(transitions, shift_2, '&', '0', 'r', shift_4)
            add_transition(transitions, shift_3, '_', '1', 'r', shift_1)
            add_transition(transitions, shift_3, '0', '1', 'r', shift_2)
            add_transition(transitions, shift_3, '1', '1', 'r', shift_3)
            add_transition(transitions, shift_3, '&', '1', 'r', shift_4)
            add_transition(transitions, shift_4, '_', '&', 'l', shift_final)
            add_transition(transitions, shift_final, '*', '*', 'l', shift_final)
            add_transition(transitions, shift_final, '#', '#', 'r', t.dest_state)

def right_delimiter_standard(transitions):
    for i, t in enumerate(transitions):
        if (t.movement == 'r' and state_without_diversion(t.current_state, t.dest_state) and
            not exists_diversion(transitions, t.dest_state, "right_delim")):
            
            num = str(i)
            right_delim = f"right_delim_{num}"
            
            add_transition(transitions, t.dest_state, '&', '_', 'r', right_delim)
            add_transition(transitions, right_delim, '_', '&', 'l', t.dest_state)

def standard_to_sipser(transitions):
    standard_to_sipser_setup(transitions)
    left_delimiter_standard(transitions)
    right_delimiter_standard(transitions)

def main(input_file):
    input_file_name = os.path.basename(input_file)  # Extract file name from path
    type_, transitions = read_input_file(input_file)
    
    if type_[1] == 'S':
        sipser_to_standard(transitions)
    else:
        standard_to_sipser(transitions)
    
    write_output_file(transitions, type_, input_file_name)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python conversor.py <input_file>")
        sys.exit(1)
    
    main(sys.argv[1])
