import six
from future.utils import implements_iterator
from future.utils import python_2_unicode_compatible

@implements_iterator
@python_2_unicode_compatible
class Obj(object):
    """docstring for Obj"""

    def __init__(self, name):
        super(Obj, self).__init__()
        self.name = name
        self.parameters = {}
        self.isValid = False

    def set_parameter(self, param_name, param_value):
        self.parameters[param_name] = param_value

    def remove_parameter(self, param_name):
        del self.parameters[param_name]

    def make_none(self):
        del self.__dict__

    def __repr__(self):
        return_string = ""
        return_string += "Name: " + self.name + " "
        for param, param_val in six.iteritems(self.parameters):
            return_string += param + ": " + str(param_val)
        return return_string

    def __str__(self):
        return self.name

@implements_iterator
@python_2_unicode_compatible
class Act(object):
    """docstring for Act"""

    def __init__(self, name):
        super(Act, self).__init__()
        self.name = name
        self.on_object = None
        self.parameters = {}
        self.condition = None
        self.loop_iterations = 1

    def add_to_object(self, obj):
        self.on_object = obj

    def set_parameter(self, param_name, param_value):
        self.parameters[param_name] = param_value

    def remove_parameter(self, param_name):
        del self.parameters[param_name]

    def set_condition(self, cond):
        self.condition = cond

    def set_loop(self, loop_iter):
        self.loop_iterations = loop_iter

    def __repr__(self):
        return_string = self.name + "\n" + "On object: " + str(self.on_object) + "\n"
        return_string += "Loop: " + str(self.loop_iterations) + "\n"
        if self.parameters:
            return_string += "Parameters: \n"
        for param, param_val in six.iteritems(self.parameters):
            return_string += "\t" + param + ": " + str(param_val) + "\n"
        return_string += "Condition :" + str(self.condition) + "\n"
        return return_string

@implements_iterator
@python_2_unicode_compatible
class Cond(object):
    """docstring for Condition"""

    def __init__(self):
        super(Cond, self).__init__()
        self.condition_type = ""
        self.condition_obj = None
        self.condition_nsubj = ""
        self.condition_action = ""
        self.condition_not = False

    def set_type(self, cond_type):
        self.condition_type = cond_type

    def set_obj(self, cond_obj):
        self.condition_obj = cond_obj

    def set_nsubj(self, cond_nsubj):
        self.condition_nsubj = cond_nsubj

    def set_action(self, cond_action):
        self.condition_action = cond_action

    def set_not(self, cond_not):
        self.condition_not = cond_not

    def __repr__(self):
        not_string = " "
        if self.condition_not:
            not_string = " not "
        return self.condition_type + " " + self.condition_obj.name + not_string + self.condition_nsubj + self.condition_action