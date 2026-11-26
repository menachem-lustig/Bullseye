from fastapi import FastAPI,HTTPException
import db
import game_logic

app = FastAPI()

@app.post('/games',status_code=201)
def new_game():
    secret_code = game_logic.generate_secret_code()
    game_id = db.insert_game(secret_code)
    return {"game_id": game_id, "status": "in_progress", "attempts_used": 0} 

@app.post('/games/{game_id}/guesses')
def new_guess(game_id,guess):
    game= db.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404)
    if game['status'] != "in_progress":
        raise HTTPException(status_code=409,detail='Game has already ended')
    guess_dict = dict(guess)
    if not game_logic.validate_guess(guess_dict['guess']):
        raise HTTPException(status_code=422)
    secret_code= game['secret_code'].split(' ')
    bools,hint = game_logic.score_guess(guess_dict['guess'] ,secret_code)
    if bools == 4:
        status = 'won'
    # db.update_game(1,)
    
