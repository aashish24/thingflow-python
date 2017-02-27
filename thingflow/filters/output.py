# Copyright 2016 by MPI-SWS and Data-Ken Research.
# Licensed under the Apache 2.0 License.
from sys import stdout

from thingflow.base import OutputThing, XformOrDropFilter, filtermethod

class Output(XformOrDropFilter):
    def __init__(self, previous_in_chain, file=stdout):
        super().__init__(previous_in_chain)
        self.file = file

    def _filter(self, x):
        print(x, file=self.file)
        return x

    def on_error(self, e):
        print(e, file=self.file)
        self._dispatch_error(e)

@filtermethod(OutputThing)
def output(this, file=stdout):
    """Print each element of the sequence. Exceptions are printed
    as well. We don't call it print, because that will override the
    built-in print function.
    """
    return Output(this, name="output")

class OutputCount(XformOrDropFilter):
    def __init__(self, previous_in_chain, file=stdout):
        super().__init__(previous_in_chain)
        self.file = file
        self.count = 0

    def _filter(self, x):
        self.count += 1
        return x

    def on_completed(self):
        msg = "*      %d events processed      *" % self.count
        print('*'*len(msg), file=self.file)
        print(msg, file=self.file)
        print('*'*len(msg), file=self.file)
        self._dispatch_completed()
        
@filtermethod(OutputThing)
def output_count(this, file=stdout):
    """Just count the number of events and print out a banner with the
    total at the end.
    """
    return OutputCount(this, file=file)
