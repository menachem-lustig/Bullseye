from fastapi import FastAPI, HTTPException
import db
import game_logic
import schema

app = FastAPI()
schema.init_db()


@app.post('/games', status_code=201)
def new_game():
    secret_code = game_logic.generate_secret_code()
    game_id = db.insert_game(secret_code)
    return {"game_id": game_id, "status": "in_progress", "attempts_used": 0}


@app.post('/games/{game_id}/guesses')
def new_guess(game_id: int, guess: dict):
    game = db.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404)
    if game['status'] != "in_progress":
        raise HTTPException(status_code=409, detail='Game has already ended')
    if 'guess' not in guess:
        raise HTTPException(status_code=422)

    valid_guess = game_logic.validate_guess(guess['guess'])
    if not valid_guess:
        raise HTTPException(status_code=422)

    secret_code = game['secret_code'].split(' ')
    bulls, hits = game_logic.score_guess(valid_guess, secret_code)
    attempts_used = game['attempts_used'] + 1

    if bulls == 4:
        status = 'won'
    elif attempts_used >= 10:
        status = 'lost'
    else:
        status = 'in_progress'

    db.update_game(game_id, attempts_used, status)
    return {"bulls": bulls, "hits": hits, "attempts_used": attempts_used}


@app.get('/games/{game_id}/status')
def get_status(game_id: int):
    game = db.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404)

    response = {
        "game_id": game['id'],
        "status": game['status'],
        "attempts_used": game['attempts_used']
    }
    if game['status'] == 'won':
        response['secret_code'] = game['secret_code'].split(' ')
    return response