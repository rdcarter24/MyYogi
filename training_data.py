import model
import sqlalchemy
from flask import session


########## Training Data!
########## BUG!! refine flow db to allow for feedback
GOOD_WARM_UP = [[1,3,4,7,4,3,2,3,4,7,4,3,2,3,5,3,2,3,4,8,10,13,10,9,4,3,2,1,4,9,10,13,10,8,4,3,2,1],
[1,3,4,3,2,3,4,6,3,2,3,5,7,4,8,10,13,10,45,15,13,10,9,4,7,4,3,6]]

GOOD_WARRIOR = [[1,3,4,7,4,8,10,14,10,8,24,100,14,10,8,4,7,4,3,1,3,4,7,4,8,100,14,10,8,28,30,28,36,28,8,100,14,10,10,9,4,7,4,3,1],
[1,3,4,7,4,8,20,8,100,10,8,24,28,30,28,36,28,32,28,8,100,10,10,4,7,4,3,1]]

good_balance = []

good_floor_stretch = []



###### training feedback
routines = model.session.query(model.Routine).filter_by(user_id=0).all()

for routine in routines:
    warm_up_train = []
    warrior_train =[]
    for obj in routine.feedback_asanas:
        ########### posible BUG!!! links all "1"s as if continuous flow
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
    return GOOD_WARRIOR
     

