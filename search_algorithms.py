from crossword import *
import copy


def satisfies_restrictions(word: Word, assigned: list, R: np.array):
    """
     It returns if the given word satisfies the restrictions of the problem, according to the variables
     previously assigned.
        Args:
            word (object of class Word): The word to check.
            assigned (list): Contains the list of the Word previously assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
        Returns:
            (bool): True if the word satisfies the restrictions.
    """

    for variable in assigned:
        if not word.is_compatible(variable, R):
            return False
    return True


"""
La meva idea és que a partir d'ara amaguem tots els mètodes de les classes, amb la funció satisfà restriccions
feta no caldria cridar res en aquelles classes per fer aquesta funció(crec)

No oblidar el que són els paràmetres, no tenen "res" a veure amb la classe crossword ara ja, al main cridariem:

    c = Crossword(a_dict_CB, a_cross_CB)
    bool, list = Backtracking( [], copy.deepcopy(c.words), copy.deepcopy(c.intersections), copy.deepcopy(c.candidates)) (copy deepcopy per si es borra algo)
    if bool:
        c.set_words(list) (si al final definim list com una llista de objectes Word, ja està implementat el set_words)

#########################################################
        JA TINC EL TEST FET --> DESCOMENTAR A TESTCASES.PY PER VEURE SI FUNCIONA
######################################################
    
"""


def backtracking_raw(assigned: list, not_assigned: list, R: np.array, C: dict):
    """
     Recursive method that will try to fill in all the whitespaces of the crossword.
        Args:
            assigned (list): Contains the list of the Word previously assigned.
            not_assigned (list): Contains the list of the Word to be assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
            R (dict): Dictionary containing all the candidates for each size.
        Returns:
            (bool): True if a solution is found.
            (list): List containing the solution (in case that it exists).
    """

    if not_assigned == []:
        return True, assigned

    word = not_assigned[0]

    for candidate in C[word.size]:
        word.set_word(candidate)

        if satisfies_restrictions(word, assigned, R):
            idx = C[word.size].index(candidate)
            C[word.size].remove(candidate)
            assigned.append(not_assigned.pop(0))
            success, result = backtracking_raw(
                assigned, not_assigned, R, C)

            if success:
                return True, result
            else:
                not_assigned.insert(0, assigned.pop())
                C[word.size].insert(idx, candidate)

    return False, []


def forward_checking(assigned_word: Word, not_assigned: list, R: np.array):
    for word in not_assigned:
        temp = []

        while word.candidates:
            c = word.candidates.pop()
            word.set_word(c)
            if assigned_word.is_compatible(word, R):
                temp.append(c)

        word.candidates = temp
        word.set_word("")


def backtracking(assigned: list, not_assigned: list, R: np.array):
    """
     Recursive method that will try to fill in all the whitespaces of the crossword.
        Args:
            assigned (list): Contains the list of the Word previously assigned.
            not_assigned (list): Contains the list of the Word to be assigned.
            R (numpy array): Matrix containing the restrictions of the problem (the intersections of the crossword).
        Returns:
            (bool): True if a solution is found.
            (list): List containing the solution (in case that it exists).
    """

    if not_assigned == []:
        return True, assigned

    new_assigned = copy.deepcopy(assigned)
    new_not_assigned = copy.deepcopy(not_assigned)
    word = new_not_assigned.pop(0)
    candidates = word.candidates

    for candidate in candidates:
        word.set_word(candidate)

        if satisfies_restrictions(word, new_assigned, R):
            new_assigned.append(word)
            candidates.remove(candidate)

            for w in new_not_assigned:
                if candidate in w.candidates:
                    w.candidates.remove(candidate)

            success, result = backtracking(new_assigned, new_not_assigned, R)

            if success:
                forward_checking(word, new_not_assigned, R)
                return True, result

    return False, []
