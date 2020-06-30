from __future__ import print_function
from flask import Flask, request, render_template
from flask_restful import Resource, Api
import logging

from ObjAct import Act, Obj
from semmatch import semantic_matching
from SemanticRoleLabeling import approach_two
from GenerateCode_js import generate_code

APP = Flask(__name__)
API = Api(APP)

ENV_OBJECT_ONE = Obj("character")
ENV_OBJECT_TWO = Obj("tree")
ENV_OBJECT_THREE = Obj("axe")
ENV_OBJECT_FOUR = Obj("cow")
ENV_OBJECT_FIVE = Obj("goal")

ENV_OBJECTS = [ENV_OBJECT_ONE, ENV_OBJECT_TWO, ENV_OBJECT_THREE, ENV_OBJECT_FOUR, ENV_OBJECT_FIVE]

ENV_ACTION_ONE = Act("walk")
ENV_ACTION_ONE.set_parameter("direction", "right")
ENV_ACTION_ONE.set_parameter("target", None)

ENV_ACTION_TWO = Act("jump")
ENV_ACTION_TWO.set_parameter("direction", "right")
ENV_ACTION_TWO.set_parameter("target", None)

ENV_ACTION_THREE = Act("cut")
ENV_ACTION_THREE.set_parameter("target", "")
ENV_ACTION_THREE.set_parameter("with", "")

ENV_ACTION_FOUR = Act("eat")
ENV_ACTION_FOUR.set_parameter("target", "")

ENV_ACTIONS = [ENV_ACTION_ONE, ENV_ACTION_TWO, ENV_ACTION_THREE, ENV_ACTION_FOUR]


class Get_Code(Resource):
    def post(self):
        if request.form['data']:
            obj, act = approach_two(request.form['data'])
            logging.info("--------------------- AFTER MATCHING ----------------------")
            matched_objects, matched_actions = semantic_matching(obj, act, ENV_OBJECTS, ENV_ACTIONS)
            logging.info(matched_objects)
            logging.info(matched_actions)
            generated_code = generate_code(matched_objects, matched_actions)
            logging.info("Generated code: " + generated_code)
            return {'code': generated_code}
        else:
            return {'NO! WHAT IS THIS?! :': request.form}


API.add_resource(Get_Code, '/getcode')


@APP.route('/')
def main():
    return render_template('index_game.html')


if __name__ == '__main__':
    APP.run(debug=True)
