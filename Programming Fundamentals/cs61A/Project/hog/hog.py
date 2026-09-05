"""The Game of Hog."""

from dice import six_sided, make_test_dice
from ucb import main, trace, interact

GOAL = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1

    # 数据初始化
    is_one = False # 判断是否掷出1
    numbers = 0 # 当前投掷次数
    score = 0 # 当前分数
    result = 0 # 总分数

    # 循环模拟掷骰
    while numbers < num_rolls:
        score = dice() # 保存当前掷骰结果
        if score == 1: # 如果掷出1
            is_one = True # 标记掷出1,最后返回1
            numbers += 1 # 投掷次数加1
        else: # 如果没有掷出1
            result += score # 累加分数
            numbers += 1 # 投掷次数加1
    if is_one:
        return 1
    else:
        return result    
    # END PROBLEM 


def boar_brawl(player_score, opponent_score):
    """Return the points scored by rolling 0 dice according to Boar Brawl.

    player_score:     The total score of the current player.
    opponent_score:   The total score of the other player.

    """
    # BEGIN PROBLEM 2
    # 当前玩家的个位与对手的十位之差 → 取绝对值 → 乘以 3
    player_score = player_score % 10 # 个位 : % 取余
    opponent_score = opponent_score // 10 % 10 # 十位 : // 取整 +  % 取余
    result = abs(player_score - opponent_score) * 3

    if result == 0:
        return 1
    else:
        return result
    # END PROBLEM 2


