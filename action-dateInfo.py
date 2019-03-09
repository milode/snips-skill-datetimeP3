#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import datetime

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()


def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)
    

def action_wrapper(hermes, intentMessage, conf):
    """ Write the body of the function that will be executed once the intent is recognized. 
    In your scope, you have the following objects : 
    - intentMessage : an object that represents the recognized intent
    - hermes : an object with methods to communicate with the MQTT bus following the hermes protocol. 
    - conf : a dictionary that holds the skills parameters you defined 
    """ 
    result_sentence = "Diese Funktion ist noch nicht vorhanden, wird aber bald hinzugefügt."
    datetype = intentMessage.slots.datetype.first().value
    print((intentMessage.slots.datetype))
    if datetype == 'weekday' or 'wochentag' in datetype:
        weekday = datetime.datetime.now().isoweekday()
        weekday_list = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        result_sentence = "Heute haben wir {weekday}.".format(weekday=weekday_list[weekday - 1])
    elif datetype == 'year':
        year = datetime.datetime.now().year
        result_sentence = "Wir sind im Jahr {year}".format(year=year)
    elif datetype == 'weeknumber' or 'kw' in datetype:
        weeknumber = datetime.datetime.now().isocalendar()[1]
        result_sentence = "Wir haben gerade die Kalenderwoche {weeknumber}".format(weeknumber=weeknumber)
    elif datetype == 'minute':
        minutes = datetime.datetime.now().minute
        result_sentence = "Wir haben die Minute {minutes}".format(minutes=minutes)
    elif datetype == 'hour':
        hours = datetime.datetime.now().hour
        result_sentence = "Wir haben gerade die Stunde {hours}".format(hours=hours)
    current_session_id = intentMessage.session_id
    hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    with Hermes("localhost:1883") as h:
        h.subscribe_intent("milode:dateInfo", subscribe_intent_callback).start()
