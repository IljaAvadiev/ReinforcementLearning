import numpy as np

###########################################################################################
# POLICY ITERATION
###########################################################################################


def policy_evaluation(pi, model, gamma=0.99, theta=1e-5):
    '''
    Calculate the value function of a given policy pi
    Args: 
        pi:      policy to be evaluated (a dictionary)
        model:   a dictionary containing the dynamics of the MDP 
        gamma:   discount factor
        theta:   threshhold value to interrupt the policy evaluation

    Returns: 
        State value function V
    '''
    nS = len(model)
    V = np.zeros(nS)
    V_old = V.copy()
    while True:
        for state in range(nS):
            action = pi[state]
            v = 0
            for prob, new_state, reward, done in model[state][action]:
                v += prob * (reward + gamma *
                             V_old[new_state] * (not done))
            V[state] = v
        max_diff = np.max(np.abs(V-V_old))
        if max_diff < theta:
            break
        V_old = V.copy()
    return V


def policy_improvement(V, model, gamma=0.99):
    '''
    Calculate an improved policy pi by acting greedily using the value function V of the current policy

    Args: 
        V:       state value function of a given policy
        model:   a dictionary containing the dynamics of the MDP 
        gamma:   discount factor

    Returns: 
        pi:      improved policy

    '''

    nS = len(model)
    nA = len(model[0])
    Q = np.zeros((nS, nA))
    for state in range(nS):
        for action in range(nA):
            for prob, new_state, reward, done in model[state][action]:
                Q[state][action] += prob * \
                    (reward + gamma * V[new_state] * (not done))
    # act greedy
    return {state: action for state,
            action in enumerate(np.argmax(Q, axis=1))}


def policy_iteration(pi, model, gamma=0.99, theta=1e-5):
    '''
    Finds an optimal policy using policy iteration

    Args: 
        pi:      starting policy
        model:   a dictionary containing the dynamics of the MDP 
        gamma:   discount factor
        theta:   threshhold value to interrupt the policy evaluation

    Returns: 
        Optimal value function and policy
    '''
    while True:
        V = policy_evaluation(pi, model, gamma, theta)
        new_pi = policy_improvement(V, model, gamma)
        if pi == new_pi:
            break
        pi = new_pi
    return V, pi


###########################################################################################
# VALUE ITERATION
###########################################################################################


def value_iteration(model, gamma=0.99, theta=1e-5):
    '''
    Finds an optimal policy using value iteration

    Args: 
        model:   a dictionary containing the dynamics of the MDP 
        gamma:   discount factor
        theta:   threshhold value to interrupt the policy evaluation

    Returns: 
        Optimal value function and policy
    '''
    nS = len(model)
    nA = len(model[0])
    V = np.zeros(nS)
    V_old = V.copy()
    while True:
        Q = np.zeros((nS, nA))
        for state in range(nS):
            for action in range(nA):
                for prob, new_state, reward, done in model[state][action]:
                    Q[state][action] += prob * \
                        (reward + gamma * V_old[new_state] * (not done))
        V = np.max(Q, axis=1)
        max_diff = np.max(np.abs(V-V_old))
        if max_diff < theta:
            break
        V_old = V.copy()

    pi = {state: action for state,
          action in enumerate(np.argmax(Q, axis=1))}

    return V, pi