def take_turn(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the points scored on a turn rolling NUM_ROLLS dice when the
    player has PLAYER_SCORE points and the opponent has OPPONENT_SCORE points.

    num_rolls:       The number of dice rolls that will be made.
    player_score:    The total score of the current player.
    opponent_score:  The total score of the other player.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return boar_brawl(player_score, opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def simple_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, ignoring Sus Fuss.
    """
    score = player_score + take_turn(num_rolls, player_score, opponent_score, dice)
    return score

def is_prime(n):
    """Return whether N is prime."""
    if n == 1:
        return False
    k = 2
    while k < n:
        if n % k == 0:
            return False
        k += 1
    return True

def num_factors(n):
    """Return the number of factors of N, including 1 and N itself. 
       计算一个正整数有多少个因数
       因数: 能被该数整除的数
       """
    # BEGIN PROBLEM 4
    number = 0 # 计数器
    factor = n # 因数
    while factor > 0:
        if n % factor == 0:
            number += 1
        factor -= 1
    return number 
    # END PROBLEM 4

def sus_points(score):
    """Return the new score of a player taking into account the Sus Fuss rule.
    判断分数是否触发 Sus Fuss, ()并跳到下一个质数"""
    # BEGIN PROBLEM 4
    number = num_factors(score) # 计算因数个数
    if number == 3 or number == 4:
        while is_prime(score) == False:
            score += 1
    return score    
    # END PROBLEM 4

def sus_update(num_rolls, player_score, opponent_score, dice=six_sided):
    """Return the total score of a player who starts their turn with
    PLAYER_SCORE and then rolls NUM_ROLLS DICE, *including* Sus Fuss.
    更新玩家一轮结束后的总分，并应用 Sus Fuss。
    """
    # BEGIN PROBLEM 4
    score = take_turn(num_rolls, player_score, opponent_score, dice) # 计算本轮得分
    temp_score = player_score + score # 计算本轮总分
    new_score = sus_points(temp_score) # 应用 Sus Fuss
    return new_score
    # END PROBLEM 4


def always_roll_5(score, opponent_score):
    """A strategy of always rolling 5 dice, regardless of the player's score or
    the opponent's score.
    """
    return 5


def play(strategy0, strategy1, update,
         score0=0, score1=0, dice=six_sided, goal=GOAL):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first and Player 1's score second.

    E.g., play(always_roll_5, always_roll_5, sus_update) simulates a game in
    which both players always choose to roll 5 dice on every turn and the Sus
    Fuss rule is in effect.

    A strategy function, such as always_roll_5, takes the current player's
    score and their opponent's score and returns the number of dice the current
    player chooses to roll.

    An update function, such as sus_update or simple_update, takes the number
    of dice to roll, the current player's score, the opponent's score, and the
    dice function used to simulate rolling dice. It returns the updated score
    of the current player after they take their turn.

    strategy0: The strategy for player0.
    strategy1: The strategy for player1.
    update:    The update function (used for both players).
    score0:    Starting score for Player 0
    score1:    Starting score for Player 1
    dice:      A function of zero arguments that simulates a dice roll.
    goal:      The game ends and someone wins when this score is reached.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    while score0 < goal and score1 < goal:
        if who == 0:
            # 确定玩家0的投掷次数
            num_rolls = strategy0(score0, score1)
            # 更新玩家分数
            score0 = update(num_rolls, score0, score1, dice)
            who = 1 # 切换玩家
        else:
            # 确定玩家1的投掷次数
            num_rolles = strategy1(score1, score0)
            # 更新玩家1的分数
            score1 = update(num_rolles, score1, score0, dice)  
            who = 0 # 切换玩家
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a player strategy that always rolls N dice.

    A player strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(3)
    >>> strategy(0, 0)
    3
    >>> strategy(99, 99)
    3
    """
    assert n >= 0 and n <= 10
    # BEGIN PROBLEM 6
    def  strategy(score,opponent_score): 
         return n
    return strategy
    # END PROBLEM 6


def catch_up(score, opponent_score):
    """A player strategy that always rolls 5 dice unless the opponent
    has a higher score, in which case 6 dice are rolled.

    >>> catch_up(9, 4)
    5
    >>> strategy(17, 18)
    6
    """
    if score < opponent_score:
        return 6  # Roll one more to catch up
    else:
        return 5


def is_always_roll(strategy, goal=GOAL):
    """Return whether STRATEGY always chooses the same number of dice to roll
    given a game that goes to GOAL points.

    >>> is_always_roll(always_roll_5)
    True
    >>> is_always_roll(always_roll(3))
    True
    >>> is_always_roll(catch_up)
    False
    """
    # BEGIN PROBLEM 7
    score = 0
    opponent_score = 0
    # 确定标准策略的投掷次数
    standard_rolls = strategy(score, opponent_score)
    # 外层循环代表玩家
    while score < goal :
        # 内层循环代表对手
        while opponent_score < goal :
            # 检查策略是否在不同的分数下返回相同的投掷次数
            if strategy(score, opponent_score) != standard_rolls:
                return False
            opponent_score += 1
        score += 1
        # 重置对手分数为0，开始下一轮
        opponent_score = 0
    return True
    # END PROBLEM 7


def make_averaged(original_function, samples_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    called SAMPLES_COUNT times.

    To implement this function, you will have to use *args syntax.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 40)
    >>> averaged_dice(1, dice)  # The avg of 10 4's, 10 2's, 10 5's, and 10 1's
    3.0
    """
    # BEGIN PROBLEM 8
    def averaged_function(*args):
        total = samples_count
        result = 0
        while total > 0: 
            result += original_function(*args)
            total -= 1
        return result / samples_count
    return averaged_function
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, samples_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of SAMPLES_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    
    averaged_roll_dice = make_averaged(roll_dice, samples_count) # 求平均
    best_average = averaged_roll_dice(1, dice) # 目前最高平均分
    best_num_rolls = 1 # 目前最佳投掷次数
    rolls_count = 2 # 投掷次数计数器,从2开始,因为1已经计算过了
    while rolls_count <= 10:
        current_average = averaged_roll_dice(rolls_count, dice) # 当前投递次数的平均分
        if current_average > best_average: # 如果当前平均分更高
            best_average = current_average # 更新最高平均分
            best_num_rolls = rolls_count # 更新最佳投掷次数
        rolls_count += 1 # 投掷次数加1
    return best_num_rolls

    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1, sus_update)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)

    print('always_roll(6) win rate:', average_win_rate(always_roll(6))) # near 0.5
    print('catch_up win rate:', average_win_rate(catch_up))
    print('always_roll(3) win rate:', average_win_rate(always_roll(3)))
    print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    print('boar_strategy win rate:', average_win_rate(boar_strategy))
    print('sus_strategy win rate:', average_win_rate(sus_strategy))
    print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"



def boar_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice if Boar Brawl gives at least THRESHOLD
    points, and returns NUM_ROLLS otherwise. Ignore score and Sus Fuss.
    """
    # BEGIN PROBLEM 10
    score_not_rolling = boar_brawl(score, opponent_score) # 计算不投掷骰子时的得分
    if score_not_rolling >= threshold: # 如果不投掷骰子时的
        return 0 # 返回0,不投掷骰子
    else:
        return num_rolls # 返回num_rolls,投掷骰子
    # END PROBLEM 10


def sus_strategy(score, opponent_score, threshold=11, num_rolls=6):
    """This strategy returns 0 dice when your score would increase by at least threshold."""
    # BEGIN PROBLEM 11
    zerotime_score = sus_update(0, score, opponent_score) # 计算不投掷骰子时的得分
    score_increase = zerotime_score - score # 计算得分增加量
    if score_increase >= threshold: # 如果得分增加量大于等于�
        return 0 # 返回0,不投掷骰子
    else:
        return num_rolls # 返回num_rolls,投掷骰子
    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 6  # Remove this line once implemented.
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: The function in this section does not need to be changed. It uses
# features of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()