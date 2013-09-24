import model
import sqlalchemy
from flask import session


########## Training Data!
########## BUG!! refine flow db to allow for feedback
GOOD_WARM_UP = [[1,3,2,3,4,7,4,3,2,3,5,7,4,8,9,11,9,11,9,12,9,32,13,11,16,8,4,3,6,3,4],
[1,3,4,7,4,8,9,12,10,32,13,11,16,8,4,7,4,3,6,3,4],[1,3,4,7,5,8,9,11,9,32,13,11,16,8,4,7,4,3,6,3,4]]

GOOD_WARRIOR = [[8,17,8,20,8,9,32,33,12,16,8,22,23,22,24,22,8,12],
[]]

GOOD_BALANCE = []

GOOD_FLOOR_STRETCH = []



###### training feedback
routines = model.session.query(model.Routine).filter_by(user_id=0).all()

for routine in routines:
    warm_up_train = []
    warrior_train =[]
    for obj in routine.feedback_asanas:
        ########### posible BUG!!! links all "1"s as if continuous flow
        #####solution while i+1 != 0
        if obj.rating == "1" and obj.sub_routine == "warm_up":
            warm_up_train.append(obj.asana_id)

        elif obj.rating == "1" and obj.sub_routine == "warrior":
            warrior_train.append(obj.asana_id)

    GOOD_WARM_UP.append(warm_up_train)
    GOOD_WARRIOR.append(warrior_train)


###### User saved feedback
def customize(user_id):
    global GOOD_WARM_UP
    global GOOD_WARRIOR


    user = model.session.query(model.User).filter_by(id=user_id).one()
    print user
    for routine in user.routines:
        warm_up_train = []
        warrior_train =[]
        for obj in routine.routine_asanas:
            if obj.sub_routine == "warm_up":
                warm_up_train.append(obj.asana_id)

            elif obj.sub_routine == "warrior":
                warrior_train.append(obj.asana_id)

        GOOD_WARM_UP.append(warm_up_train)
        GOOD_WARRIOR.append(warrior_train)

    return GOOD_WARM_UP



