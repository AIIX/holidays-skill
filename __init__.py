import sys
import json
import requests
import pycountry
import dateutil.parser

from os.path import dirname, join
from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.messagebus.message import Message

class HolidaySkill(MycroftSkill):
    """ 
    Holiday Skill
    """
    @intent_file_handler('get.holidays.intent')
    def handle_get_holidays_intent(self, message):
        """ 
        Get Holidays Intent
        """
        holidayIndexKey = "bb1a10ab5d14d11b3e3c7ff19649ea2d428a44f8"
        country = message.data['country']
        countryCode = self.getCountryCode(country)
        year = message.data['year']
        try:
            method = "GET"
            app_country = countryCode
            app_year = year
            format_url = "https://www.calendarindex.com/api/v1/holidays?country={0}&year={1}&api_key={2}".format(app_country, app_year, holidayIndexKey)
            response = requests.request(method, format_url)
            globalResult = response.json()
            for x in globalResult['response']['holidays']:
                dateDayString = dateutil.parser.parse(x['start']).strftime("%A")
                dateDayInt = dateutil.parser.parse(x['start']).strftime("%d")
                dateMonth = dateutil.parser.parse(x['start']).strftime("%B")
                dateYear = dateutil.parser.parse(x['start']).strftime("%Y")
                speakresult = x['name'], "|",  dateDayString, "|", dateDayInt, "of" ,  dateMonth, "in", dateYear, "|", x['type']
                self.speak(speakresult)
            self.gui['holidayListBlob'] = globalResult
            self.gui.show_page("holidaylist.qml")

        except:
            notFoundMessage = "I couldn't find any holiday listing".format(person_name)
            self.speak(notFoundMessage)
            
    def getCountryCode(self, country):
        try:
            country_code = pycountry.countries.get(name=country).alpha_2
            return country_code
        except:
            self.speak("Couldn't find country code")
            self.stop()
    
    def stop(self):
        pass


def create_skill():
    return HolidaySkill()
