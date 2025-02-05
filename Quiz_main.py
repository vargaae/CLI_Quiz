from modules import import_questions, welcome_message, cycle_through_questions, get_results


def main() -> None:
    questions_answers, nr_of_questions, max_points = import_questions(points_for_perfect = 5)
    player_name = welcome_message(nr_of_questions)
    points, nr_of_right_answers = cycle_through_questions(questions_answers)
    get_results(nr_of_questions, points, max_points, nr_of_right_answers, player_name)


if __name__ == "__main__":
    main()