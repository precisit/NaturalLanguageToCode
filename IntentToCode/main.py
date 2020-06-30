import sys
import logging
from ObjAct import Obj, Act
from semmatch import semantic_matching
from SemanticRoleLabeling import approach_two
from GenerateCode_python import generate_code

ENV_OBJECT_ONE = Obj("character")
ENV_OBJECT_ONE.set_parameter("position", (5, 10))

ENV_OBJECT_TWO = Obj("tree")
ENV_OBJECT_TWO.set_parameter("position", (7, 12))

ENV_OBJECT_THREE = Obj("axe")

ENV_OBJECT_FOUR = Obj("cow")

ENV_OBJECT_FIVE = Obj("johanna")

ENV_OBJECTS = [ENV_OBJECT_ONE, ENV_OBJECT_TWO, ENV_OBJECT_THREE, ENV_OBJECT_FOUR, ENV_OBJECT_FIVE]

ENV_ACTION_ONE = Act("hit")
ENV_ACTION_ONE.set_parameter("target", None)
ENV_ACTION_ONE.set_parameter("with", None)

ENV_ACTION_TWO = Act("walk")
ENV_ACTION_TWO.set_parameter("direction", "right")
ENV_ACTION_TWO.set_parameter("target", None)

ENV_ACTION_THREE = Act("jump")
ENV_ACTION_THREE.set_parameter("how", "low")

ENV_ACTION_FOUR = Act("wave")

ENV_ACTION_FIVE = Act("cut")
ENV_ACTION_FIVE.set_parameter("target", None)
ENV_ACTION_FIVE.set_parameter("with", None)

ENV_ACTION_SIX = Act("eat")

ENV_ACTION_SEVEN = Act("turn")
ENV_ACTION_SEVEN.set_parameter("direction", None)

ENV_ACTIONS = [ENV_ACTION_ONE, ENV_ACTION_TWO, ENV_ACTION_THREE, ENV_ACTION_FOUR, ENV_ACTION_FIVE, ENV_ACTION_SIX]


if len(sys.argv) > 1:
    print( "Test started.")
    with open('test_data.txt', 'r') as f:
        for sent in f:
            print(sent)
            if sys.argv[1] == "2":
                obj, act = approach_two(sent)
                logging.info("--------------------- AFTER MATCHING ----------------------")
                matched_objects, matched_actions = semantic_matching(obj, act, ENV_OBJECTS, ENV_ACTIONS)
                logging.info(matched_objects)
                logging.info(matched_actions)
                generated_code = generate_code(matched_objects, matched_actions)
                logging.info("Generated code: " + generated_code)
                print(generated_code)
    print("Test complete.")

else: 
    print("Needs parameter Test: 1 or 2")