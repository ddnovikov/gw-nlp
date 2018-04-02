class SemanticKernelTagger:
    def __init__(self,
                 com_gen=None,
                 cat_gens=None,
                 top_m=50,
                 top_n=1000):
        self.top_m = top_m
        self.top_n = top_n
        self.categories = {}
        self.common = []
        if com_gen:
            self.load_common(com_gen)
        if cat_gens:
            self.load_categories(cat_gens)

    def load_common(self, gen):
        self.common = [i for i, _ in gen]

    def get_sk(self, gen):
        unigrams = [i for i, _ in gen]
        sk_n_ord = set(unigrams) - set(self.common)
        return [el for el in unigrams if el in sk_n_ord]

    def load_categories(self, gens_dict):
        for key in gens_dict.keys():
            self.categories[key] = self.get_sk(gens_dict[key])

    def _metric(self, top_input, top_supportive):
        if len(top_input):
            return (1 - (len(set(top_input) - set(top_supportive)) / float(len(top_input))))
        else:
            return -1

    def tag(self, gen):
        res = {}
        sk = self.get_sk(gen)
        for cat in self.categories.keys():
            res[cat] = self._metric(sk[:self.top_m], self.categories[cat][:self.top_n])
        return res
