#!/usr/bin/env python
"""
CS 65 Lab #3 -- 5 Oct 2008
Dougal Sutherland

Implements a hidden Markov model, based on Jurafsky + Martin's presentation,
which is in turn based off work by Jason Eisner. We test our program with
data from Eisner's spreadsheets.
"""


identity = lambda x: x

class HiddenMarkovModel(object):
    """A hidden Markov model."""

    def __init__(self, states, transitions, emissions, vocab):
        """
        states - a list/tuple of states, e.g. ('start', 'hot', 'cold', 'end')
                 start state needs to be first, end state last
                 states are numbered by their order here
        transitions - the probabilities to go from one state to another
                      transitions[from_state][to_state] = prob
        emissions - the probabilities of an observation for a given state
                    emissions[state][observation] = prob
        vocab: a list/tuple of the names of observable values, in order
        """
        self.states = states
        self.real_states = states[1:-1]
        self.start_state = 0
        self.end_state = len(states) - 1
        self.transitions = transitions
        self.emissions = emissions
        self.vocab = vocab

    # functions to get stuff one-indexed
    state_num = lambda self, n: self.states[n]
    state_nums = lambda self: xrange(1, len(self.real_states) + 1)

    vocab_num = lambda self, n: self.vocab[n - 1]
    vocab_nums = lambda self: xrange(1, len(self.vocab) + 1)
    num_for_vocab = lambda self, s: self.vocab.index(s) + 1

    def transition(self, from_state, to_state):
        return self.transitions[from_state][to_state]

    def emission(self, state, observed):
        return self.emissions[state][observed - 1]


    # helper stuff
    def _normalize_observations(self, observations):
        return [None] + [self.num_for_vocab(o) if o.__class__ == str else o
                                               for o in observations]

    def _init_trellis(self, observed, forward=True, init_func=identity):
        trellis = [ [None for j in range(len(observed))]
                          for i in range(len(self.real_states) + 1) ]

        if forward:
            v = lambda s: self.transition(0, s) * self.emission(s, observed[1])
        else:
            v = lambda s: self.transition(s, self.end_state)
        init_pos = 1 if forward else -1

        for state in self.state_nums():
            trellis[state][init_pos] = init_func( v(state) )
        return trellis

    def _follow_backpointers(self, trellis, start):
        # don't bother branching
        pointer = start[0]
        seq = [pointer, self.end_state]
        for t in reversed(xrange(1, len(trellis[1]))):
            val, backs = trellis[pointer][t]
            pointer = backs[0]
            seq.insert(0, pointer)
        return seq


    # actual algorithms

    def forward_prob(self, observations, return_trellis=False):
        """
        Returns the probability of seeing the given `observations` sequence,
        using the Forward algorithm.
        """
        observed = self._normalize_observations(observations)
        trellis = self._init_trellis(observed)

        for t in range(2, len(observed)):
            for state in self.state_nums():
                trellis[state][t] = sum(
                    self.transition(old_state, state)
                        * self.emission(state, observed[t])
                        * trellis[old_state][t-1]
                    for old_state in self.state_nums()
                )
        final = sum(trellis[state][-1] * self.transition(state, -1)
                    for state in self.state_nums())
        return (final, trellis) if return_trellis else final


    def backward_prob(self, observations, return_trellis=False):
        """
        Returns the probability of seeing the given `observations` sequence,
        using the Backward algorithm.
        """
        observed = self._normalize_observations(observations)
        trellis = self._init_trellis(observed, forward=False)

        for t in reversed(range(1, len(observed) - 1)):
            for state in self.state_nums():
                trellis[state][t] = sum(
                    self.transition(state, next_state)
                        * self.emission(next_state, observed[t+1])
                        * trellis[next_state][t+1]
                    for next_state in self.state_nums()
                )
        final = sum(self.transition(0, state)
                        * self.emission(state, observed[1])
                        * trellis[state][1]
                    for state in self.state_nums())
        return (final, trellis) if return_trellis else final


    def viterbi_sequence(self, observations, return_trellis=False):
        """
        Returns the most likely sequence of hidden states, for a given
        sequence of observations. Uses the Viterbi algorithm.
        """
        observed = self._normalize_observations(observations)
        trellis = self._init_trellis(observed, init_func=lambda val: (val, [0]))

        for t in range(2, len(observed)):
            for state in self.state_nums():
                emission_prob = self.emission(state, observed[t])
                last = [(old_state, trellis[old_state][t-1][0] * \
                                    self.transition(old_state, state) * \
                                    emission_prob)
                        for old_state in self.state_nums()]
                highest = max(last, key=lambda p: p[1])[1]
                backs = [s for s, val in last if val == highest]
                trellis[state][t] = (highest, backs)

        last = [(old_state, trellis[old_state][-1][0] * \
                            self.transition(old_state, self.end_state))
                for old_state in self.state_nums()]
        highest = max(last, key = lambda p: p[1])[1]
        backs = [s for s, val in last if val == highest]
        seq = self._follow_backpointers(trellis, backs)

        return (seq, trellis) if return_trellis else seq


    def train_on_obs(self, observations, return_probs=False):
        """
        Trains the model once, using the forward-backward algorithm. This
        function returns a new HMM instance rather than modifying this one.
        """
        observed = self._normalize_observations(observations)
        forward_prob,  forwards  = self.forward_prob( observations, True)
        backward_prob, backwards = self.backward_prob(observations, True)

        # gamma values
        prob_of_state_at_time = posat = [None] + [
            [0] + [forwards[state][t] * backwards[state][t] / forward_prob
                for t in range(1, len(observations)+1)]
            for state in self.state_nums()]
        # xi values
        prob_of_transition = pot = [None] + [
            [None] + [
                [0] + [forwards[state1][t]
                        * self.transition(state1, state2)
                        * self.emission(state2, observed[t+1])
                        * backwards[state2][t+1]
                        / forward_prob
                  for t in range(1, len(observations))]
              for state2 in self.state_nums()]
          for state1 in self.state_nums()]

        # new transition probabilities
        trans = [[0 for j in range(len(self.states))]
                    for i in range(len(self.states))]
        trans[self.end_state][self.end_state] = 1

        for state in self.state_nums():
            state_prob = sum(posat[state])
            trans[0][state] = posat[state][1]
            trans[state][-1] = posat[state][-1] / state_prob
            for oth in self.state_nums():
                trans[state][oth] = sum(pot[state][oth]) / state_prob

        # new emission probabilities
        emit = [[0 for j in range(len(self.vocab))]
                   for i in range(len(self.states))]
        for state in self.state_nums():
            for output in range(1, len(self.vocab) + 1):
                n = sum(posat[state][t] for t in range(1, len(observations)+1)
                                              if observed[t] == output)
                emit[state][output-1] = n / sum(posat[state])

        trained = HiddenMarkovModel(self.states, trans, emit, self.vocab)
        return (trained, posat, pot) if return_probs else trained


