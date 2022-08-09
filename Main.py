import numpy as np
import matplotlib.pyplot as plt
import pygame
import time


def Q(q_table, current_state, action, reward, next_state, learning_rate, discount_rate):
    """
    Function to update the Q table.
    :param q_table:
    :param current_state:
    :param action:
    :param reward:
    :param next_state:
    :param learning_rate:
    :param discount_rate:
    :return:
    """
    if next_state == 5:
        next_state = 4
    print(
        q_table, current_state, action, reward, next_state, learning_rate, discount_rate
    )
    e = q_table[current_state][action] + learning_rate * (
            reward
            + discount_rate * max(q_table[next_state])
            - q_table[current_state][action]
    )
    q_table[current_state][action] = e
    return q_table


def action(q_table, state):
    """
    Function to choose an action.
    :param q_table:
    :param state:
    :return:
    """
    if q_table[state][1] > q_table[state][0]:
        print("Right")
        # 10% chance of moving left
        if np.random.randint(0, 10) == 1 or 2:
            return 0
        return 1
    elif q_table[state][0] > q_table[state][1]:
        print("0")
        if np.random.randint(0, 10) == 1 or 2:
            return 1
        return 0
    elif q_table[state][0] == q_table[state][1]:
        print("Random")
        return np.random.choice([0, 1])


def main(reward, env, ep, gui):
    """
    Main function for the game.
    :param reward:
    :param env:
    :param ep:
    :param gui:
    :return: left and right
    """
    l, r = 0, 0
    state = 0

    q_table = np.array([[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]])
    learning_rate = 0.1
    discount_rate = 0.9

    for i in range(ep):
        actions = action(q_table, state)

        if actions == 1:
            print("Right")
            r += 1
            next_state = state + 1
            q_table = Q(
                q_table, state, actions, 0, next_state, learning_rate, discount_rate
            )
            if state < 4:
                env[state] = ""
                state += 1
                env[state] = PLAYER
                if gui:
                    screen.blit(background, (0, 0))
                    screen.blit(char, (state * 200, 80))
                    time.sleep(1)
                    pygame.display.update()
            else:
                q_table = Q(
                    q_table,
                    state,
                    actions,
                    10,
                    next_state,
                    learning_rate,
                    discount_rate,
                )

                reward += 10
        if actions == 0:
            print("Left")
            l += 1
            q_table = Q(q_table, state, actions, 2, 0, learning_rate, discount_rate)
            print(q_table)
            reward += 2
            state = 0

            if gui:
                screen.blit(background, (0, 0))
                screen.blit(char, (100, 80))
                time.sleep(1)
                pygame.display.update()
        env = np.array(["", "", "", "", ""])
        env[state] = PLAYER
        print(env)
        print("Reward", reward)
        print(q_table)
    return l, r


if __name__ == "__main__":
    ### HYPER PARAMETERS ###
    state = 0
    reward = 0
    env = np.array(["", "", "", "", ""])
    PLAYER = "*"
    gui = False
    epochs = 1000

    if gui:
        pygame.init()
        screen = pygame.display.set_mode((950, 185))
        pygame.display.set_caption("Q Learning")
        background = pygame.image.load("GUI/Background.png")
        char = pygame.image.load("GUI/Char.png")
        char = pygame.transform.scale(char, (50, 50))
    print(f"Left:{main(reward, env, epochs, gui)[0]}\nRight:{main(reward, env, 10000, gui)[1]}")
