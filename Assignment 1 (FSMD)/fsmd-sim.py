import math
import sys
import xmltodict

if len(sys.argv) < 3:
    print('Missing arguments to start simulation')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments to start simulation.')
    sys.exit(-1)

iterations = int(sys.argv[1])

with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())

states = fsmd_des['fsmddescription']['statelist']['state']
initial_state = fsmd_des['fsmddescription']['initialstate']

inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            inputs[input_i] = 0

variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0

operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        if type(operation) is str:
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            break
        else:
            operations[operation['name']] = operation['expression']

conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            conditions[condition['name']] = condition['expression']

fsmd = {}
for state in states:
    fsmd[state] = []
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
        if type(transition) is str:
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            break
        else:
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})

def execute_setinput(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return

def execute_operation(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    return

def execute_instruction(instruction):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operations[operation])
    return
  
def evaluate_condition(condition):
    if condition == 'True' or condition=='true' or condition == 1:
        return True
    if condition == 'False' or condition=='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in conditions:
        condition_explicit = condition_explicit.replace(element, conditions[element])
    return eval(condition_explicit, merge_dicts(variables, inputs))

def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

cycle = 0
state = initial_state
print('\n\n----------------------------')
print('-----START-OF-SIMULATION----')
print('----------------------------')

repeat = True
while repeat == True:   
    try:
        if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
            for setinput in fsmd_stim['fsmdstimulus']['setinput']:
                if type(setinput) is str:
                    if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                        execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                    break
                else:
                    if int(setinput['cycle']) == cycle:
                        execute_setinput(setinput['expression'])
    except:
        pass
    
    
    s = 0
    while evaluate_condition(fsmd[state][s]["condition"]) == False:
        s = s +1
    execute_instruction(fsmd[state][s]["instruction"])
    print('\nCurrent state: ' + state)
    print('Condition(s) needed for this state: ' + fsmd[state][s]['condition'])
    print('Action(s) in this state: ' + fsmd[state][s]['instruction'])
    print('Next possible state(s): ' + fsmd[state][s]['nextstate'])
    print('Newly calculated value(s):')
    for variable in variables:
        print(' ' + str(variable)+ " = " + str(variables[variable]))
    print('\n-----------||---------------')
    print('-----------\/---------------')     
    cycle = cycle + 1
    state = fsmd[state][s]["nextstate"]
    
    if cycle > iterations:
        repeat = False
        print("\nNot enough cycles were allocated, stopping simulation...")
        sys.exit()

    try:
        if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
            if state == fsmd_stim['fsmdstimulus']['endstate']:
                print('\nCurrent state: ' + state)
                print('Condition(s) needed for this state: ' + fsmd[state][s]['condition'])
                print('Action(s) in this state: ' + fsmd[state][s]['instruction'])
                print('Next possible state(s): ' + fsmd[state][s]['nextstate'])
                print('Newly calculated value(s):')
                for variable in variables:
                    print(' ' + str(variable)+ " = " + str(variables[variable]))
                print('\n----------------------------')
                print('-------END-OF-SIMULATION----')
                print('----------------------------')
                print('\nCycles allocated for the simulation: ' + str(sys.argv[1]))
                print('\nNumber of cycles the simulation took: ' + str(cycle))
                repeat = False
    except:
        if state == states[-1]:
            print('\nCurrent state: ' + state)
            print('Condition(s) needed for this state: ' + fsmd[state][s]['condition'])
            print('Action(s) in this state: ' + fsmd[state][s]['instruction'])
            print('Next possible state(s): ' + fsmd[state][s]['nextstate'])
            print('Newly calculated value(s):')
            for variable in variables:
                print(' ' + str(variable)+ " = " + str(variables[variable]))
            print('\n----------------------------')
            print('-------END-OF-SIMULATION----')
            print('----------------------------')
            print('\nCycles allocated for the simulation: ' + str(sys.argv[1]))
            print('\nNumber of cycles the simulation took: ' + str(cycle))
            repeat = False
