class Pipeline:
    '''
    A class that can be used for wrapping lots of preprocessing
    functions in one pipeline.
    '''

    def __init__(self, steps):
        self.steps = steps

    def __repr__(self):
        return f'Pipeline(steps={self.steps})'

    def __bool__(self):
        return bool(self.steps)

    def __len__(self):
        return len(self.steps)

    def __add__(self, other):
        if isinstance(other, tuple):
            return Pipeline(steps=self.steps + [other])

        elif isinstance(other, list):
            return Pipeline(steps=self.steps + other)

        elif isinstance(other, Pipeline):
            return Pipeline(steps=self.steps + other.steps)

        else:
            raise

    def __eq__(self, other):
        return self.steps == other.steps

    def __ne__(self, other):
        return self.steps != other.steps

    def apply(self, input_):
        res = input_
        for func, kwargs, input_arg_name in self.steps:
            cur_kwargs = dict(**{input_arg_name: res}, **kwargs)
            res = func(**cur_kwargs)
        return res
