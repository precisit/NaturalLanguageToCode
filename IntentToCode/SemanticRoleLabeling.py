import logging
from ObjAct import Obj, Act, Cond
from machine_learning import call_for_machine_learning_POS
import utils as utils
from nltk import word_tokenize
from pntl.tools import Annotator
from textblob import TextBlob

annotator=Annotator(senna_dir="C:/Users/desse/PycharmProjects/machine_translation_project/IntentToCode/senna-v3.0/senna",
         stp_dir="C:/Users/desse/PycharmProjects/machine_translation_project/IntentToCode/stanford-corenlp-full-2018-10-05")

def approach_two(sentence):
    logging.basicConfig(filename='SemRoleLabel.log',
                        format='%(asctime)s %(levelname)s:%(message)s',
                        level=logging.DEBUG)
    #wiki = TextBlob(sentence) #Used for correction misspelling
    #sentence = str(wiki.correct())

    logging.info("Input sentence: " + sentence)
    text = word_tokenize(sentence)

    pos_tag_result = call_for_machine_learning_POS(sentence)
    new_sentence = ''.join(word[0] + " " for word in pos_tag_result)

    annotations = annotator.get_annoations(text)
    sem_role_labels = annotations['srl']
    pos_labels = annotations['pos']
    pos_dict = {}

    logging.info("Semantic role labels")
    logging.info(sem_role_labels)
    logging.info("Part-of-speech labels")
    logging.info(pos_labels)
    objects = []
    actions = []


    utils.check_ambigous_words(pos_labels, sem_role_labels, sentence)
    print('sem: ', sem_role_labels)
    print('Network: ', pos_tag_result)
    print('pre pos: ', pos_labels)
    print('new sentence: ', new_sentence)
    #pos_labels = pos_tag_result
    for word in pos_labels:
        pos_dict[word[0].lower()] = word[1]
        if word[1].find("NN") != -1 and word[0] not in objects:
            new_obj = Obj(word[0].lower())
            objects.append(new_obj)

    direction_found = False
    found_number = False
    loop = ""

    for verb_sentence in sem_role_labels:
        if len(verb_sentence['V'].lower().split()) > 1:
            # in case of multi-word verb
            for word in verb_sentence['V'].lower().split():
                if "VB" in pos_dict[word]:
                    new_act = Act(word)
                elif utils.direction_to_vector(word):
                    new_act.set_parameter("direction", utils.direction_to_vector(word))
                    direction_found = True
        else:
            new_act = Act(verb_sentence['V'].lower())

        if "A0" in verb_sentence:
            if not any(obj.name == verb_sentence['A0'].lower().replace('the','').strip() for obj in objects):
                new_obj = Obj(verb_sentence['A0'].lower().replace('the','').strip())
                objects.append(new_obj)
            else: 
                for obj in objects:
                    if obj.name == verb_sentence['A0'].lower().replace('the','').strip():
                        new_obj = obj
                        break
            new_act.add_to_object(new_obj)

        if "A1" in verb_sentence:
            found_number = False
            words = verb_sentence['A1'].lower().split()
            for word in words:
                if utils.direction_to_vector(word) and not direction_found:
                    new_act.set_parameter("direction", utils.direction_to_vector(word))
                    direction_found = True
                elif utils.look_for_number(word, found_number, new_act, loop):
                    found_number, new_act, loop = utils.look_for_number(word, found_number, new_act, loop)
                elif pos_dict[word] == "PRP":
                    new_act.set_parameter("target", objects[-1])
                else:
                    if pos_dict[word].find("NN") != -1:
                        object_found = False
                        for li_obj in objects:
                            if li_obj.name == word:
                                param_value = li_obj
                                object_found = True
                        if not object_found and pos_dict[word.lower()] != "NNS" :
                            new_obj = Obj(word)
                            param_value = new_obj
                            objects.append(new_obj)
                        if not direction_found and pos_dict[word.lower()] != "NNS":
                            if word != 'step':  #Steps needs to be excluded from possible targets
                                new_act.set_parameter("target", param_value)


        if "A2" in verb_sentence:
            with_list = verb_sentence["A2"].split()
            if utils.direction_to_vector(verb_sentence['A2']) and not direction_found:
                new_act.set_parameter("direction", utils.direction_to_vector(verb_sentence['A2']))
            for word in with_list:
                if pos_dict[word].find("NN") != -1:
                    object_found = False
                    for li_obj in objects:
                        if li_obj.name == word:
                            param_value = li_obj
                            object_found = True
                    if not object_found:
                        new_obj = Obj(word)
                        param_value = new_obj
                        objects.append(new_obj)
                    new_act.set_parameter("with", param_value)
                if pos_dict[word] == 'CD' and utils.look_for_number(word, found_number, new_act, loop):
                    word, found_number, new_act, loop = utils.look_for_number(word, found_number, new_act, loop)
                if pos_dict[word] == "PRP":
                    new_act.set_parameter("with", objects[-1])

        #if "A3" in verb_sentence:

        if "A4" in verb_sentence:
            target_sent_list = verb_sentence["A4"].split()
            for word in target_sent_list:
                if pos_dict[word.lower()] == "RB":
                    if utils.look_for_number(word, found_number, new_act, loop):
                        found_number, new_act, loop = utils.look_for_number(word, found_number, new_act, loop)
                    if utils.direction_to_vector(word) and not direction_found:
                        new_act.set_parameter("direction", utils.direction_to_vector(word))
                        direction_found = True
                if pos_dict[word.lower()].find("NN") != -1:
                    object_found = False
                    for li_obj in objects:
                        if li_obj.name == word.lower():
                            param_value = li_obj
                            object_found = True 
                    if not object_found:
                        new_obj = Obj(word.lower())
                        param_value = new_obj
                        objects.append(new_obj)
                    if not direction_found and utils.direction_to_vector(word) :
                        new_act.set_parameter("direction", utils.direction_to_vector(word))
                        direction_found = True
                    elif  not direction_found:
                        new_act.set_parameter("target", param_value)

        if "AM-MNR" in verb_sentence:
            withaction = False
            targetaction = False
            if utils.direction_to_vector(verb_sentence['AM-MNR']) and not direction_found:
                new_act.set_parameter("direction", utils.direction_to_vector(verb_sentence['AM-MNR']))
                direction_found = True
            else:
                for word in verb_sentence["AM-MNR"].split():
                    if pos_dict[word] in ["JJ"]:
                        new_act.set_parameter("how", verb_sentence['AM-MNR'])
                    if pos_dict[word] in ["IN"]:
                        withaction = True
                    if pos_dict[word] in ["TO"]:
                        targetaction = True
                    if pos_dict[word].find("NN") != -1:
                        found_obj = False
                        for li_obj in objects:
                            if li_obj.name == word.lower():
                                found_obj = True
                                if withaction:
                                    new_act.set_parameter("with", li_obj)
                                elif targetaction:
                                    new_act.set_parameter("target", li_obj)
                                else:
                                    new_act.set_parameter("with", li_obj)
                                    new_act.set_parameter("target", li_obj)
                        if not found_obj:
                                new_obj = Obj(word)
                                new_act.set_parameter("with", new_obj)
                                objects.append(new_obj)

        if "AM-DIR" in verb_sentence:
            if utils.direction_to_vector(verb_sentence['AM-DIR']) and not direction_found:
                new_act.set_parameter("direction",utils.direction_to_vector(verb_sentence['AM-DIR']))
                direction_found = True
            else:
                dir_list = verb_sentence['AM-DIR'].split()
                for word in dir_list:
                    if pos_dict[word.lower()].find("NN") != -1:
                        object_found = False
                        for li_obj in objects:
                            if li_obj.name == word.lower():
                                param_value = li_obj
                                object_found = True 
                        if not object_found:
                            new_obj = Obj(word.lower())
                            param_value = new_obj
                            objects.append(new_obj)

                        new_act.set_parameter("target", param_value)
                        break

        if "AM-TMP" in verb_sentence:
            found_number = False
            loop = ""
            for word in verb_sentence["AM-TMP"].split():
                # Check if the word is an loop indicator
                # Should this be done using POS-tags CD and RB? 
                if utils.look_for_number(word, found_number, new_act, loop):
                    found_number, new_act, loop = utils.look_for_number(word, found_number, new_act, loop)
                if utils.direction_to_vector(word) and not direction_found:
                    new_act.set_parameter("direction", utils.direction_to_vector(word))
                    direction_found = True
                # Check if it is an until-statement
                if pos_dict[word.lower()] == "IN" and not found_number:
                    new_cond = Cond()
                    new_cond.set_type(word.lower())
                    
                    for cond_word in verb_sentence["AM-TMP"].split():
                        if pos_dict[cond_word.lower()] in ["NN", "PRP", "NNS"]:
                            obj_found = False
                            for obj in objects:
                                if obj.name == cond_word.lower(): 
                                    new_cond.set_obj(obj)
                                    obj_found = True
                            if not obj_found:
                                new_obj = Obj(cond_word.lower())
                                new_cond.set_obj(new_obj)
                                objects.append(new_obj)                   
                        if pos_dict[cond_word.lower()] in ["JJ", "VBP"]:
                            new_cond.set_nsubj(cond_word)
                    new_act.set_condition(new_cond)

        if 'AM-EXT' in verb_sentence:
            for word in verb_sentence["AM-EXT"].split():
                if word.isnumeric():
                    loop = word
                    new_act.set_loop(int(word))
                elif utils.direction_to_vector(word) and not direction_found:
                    new_act.set_parameter("direction", utils.direction_to_vector(word))
                    direction_found = True

        if "AM-ADV" in verb_sentence:
            cond_sentence = verb_sentence["AM-ADV"]
            new_cond = Cond()
            cond_list = cond_sentence.lower().split()

            for word in cond_list:
                if pos_dict[word] == "IN":
                    new_cond.set_type(word)
                if pos_dict[word] in ["NN", "PRP", "NNS"]:
                    found_obj = False
                    for li_obj in objects:
                        if li_obj.name == word.lower():
                            new_cond.set_obj(li_obj)
                            found_obj = True
                    if not found_obj:
                        new_obj = Obj(word.lower())
                        new_cond.set_obj(new_obj)
                        objects.append(new_obj)
                if pos_dict[word] == "JJ":
                    new_cond.set_nsubj(word)

                if pos_dict[word] == "VBP":
                    new_cond.set_action(word)
                    for act in actions:
                        if act.name == word:
                            actions.remove(act)
                            break
                if pos_dict[word] == "RB":
                    new_cond.set_not(True)

            new_act.set_condition(new_cond)
        actions.append(new_act)

    logging.info("Output objects:")
    logging.info(objects)
    logging.info("Output actions:")
    logging.info(actions)
    print("object: ", objects,'actions: ', actions)
    return objects, actions