
import training_data
import random
#import sciplot
import model



########### Query Functions ############
###### Asanas

####### BUG!!! get random asana based on routine
def get_random_asana(sub_routine, position):
    rand_asana = model.session.query(model.Asana).filter_by(sub_routine = sub_routine).filter_by(position=position).all()
    print len(rand_asana)
    rand =  random.randrange(0,len(rand_asana))
    return rand_asana[rand]

def get_asana(**kwargs):
    for key in kwargs:
        asana = model.session.query(model.Asana).filter(getattr(model.Asana,key) == kwargs[key]).first()
    return asana

def add_asana(name, routine):  # make number of arguments flexible (*kwargs)
    asana = model.Asana(name=name, routine=routine)
    model.session.add(asana)
    model.session.commit()
    return asana

######## Flows
def get_flow(**kwargs):
    for key in kwargs:
        flow = model.session.query(model.Flow).filter(getattr(model.Flow,key) == kwargs[key]).all()
    return flow

######## Users
def get_user(**kwargs):
    for key in kwargs:
        user = model.session.query(model.User).filter(getattr(model.User,key) == kwargs[key]).first()
    if user:
        return user
    else:
        return None

def add_user(email, password, username):
    user = model.User(email=email, password=password, username=username)
    model.session.add(user)
    model.session.commit()
    return user

########## Routine

def save_routine(name, user_id):  # make number of arguments flexible (*kwargs)
    routine = model.Routine(name=name, user_id=user_id)
    model.session.add(routine)
    model.session.commit()
    return routine

def save_routine_asana(asana_id, routine_id, order, sub_routine):
    routine_asana = model.Routine_Asana(asana_id=asana_id, routine_id=routine_id, order=order, sub_routine=sub_routine)
    model.session.add(routine_asana)
    model.session.commit()
    return

def get_routine(routine_id):
    routine = model.session.query(model.Routine_Asana).filter_by(routine_id = routine_id).all()
    return routine

######## BUG!! maybe add an order
def train_routine_asana(asana_id, routine_id, sub_routine, rating):
    train_routine_asana = model.Feedback_Asana(asana_id=asana_id, routine_id=routine_id, sub_routine=sub_routine, rating=rating)
    model.session.add(train_routine_asana)
    model.session.commit()
    return

############# Helper Functions ############
def rando_choice(data_list):
    num = random.randint(0, len(data_list) - 1)
    choice = data_list[num]
    return choice


###### need to carry "breaths" after implementing this
def time_variance(obj):
    rand = round(random.random(),1)
    num = random.randint(0,len(obj.variance))
    if rand > .5:
        time = obj.breaths + num
    else:
        time = obj.breaths - num


def coin_toss(input):
    rand = round(random.random(),1)
    if rand <= input:
        return True
    else:
        return False


def generate_routine(training_data, time, sub_routine):
    trigram_dict = {}
    trigram_chain = []

    # convert given time in min to number of breaths
    time_in_sec = time * 60
    breath = 4
    num_breaths = time_in_sec/breath
    breaths = 0

    ############  Set up dictionary
    for i in range(len(training_data)):
        for j in range(len(training_data[i])-2):
            asana1 = training_data[i][j]
            asana2 = training_data[i][j+1]
            asana3 = training_data[i][j+2]

            key = (asana1, asana2)
            trigram_dict.setdefault(key,[]).append(asana3)

    ########### Build list of tuples (obj, obj.time)
    start_key = (training_data[0][0], training_data[0][1])
    print training_data[0][0]
    first_asana = get_asana(id=start_key[0])
    breaths += first_asana.breaths
    sec_asana = get_asana(id=start_key[1])
    breaths += sec_asana.breaths
    trigram_chain.extend([(first_asana,first_asana.breaths),(sec_asana,sec_asana.breaths)])

    options_list = trigram_dict[start_key]
    chosen_option = rando_choice(options_list)

    ########## Check if option is an asana or flow
    if chosen_option >= 100:
        flow = get_flow(flow_id=chosen_option)
        for chosen_option in flow:
            breaths += chosen_option.breaths
            trigram_chain.append((chosen_option.asana, chosen_option.breaths))
        new_key = (flow[-2].asana.id, flow[-1][0].asana.id)
    else:
        third_asana = get_asana(id=chosen_option)
        trigram_chain.append((third_asana, third_asana.breaths))
        new_key = (start_key[1], chosen_option)

    while breaths <= num_breaths:
        if new_key in trigram_dict:
            option_list = trigram_dict[new_key]
            chosen_option = rando_choice(option_list)

            if coin_toss(.1) == True: # gets a random asana on occasion
                asana = get_random_asana(sub_routine, trigram_chain[-1][0].position)

                breaths += asana.breaths
                trigram_chain.append((asana, asana.breaths))
                chosen_option = asana.id
            elif chosen_option >= 100:
                flow = get_flow(flow_id=chosen_option)
                for asana in flow:
                    breaths += asana.breaths
                    trigram_chain.append((asana.asana, asana.breaths))
            else:
                asana = get_asana(id=chosen_option)
                breaths += asana.breaths
                trigram_chain.append((asana, asana.breaths))
            new_key = (new_key[1],chosen_option)
        else:
            # BUG!!!   its pooping out if new_key is not in trigram_dict
            break

    return (trigram_chain, sub_routine)



########### Build Up Routine with sub routines#########

def get_yoga_routine(training_data, user_id):
    routine = []

    warm_up = generate_routine(training_data.customize(user_id), 1, "warm_up")

    #warrior = generate_routine(training_data.customize(user_id), 1, "warrior")


    routine.append(warm_up)
    #routine.append(warrior)

    return routine


'''
    sun_salutation = query #flow database for sun salutaion
    #warrior series needs to repeat on both sides

    one_side = generate_routine(training_data.good_warrior, 7)

    vinyasa = query #flow database for vinyasa or other flow sequence

    other_side = one_side # work out how to do mirror

    balance = generate_routine(training_data.good_balance, 10)

    floor_stretch = generate_routine(training_data.good_floor_balance, 10)

    savasana =  query # asana database for savasana

    return warm_up + sun_salutation + one_side + vinyasa + other_side + balance
    + floor_stretch + savasana








########### Trigram Markov ###############


# class Trigram(object):
#     def __init__(self):
#         self.name = None


# # takes in a training data set and returns a markov dictionary
#     def read_training_data(self, training_data):
#         trigram_dict = {}


#         for i in range(len(training_data)-2):
#             move1 = training_data[i]
#             move2 = training_data[i+1]
#             move3 = training_data[i+2]

#             key = (move1,move2)

#             trigram_dict.setdefault(key,[]).append(move3)

#         return trigram_dict


# # takes in a markov dictionary and returns a predicted yoga routine
#     def make_prediction(self, d):
#         trigram_chain = []

#         start_key = (0,2)
#         options_list = d[start_key]
#         chosen_option = rando_choice(options_list)

#         trigram_chain.extend([start_key[0],start_key[1],chosen_option])

#         new_key = (start_key[1],chosen_option)



#         for i in range(len(training_data.good_warm_up)-3):
#             if new_key in d:
#                 option_list = d[new_key]

#                 chosen_option = rando_choice(option_list)
#                 trigram_chain.append(chosen_option)

#                 new_key = (new_key[1],chosen_option)

#             else:
#                 break
#         return trigram_chain





################### Quadgram Markov ###############

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

'''