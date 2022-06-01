class Human:

    def __init__(self, permutation, distance, age):

        self.perm = permutation
        self.dis = distance
        self.partners_array = []  # Future partners array
        self.age = age

    def set_human_id(self, value):  # WIELKI PLAN

        self.human_value = value

    def set_adaption_point(self, points):

        self.adap_points = points

    def set_roulette(self, roulette_prob, roulette_range_start, roulette_range_finish):

        self.roul_prob = roulette_prob  ## To cos daje??
        self.roul_start = roulette_range_start  # roulette_range_start
        self.roul_finish = roulette_range_finish  # roulette_range_finish

        """
        Problem powtarzalnosci Rozumiem że zakładamy iż jeden partner moze miec parenasie
        parnetrów podczas jednego rozmnazania? Mozemy dac zmienna boolowska by temu zapobiec
        
        """

    """
    add new sex parent to list
    """

    def set_coparent(self, coparent):

        self.partners_array.append(coparent)

    """
    remove ex-parent from list
    """

    def do_remove(self, coparent):

        self.partners_array.remove(coparent)

    """
    with who sex 
    """

    def do_sex(self):

        return self.partners_array.pop()

    """
     check if we are out
    """

    def is_empty_partners_array(self):

        if len(self.partners_array) == 0:
            return False
        else:
            return True

    def add_age(self):

        self.age += 1
