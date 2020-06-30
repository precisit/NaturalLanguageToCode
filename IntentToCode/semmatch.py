"""Module Docstring"""
import logging
import six
from copy import copy
from nltk.corpus import wordnet as wn
from gensim.models import Word2Vec
from ObjAct import Obj, Act


def find_matching_object_new(obj, env_objects):
    """
    Finds existing closest of env_objects to given object obj with word2vec
    :param obj: word to be examined
    :type obj: Obj
    :param env_objects: List of possible executable objects
    :type env_objects: list[Obj]
    :return: new_obj, strongest_score
    :rtype: Obj, float
    """
    new_obj = obj
    model = Word2Vec.load("word2vec.model")
    strongest_word = None
    strongest_score = 0.0
    for env_obj in env_objects:
        res = model.wv.similarity(env_obj.name,obj.name)
        if res >= strongest_score:
            strongest_score = res
            strongest_word = env_obj
    if  strongest_score < 0.1:
        # Nothing was suitable of existing words
        logging.error("There is no " + obj.name)
        return None, 0.0
    new_obj.name = strongest_word.name
    new_obj = match_object_params(new_obj, strongest_word)
    new_obj.isValid = True
    #print("Wordnet: ", final_obj, obj_score)
    #print(new_obj, strongest_score)
    return new_obj, strongest_score

def match_object_params(original, env):
    "Match parameters of object to those of existing"
    remove_param_list = []
    for param in original.parameters:
        if param not in env.parameters:
            remove_param_list.append(param)
    for param in remove_param_list:
        original.remove_parameter(param)
    for param, param_value in six.iteritems(env.parameters):
        original.set_parameter(param, param_value)
    return original

def find_matching_action_new(act, env_acts):
    """
    Finds existing closest of env_acts to given action act with word2vec
    :param act: word to be examined
    :type act: Act
    :param env_acts: List of possible executable actions
    :type env_acts: list[Act]
    :return: new_act, strongest_score
    :rtype: Act, float
    """
    new_act = act
    model = Word2Vec.load("word2vec.model")
    strongest_action = None
    strongest_score = 0.0
    for env_act in env_acts:
        res = model.wv.similarity(env_act.name,act.name)
        if res >= strongest_score:
            strongest_score = res
            strongest_action = env_act
    #print(strongest_action.name, strongest_score)
    if  strongest_score < 0.5:
        if act.name != 'take':  #A temporary fix when take is misunderstood by the system.
            # Nothing was suitable of existing words
            logging.error("There is no " + act.name)
            return None, 0.0
        else:
            strongest_score = 1.0
            strongest_action.name = 'walk'
    new_act.name = strongest_action.name
    new_act.parameters = match_action_params(new_act.parameters, strongest_action.parameters)
    return new_act, strongest_score


def match_action_params(act_params, env_act_params):
    new_params = copy(env_act_params)
    for param_key in new_params:
        if param_key in act_params:
            new_params[param_key] = act_params[param_key]

    return new_params

def semantic_matching(objects, actions, env_objects, env_actions):
    """
    Dockstring for semantic_matching
    :param objects: Object to match
    :type sentence_terms: Obj
    :param actions: Action to match
    :type index: Act
    :return: final_objects, final_actions
    :rtype: list[Obj], list[Act]
    """
    final_objects = []
    final_actions = []
    original_obj_name = ""
    original_act_name = ""
    for obj in objects:
        original_obj_name = obj.name
        final_obj, obj_score = find_matching_object_new(obj, env_objects)
        if final_obj != None:
            logging.info(original_obj_name + ": Object match / score: " + str(final_obj.name) + " / " + str(obj_score))
            final_objects.append(final_obj)

    for act in actions:
        original_act_name = act.name
        final_act, act_score = find_matching_action_new(act, env_actions)
        if final_act != None:
            logging.info(original_act_name + ": Action match / score: " + str(final_act.name) + " / " + str(act_score))
            final_actions.append(final_act)

    return final_objects, final_actions