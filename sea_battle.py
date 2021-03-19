from sea_battle_field import SeaBattleField


def say_hello(round_counter):
    print("\n", "-"*20, sep="")
    print(f"Round {round_counter+1}... ")


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


def show_text_fields(fld1, fld2, hidden_if_ai=True, sep="    "):
    for i, (f1_str, f2_str) in enumerate(
            zip(fld1.line_by_line(hidden_if_ai and fld1.player_id == 'AI'), 
                fld2.line_by_line(hidden_if_ai and fld2.player_id == 'AI')
                )
            ):
        if i:
            print(f1_str,sep,f2_str)
        else:
            print(fld1.player_id, 
                  " " * (len(f1_str)-len(fld1.player_id)), sep,
                  fld2.player_id)
            print(f1_str,sep,f2_str)


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
    show_text_fields(ai_field, humans_field, hidden_if_ai=True)
    while humans_field.is_not_empty and ai_field.is_not_empty:
        turn_counter += 1
        if human_turn:
            ai_field.get_turn(turn_counter, manually=True)
        else:
            humans_field.get_turn(turn_counter, manually=False)
            print(f"Turn #{turn_counter // 2 + 1}")
            show_text_fields(ai_field, humans_field, hidden_if_ai=True)
        human_turn = not human_turn

    if humans_field.is_empty:
        print("You loose.")
    else:
        print("You WIN!!!\n")
    round_counter += 1
    return True


print("Welcome to Sea Battle game!")
round_counter = 0
play_a_game = True
while play_a_game:
    play_a_game = game_round()
