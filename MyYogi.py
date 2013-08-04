
import training_data
import random
#import sciplot
import numpy as np
import model


# unit of time is breath about = 4 sec
breath = 4 
time = 2*60


########### Functions ############

def get_random_asana():
    rand = random.randrange(0, model.session.query(model.Asana).count())
    rand_asana = model.session.query(model.Asana)[rand]
    return rand_asana

def get_asana(**kwargs):
    for key in kwargs:
        asana = model.session.query(model.Asana).filter(getattr(model.Asana,key) == kwargs[key]).first()
    return asana   

def add_asana(name, routine):  # make number of arguments flexible (*kwargs)
    asana = model.Asana(name=name, routine=routine)
    model.session.add(asana)
    model.session.commit()
    return asana





def add_user(email, password, first_name): 
    user = model.User(email=email, password=password, first_name=first_name)
    model.session.add(user)
    model.session.commit()
    return user







def rando_choice(data_list):
    num = random.randint(0, len(data_list) - 1)
    choice = data_list[num]
    return choice

def choose_ngram(w1, w2):
    rand = round(random.random(),1)
    if rand <= w1:
        return "tri"
    elif rand <= w2:
        return "quad"

def generate_routine(training_data):
    trigram_dict = {}
    trigram_chain = [] 

    for i in range(len(training_data)-2):
        move1 = training_data[i]
        move2 = training_data[i+1]
        move3 = training_data[i+2]

        key = (move1,move2)

        trigram_dict.setdefault(key,[]).append(move3)
    
   
    start_key = (training_data[0],training_data[1])
    options_list = trigram_dict[start_key]
    chosen_option = rando_choice(options_list)

    trigram_chain.extend([start_key[0],start_key[1],chosen_option])

    new_key = (start_key[1],chosen_option)



    for i in range(len(training_data)-3):
        if new_key in trigram_dict:
            option_list = trigram_dict[new_key]

            chosen_option = rando_choice(option_list)
            trigram_chain.append(chosen_option)

            new_key = (new_key[1],chosen_option)

        else:
            break
    return trigram_chain






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


'''


########### Trigram Markov ###############


class Trigram(object):
    def __init__(self):
        self.name = None


# takes in a training data set and returns a markov dictionary
    def read_training_data(self, training_data):
        trigram_dict = {}
     

        for i in range(len(training_data)-2):
            move1 = training_data[i]
            move2 = training_data[i+1]
            move3 = training_data[i+2]

            key = (move1,move2)

            trigram_dict.setdefault(key,[]).append(move3)
        
        return trigram_dict


# takes in a markov dictionary and returns a predicted yoga routine
    def make_prediction(self, d):
        trigram_chain = []

        start_key = (0,2)
        options_list = d[start_key]
        chosen_option = rando_choice(options_list)

        trigram_chain.extend([start_key[0],start_key[1],chosen_option])

        new_key = (start_key[1],chosen_option)



        for i in range(len(training_data.good_warm_up)-3):
            if new_key in d:
                option_list = d[new_key]

                chosen_option = rando_choice(option_list)
                trigram_chain.append(chosen_option)

                new_key = (new_key[1],chosen_option)

            else:
                break
        return trigram_chain





################### Quadgram Markov ###############
'''
class Quadgram(object):
    def __init__(self):
        self.name = None


# takes in a training data set and returns a markov dictionary
    def read_training_data(self, training_data):
        quadgram_dict = {}
     

        for i in range(len(training_data)-3):
            move1 = training_data[i]
            move2 = training_data[i+1]
            move3 = training_data[i+2]
            move4 = training_data[i+3]

            key = (move1, move2, move3)

            quadgram_dict.setdefault(key,[]).append(move4)

        return quadgram_dict


# takes in a markov dictionary and returns a predicted yoga routine
    def make_prediction(self, d):
        quadgram_chain = []

        start_key = (0,2,1)
        options_list = d[start_key]

        chosen_option = rando_choice(options_list)
        quadgram_chain.extend([start_key[0],start_key[1],start_key[2],chosen_option])

        new_key = (start_key[1],start_key[2],chosen_option)


        for i in range(len(training_data.good_warm_up)-4):
            if new_key in d:
                option_list = d[new_key]

                chosen_option = rando_choice(option_list)
                quadgram_chain.append(chosen_option)

                new_key = (new_key[1],new_key[2], chosen_option)

            else:
                break
        return quadgram_chain


 # create objects
trigram = Trigram()
quadgram = Quadgram()

tri_predict = trigram.make_prediction(trigram.read_training_data(training_data.good_warm_up))

quad_predict = quadgram.make_prediction(quadgram.read_training_data(training_data.good_warm_up))



#compares both methods to training data to determine error
def compare_methods(training_data):
    error_dict = {}
    error_list = []
    
    ## write test for this
    for i in np.arange(0, 1, 0.1): 
        error = 0
        for j in range(len(training_data)):

            # tri: w1 = .1, quad: w2 = .9
            # if choose_ngram <= w1 go with tri
            if choose_ngram(i, 1-i) == "tri":
                if tri_predict[j] != training_data[j]:
                    error += 1
            else:
                if quad_predict[j] != training_data[j]:
                    error += 1
        error_dict[(round(i, 1), round(1-i, 1))] = error
        error_list.append((round(i, 1), round(1-i, 1)))
    

 
    # find weights with the lowest error
    return min(error_dict.items(), key=lambda x: x[1])[0]

compare_methods(training_data.good_warm_up)


################# ngram class
 
class Ngram(object,n):
    def __init__(self):
        self.n = None


# takes in a training data set and returns a markov dictionary
    def read_training_data(self, training_data):
        ngram_dict = {}
      #n=3

        for i in range(len(training_data)-(n-1)):
            for j in range(1, n)
                move n = training_data[i+(n-1)]
                move2 = training_data[i+1]
                move3 = training_data[i+2]

                key = (move1,move2)

                trigram_dict.setdefault(key,[]).append(move3)
            
        return trigram_dict


# takes in a markov dictionary and returns a predicted yoga routine
    def make_prediction(self, d):
        trigram_chain = []

        start_key = (0,2)
        options_list = d[start_key]
        chosen_option = rando_choice(options_list)

        trigram_chain.extend([start_key[0],start_key[1],chosen_option])

        new_key = (start_key[1],chosen_option)



        for i in range(len(training_data.good_warm_up)-3):
            if new_key in d:
                option_list = d[new_key]

                chosen_option = rando_choice(option_list)
                trigram_chain.append(chosen_option)

                new_key = (new_key[1],chosen_option)

            else:
                break
        return trigram_chain

'''