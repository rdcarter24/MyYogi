import model
import random


# unit of time is breath about = 4 sec
breath = 4 
time = 2*60


# always starts with the same firstas move
first_move = model.session.query(model.Asana).get(1)
print first_move.name


prev_move = first_move
while time > 0:
    rand = random.randrange(0, model.session.query(model.Asana).count())
    next_move = model.session.query(model.Asana)[rand]
    if (next_move.position == prev_move.position or next_move.position == prev_move.position+1 or next_move.position == prev_move.position-1) and next_move.movement != prev_move.movement:
        print next_move.name
        time = time - next_move.time * breath
        prev_move = next_move