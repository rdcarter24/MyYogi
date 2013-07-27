
import warm_up_training_data
import random
#import sciplot

import model


# unit of time is breath about = 4 sec
breath = 4 
time = 2*60




def get_random_asana():
    rand = random.randrange(0, model.session.query(model.Asana).count())
    rand_asana = model.session.query(model.Asana)[rand]
    return rand_asana

def get_asana(name):
    asana = model.session.query(model.Asana).filter_by(name=name).one()
    return asana

def add_asana(name, routine):  # make number of arguments flexible (*kwargs)
    asana = model.Asana(name=name, routine=routine)
    model.session.add(asana)
    model.session.commit()
    return asana


'''
# always starts with the same first move
first_move = model.session.query(model.Asana).get(1)

prev_move = first_move


while time > 0:
    rand = random.randrange(0, model.session.query(model.Asana).count())
    next_move = model.session.query(model.Asana)[rand]
    if (next_move.position == prev_move.position or next_move.position == prev_move.position+1 or next_move.position == prev_move.position-1) and next_move.movement != prev_move.movement:
        
        time = time - next_move.time * breath
        prev_move = next_move



def rando_choice(data_list):
    num = random.randint(0, len(data_list) - 1)
    choice = data_list[num]
    return choice

########### Bigram Markov ###############

bigram_dict = {}
bigram_chain = []

for i in range(len(warm_up_training_data.good)):
    series = warm_up_training_data.good[i]
    

    for i in range(len(series)-2):
        move1 = series[i]
        move2 = series[i+1]
        move3 = series[i+2]

        key = (move1,move2)

        bigram_dict.setdefault(key,[move3]).append(move3)



start_key = (0,1)
options_list = bigram_dict[start_key]

chosen_option = rando_choice(options_list)
bigram_chain.extend([start_key[0],start_key[1],chosen_option])

new_key = (start_key[1],chosen_option)



count = 0

while count < 15:
    if new_key in bigram_dict:
        option_list = bigram_dict[new_key]

        chosen_option = rando_choice(option_list)
        bigram_chain.append(chosen_option)

        new_key = (new_key[1],chosen_option)

        count += 1
    else:
        break
print bigram_chain
'''

