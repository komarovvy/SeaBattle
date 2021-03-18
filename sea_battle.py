from sea_battle_field import SeaBattleField


def say_hello(round_counter):
    print(f"Hello at the {round_counter+1} round!")


def do_play_the_game():
    play_answer = input("Do you like to play vs. AI (y/n)? ").lower().strip()
    if play_answer == 'n':
        print("Good bye!")
        return False
    elif play_answer == 'y':
        return True
    else:
        print("Improper input. 'y' or 'n' was expected!")
        return False


def choose_human_turn():
    print("While human has the first turn...")
    return True


def show_text_fields(fld1, fld2, hidden_if_ai = True):
    print(f"{fld1.player_id} player:")
    fld1.show_text_whole(hidden=(hidden_if_ai and fld1.player_id == 'AI'))
    print(f"{fld2.player_id} player:")
    fld2.show_text_whole(hidden=(hidden_if_ai and fld2.player_id == 'AI'))


def game_round():
    global round_counter

    say_hello(round_counter)
    if not do_play_the_game():
        return False
    # Human's turn if human_turn = True, AI's turn else
    human_turn = choose_human_turn()
    humans_field = SeaBattleField("Human", manually=True)
    ai_field = SeaBattleField("AI", manually=False)

    turn_counter = 0
    show_text_fields(ai_field, humans_field)
    while humans_field.is_not_empty and ai_field.is_not_empty:
        if human_turn:
            ai_field.get_turn(manually=True)
        else:
            humans_field.get_turn(manually=False)
        turn_counter += 1
        human_turn = not human_turn
        print(f"Turn #{turn_counter//2 + 1}")
        show_text_fields(ai_field, humans_field, hidden_if_ai=False)

    if humans_field.is_empty:
        print("You loose.")
    else:
        print("You WIN!!!")
    round_counter += 1
    return True


print("Welcome to Sea Battle game!")
round_counter = 0
play_a_game = True
while play_a_game:
    play_a_game = game_round()
