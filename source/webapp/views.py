from django.shortcuts import render
from random import sample


def generate_numbers(num):
    return sample(range(1, 10), 4)


secret_nums = generate_numbers(4)
game_history = []


def game_page(request):
    if request.method == 'GET':
        return render(request, 'input_form.html')
    else:
        user_input = {
            'numbers': request.POST.get('numbers')
        }
        if user_input['numbers']:
            output = guess_numbers(secret_nums, user_input['numbers'].split())
        else:
            output = "Error! No input! (Enter 4 unique numbers in range 1 and 9)"
        context = {
            'numbers': user_input['numbers'],
            'message': output
        }
        return render(request, 'input_form.html', context)


def guess_numbers(secret, actual):
    global secret_nums
    global game_history
    if all(item.isdigit() for item in actual):
        result = list(map(int, actual))
        if len(set(result)) == len(result) and all(0 < x < 10 for x in result) and len(result) == 4:
            bulls_cows = [0, 0]
            for num1, num2 in zip(secret, result):
                if num2 in secret:
                    if num2 == num1:
                        bulls_cows[0] += 1
                    else:
                        bulls_cows[1] += 1
            if bulls_cows[0] == 4:
                secret_nums = generate_numbers(4)
                game_history = []
                return "You got it right! New Game started!"
            game_history.append(f"Bulls: {bulls_cows[0]}, Cows: {bulls_cows[1]}")
            return f"Bulls: {bulls_cows[0]}, Cows: {bulls_cows[1]}"
    return "A ValueError occurred! (Enter 4 unique numbers in range 1 and 9)"


def stats_page(request):
    current_game_history = {}
    for game_cnt, message in enumerate(game_history):
        current_game_history[game_cnt + 1] = message
    context = {'current_game_history': current_game_history}
    return render(request, 'stats.html', context)
