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


def show_text_fields(fld1, lbl1, fld2, lbl2):
    print(f"{lbl1} player:")
    fld1.show_text_whole()
    print(f"{lbl2} player:")
    fld2.show_text_whole()


def game_round():
    global round_counter

    say_hello(round_counter)
    if not do_play_the_game():
        return False
    # Human's turn if human_turn = True, AI's turn else
    human_turn = choose_human_turn()
    humans_field = SeaBattleField(manually=True)
    ai_field = SeaBattleField(manually=False)

    turn_counter = 0
    show_text_fields(ai_field, "AI", humans_field, "Human")
    while humans_field.is_not_empty and ai_field.is_not_empty:
        if human_turn:
            ai_field.get_turn(manually=True)
        else:
            humans_field.get_turn(manually=False)
        turn_counter += 1
        human_turn = not human_turn
        print(f"Turn #{turn_counter//2 + 1}")
        show_text_fields(ai_field, "AI", humans_field, "Human")

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