# ======================
# = reading from files =
# ======================

def normalize(string):
    if '#' in string:
        string = string[:string.index('#')]
    return string.strip()

def make_hmm_from_file(f):
    def nextline():
        line = f.readline()
        if line == '': # EOF
            return None
        else:
            return normalize(line) or nextline()

    n = int(nextline())
    states = [nextline() for i in range(n)] # <3 list comprehension abuse

    num_vocab = int(nextline())
    vocab = [nextline() for i in range(num_vocab)]

    transitions = [[float(x) for x in nextline().split()] for i in range(n)]
    emissions   = [[float(x) for x in nextline().split()] for i in range(n)]

    assert nextline() is None
    return HiddenMarkovModel(states, transitions, emissions, vocab)

def read_observations_from_file(f):
    return filter(lambda x: x, [normalize(line) for line in f.readlines()])

# =========
# = tests =
# =========

import unittest
class TestHMM(unittest.TestCase):
    def setUp(self):
        # it's complicated to pass args to a testcase, so just use globals
        self.hmm = make_hmm_from_file(file(HMM_FILENAME))
        self.obs = read_observations_from_file(file(OBS_FILENAME))

    def test_forward(self):
        prob, trellis = self.hmm.forward_prob(self.obs, True)
        self.assertAlmostEqual(prob,           9.1276e-19, 21)
        self.assertAlmostEqual(trellis[1][1],  0.1,        4)
        self.assertAlmostEqual(trellis[1][3],  0.00135,    5)
        self.assertAlmostEqual(trellis[1][6],  8.71549e-5, 9)
        self.assertAlmostEqual(trellis[1][13], 5.70827e-9, 9)
        self.assertAlmostEqual(trellis[1][20], 1.3157e-10, 14)
        self.assertAlmostEqual(trellis[1][27], 3.1912e-14, 13)
        self.assertAlmostEqual(trellis[1][33], 2.0498e-18, 22)
        self.assertAlmostEqual(trellis[2][1],  0.1,        4)
        self.assertAlmostEqual(trellis[2][3],  0.03591,    5)
        self.assertAlmostEqual(trellis[2][6],  5.30337e-4, 8)
        self.assertAlmostEqual(trellis[2][13], 1.37864e-7, 11)
        self.assertAlmostEqual(trellis[2][20], 2.7819e-12, 15)
        self.assertAlmostEqual(trellis[2][27], 4.6599e-15, 18)
        self.assertAlmostEqual(trellis[2][33], 7.0777e-18, 22)

    def test_backward(self):
        prob, trellis = self.hmm.backward_prob(self.obs, True)
        self.assertAlmostEqual(prob,           9.1276e-19, 21)
        self.assertAlmostEqual(trellis[1][1],  1.1780e-18, 22)
        self.assertAlmostEqual(trellis[1][3],  7.2496e-18, 22)
        self.assertAlmostEqual(trellis[1][6],  3.3422e-16, 20)
        self.assertAlmostEqual(trellis[1][13], 3.5380e-11, 15)
        self.assertAlmostEqual(trellis[1][20], 6.77837e-9, 14)
        self.assertAlmostEqual(trellis[1][27], 1.44877e-5, 10)
        self.assertAlmostEqual(trellis[1][33], 0.1,        4)
        self.assertAlmostEqual(trellis[2][1],  7.9496e-18, 22)
        self.assertAlmostEqual(trellis[2][3],  2.5145e-17, 21)
        self.assertAlmostEqual(trellis[2][6],  1.6662e-15, 19)
        self.assertAlmostEqual(trellis[2][13], 5.1558e-12, 16)
        self.assertAlmostEqual(trellis[2][20], 7.52345e-9, 14)
        self.assertAlmostEqual(trellis[2][27], 9.66609e-5, 9)
        self.assertAlmostEqual(trellis[2][33], 0.1,        4)

    def test_viterbi(self):
        path, trellis = self.hmm.viterbi_sequence(self.obs, True)
        self.assertEqual(path, [0] + [2]*13 + [1]*14 + [2]*6 + [3])
        self.assertAlmostEqual(trellis[1][1] [0],  0.1,      4)
        self.assertAlmostEqual(trellis[1][6] [0],  5.62e-05, 7)
        self.assertAlmostEqual(trellis[1][7] [0],  4.50e-06, 8)
        self.assertAlmostEqual(trellis[1][16][0], 1.99e-09, 11)
        self.assertAlmostEqual(trellis[1][17][0], 3.18e-10, 12)
        self.assertAlmostEqual(trellis[1][23][0], 4.00e-13, 15)
        self.assertAlmostEqual(trellis[1][25][0], 1.26e-13, 15)
        self.assertAlmostEqual(trellis[1][29][0], 7.20e-17, 19)
        self.assertAlmostEqual(trellis[1][30][0], 1.15e-17, 19)
        self.assertAlmostEqual(trellis[1][32][0], 7.90e-19, 21)
        self.assertAlmostEqual(trellis[1][33][0], 1.26e-19, 21)
        self.assertAlmostEqual(trellis[2][ 1][0], 0.1,      4)
        self.assertAlmostEqual(trellis[2][ 4][0], 0.00502,  5)
        self.assertAlmostEqual(trellis[2][ 6][0], 0.00045,  5)
        self.assertAlmostEqual(trellis[2][12][0], 1.62e-07, 9)
        self.assertAlmostEqual(trellis[2][18][0], 3.18e-12, 14)
        self.assertAlmostEqual(trellis[2][19][0], 1.78e-12, 14)
        self.assertAlmostEqual(trellis[2][23][0], 5.00e-14, 16)
        self.assertAlmostEqual(trellis[2][28][0], 7.87e-16, 18)
        self.assertAlmostEqual(trellis[2][29][0], 4.41e-16, 18)
        self.assertAlmostEqual(trellis[2][30][0], 7.06e-17, 19)
        self.assertAlmostEqual(trellis[2][33][0], 1.01e-18, 20)

    def test_learning_probs(self):
        trained, gamma, xi = self.hmm.train_on_obs(self.obs, True)

        self.assertAlmostEqual(gamma[1][1],  0.129, 3)
        self.assertAlmostEqual(gamma[1][3],  0.011, 3)
        self.assertAlmostEqual(gamma[1][7],  0.022, 3)
        self.assertAlmostEqual(gamma[1][14], 0.887, 3)
        self.assertAlmostEqual(gamma[1][18], 0.994, 3)
        self.assertAlmostEqual(gamma[1][23], 0.961, 3)
        self.assertAlmostEqual(gamma[1][27], 0.507, 3)
        self.assertAlmostEqual(gamma[1][33], 0.225, 3)
        self.assertAlmostEqual(gamma[2][1],  0.871, 3)
        self.assertAlmostEqual(gamma[2][3],  0.989, 3)
        self.assertAlmostEqual(gamma[2][7],  0.978, 3)
        self.assertAlmostEqual(gamma[2][14], 0.113, 3)
        self.assertAlmostEqual(gamma[2][18], 0.006, 3)
        self.assertAlmostEqual(gamma[2][23], 0.039, 3)
        self.assertAlmostEqual(gamma[2][27], 0.493, 3)
        self.assertAlmostEqual(gamma[2][33], 0.775, 3)

        self.assertAlmostEqual(xi[1][1][1],  0.021, 3)
        self.assertAlmostEqual(xi[1][1][12], 0.128, 3)
        self.assertAlmostEqual(xi[1][1][32], 0.13,  3)
        self.assertAlmostEqual(xi[2][1][1],  0.003, 3)
        self.assertAlmostEqual(xi[2][1][22], 0.017, 3)
        self.assertAlmostEqual(xi[2][1][32], 0.095, 3)
        self.assertAlmostEqual(xi[1][2][4],  0.02,  3)
        self.assertAlmostEqual(xi[1][2][16], 0.018, 3)
        self.assertAlmostEqual(xi[1][2][29], 0.010, 3)
        self.assertAlmostEqual(xi[2][2][2],  0.972, 3)
        self.assertAlmostEqual(xi[2][2][12], 0.762, 3)
        self.assertAlmostEqual(xi[2][2][28], 0.907, 3)

    def test_learning_results(self):
        trained = self.hmm.train_on_obs(self.obs)

        tr = trained.transition
        self.assertAlmostEqual(tr(0, 0), 0,      5)
        self.assertAlmostEqual(tr(0, 1), 0.1291, 4)
        self.assertAlmostEqual(tr(0, 2), 0.8709, 4)
        self.assertAlmostEqual(tr(0, 3), 0,      4)
        self.assertAlmostEqual(tr(1, 0), 0,      5)
        self.assertAlmostEqual(tr(1, 1), 0.8757, 4)
        self.assertAlmostEqual(tr(1, 2), 0.1090, 4)
        self.assertAlmostEqual(tr(1, 3), 0.0153, 4)
        self.assertAlmostEqual(tr(2, 0), 0,      5)
        self.assertAlmostEqual(tr(2, 1), 0.0925, 4)
        self.assertAlmostEqual(tr(2, 2), 0.8652, 4)
        self.assertAlmostEqual(tr(2, 3), 0.0423, 4)
        self.assertAlmostEqual(tr(3, 0), 0,      5)
        self.assertAlmostEqual(tr(3, 1), 0,      4)
        self.assertAlmostEqual(tr(3, 2), 0,      4)
        self.assertAlmostEqual(tr(3, 3), 1,      4)

        em = trained.emission
        self.assertAlmostEqual(em(0, 1), 0,      4)
        self.assertAlmostEqual(em(0, 2), 0,      4)
        self.assertAlmostEqual(em(0, 3), 0,      4)
        self.assertAlmostEqual(em(1, 1), 0.6765, 4)
        self.assertAlmostEqual(em(1, 2), 0.2188, 4)
        self.assertAlmostEqual(em(1, 3), 0.1047, 4)
        self.assertAlmostEqual(em(2, 1), 0.0584, 4)
        self.assertAlmostEqual(em(2, 2), 0.4251, 4)
        self.assertAlmostEqual(em(2, 3), 0.5165, 4)
        self.assertAlmostEqual(em(3, 1), 0,      4)
        self.assertAlmostEqual(em(3, 2), 0,      4)
        self.assertAlmostEqual(em(3, 3), 0,      4)

        # train 9 more times
        for i in range(9):
            trained = trained.train_on_obs(self.obs)

        tr = trained.transition
        self.assertAlmostEqual(tr(0, 0), 0,      4)
        self.assertAlmostEqual(tr(0, 1), 0,      4)
        self.assertAlmostEqual(tr(0, 2), 1,      4)
        self.assertAlmostEqual(tr(0, 3), 0,      4)
        self.assertAlmostEqual(tr(1, 0), 0,      4)
        self.assertAlmostEqual(tr(1, 1), 0.9337, 4)
        self.assertAlmostEqual(tr(1, 2), 0.0663, 4)
        self.assertAlmostEqual(tr(1, 3), 0,      4)
        self.assertAlmostEqual(tr(2, 0), 0,      4)
        self.assertAlmostEqual(tr(2, 1), 0.0718, 4)
        self.assertAlmostEqual(tr(2, 2), 0.8650, 4)
        self.assertAlmostEqual(tr(2, 3), 0.0632, 4)
        self.assertAlmostEqual(tr(3, 0), 0,      4)
        self.assertAlmostEqual(tr(3, 1), 0,      4)
        self.assertAlmostEqual(tr(3, 2), 0,      4)
        self.assertAlmostEqual(tr(3, 3), 1,      4)

        em = trained.emission
        self.assertAlmostEqual(em(0, 1), 0,      4)
        self.assertAlmostEqual(em(0, 2), 0,      4)
        self.assertAlmostEqual(em(0, 3), 0,      4)
        self.assertAlmostEqual(em(1, 1), 0.6407, 4)
        self.assertAlmostEqual(em(1, 2), 0.1481, 4)
        self.assertAlmostEqual(em(1, 3), 0.2112, 4)
        self.assertAlmostEqual(em(2, 1), 0.00016,5)
        self.assertAlmostEqual(em(2, 2), 0.5341, 4)
        self.assertAlmostEqual(em(2, 3), 0.4657, 4)
        self.assertAlmostEqual(em(3, 1), 0,      4)
        self.assertAlmostEqual(em(3, 2), 0,      4)
        self.assertAlmostEqual(em(3, 3), 0,      4)

if __name__ == '__main__':
    import sys
    HMM_FILENAME = sys.argv[1] if len(sys.argv) >= 2 else 'example.hmm'
    OBS_FILENAME = sys.argv[2] if len(sys.argv) >= 3 else 'observations.txt'

    unittest.main()