#imports
import gesture_box as gesture
import json
import urllib2
import calendar_part
import pingpong
import threading
import traceback
import requests
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.factory import Factory 
from kivy.uix.listview import ListItemButton
from kivy.storage.jsonstore import JsonStore
from kivy.network.urlrequest import UrlRequest
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.modernmenu import MenuSpawner,ModernMenu
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle,Color
from kivy.garden.moretransitions import RippleTransition
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty
from urllib import urlopen
from kivy.animation import Animation
import datetime
from os.path import exists
from plyer import orientation
from kivy.graphics import Color, Ellipse, Line
from random import random

from kivy.utils import platform
from kivy.config import Config

#Loading files
Builder.load_file('StatusBar.kv')
Builder.load_file('Locations.kv')
Builder.load_file('Current.kv')
Builder.load_file('WholeWeek.kv')

Builder.load_file('calendar_part.kv')
Builder.load_file('months.kv')
Builder.load_file('dates.kv')
Builder.load_file('select.kv')
Builder.load_file('days.kv')

Builder.load_file('pingpong.kv')



if platform == 'linux':
    print "its linux"

#global variable
try:
    variable_for_ping_pong_gesture = 0
    name_file = open("global_name.json","r")
    getname = json.load(name_file)
except:
    getname = 'Jaipur(IN)'

class HelpDialog(Popup):
    rst = ObjectProperty(None)
    
    def __init__(self,**kwargs):
        super(HelpDialog,self).__init__(**kwargs)
        self.rst = '''
Welcome
----------------------------

**How to use this application?**

Swipe left or right to view weather forecast. Search for new places, tap on them to view forecast for that region.
Use Navigation bar to change theme or to change areas.
Play Game or use calendar and navigate using gestures. Change theme. This application will remember all your choices like your theme and last search.

Features
---------------------------
**Gesture Recognition**

Draw these Symbols/characters. 

- 'S' move to Settings area.
- 'C' move to Calendar area.
- 'W' move to Weather area.
- 'P' move to game area.
- '|' draw a line from top to bottom to refresh the application and get updated forecast.

**MordenMenu**

Give a long press on the screen to open up a wheel shaped menu with multiple options and navigate where ever you want.
You can also change the Theme of the application using this Menubar. 

Click on center of the menu to go back.

**Navigation Bar**

Use Navigation bar to change theme or to navigate to different areas.

**Calendar**

Calendar which consists year from 0000 to 9999 and simple to use UI.

**Game**

There is a small Ping Pong game just for fun.


Developer
-----------------------

Kuldeep Singh, LNMIIT Jaipur, India
        
        '''

class StatusBar(BoxLayout):
    
    def connect(self):
        self.parent.ids.status_label.text = "updating..."
        threading.Thread(target=self.fourth_thread).start()
    
    def fourth_thread(self):
        
        config = MainApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        global getname
        if temp_type == "metric":
            self.temp_str = "C"
            print "C"
        elif temp_type == "imperial":
            self.temp_str = "F"
            print "F"
        try:
            url = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q={}&mode=json&units={}'.format(getname,temp_type)).read()
            result = json.loads(url)
            print "starting"
            self.out_file = open("weather.json","w")
            json.dump(result,self.out_file, indent=4)
            self.out_file.close()
            self.parent.ids.current.ids.location.text = str(result['city']['name'] +'('+ result['city']['country']+')')
            
            self.parent.ids.current.ids.conditions.text = str(result['list'][0]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions1.text = str(result['list'][1]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions2.text = str(result['list'][2]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions3.text = str(result['list'][3]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions4.text = str(result['list'][4]['weather'][0]['description'])
            
            
            self.parent.ids.current.ids.temp_min.text = str(result['list'][0]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.current.ids.temp_max.text = str(result['list'][0]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min1.text = str(result['list'][1]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max1.text = str(result['list'][1]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min2.text = str(result['list'][2]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max2.text = str(result['list'][2]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min3.text = str(result['list'][3]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max3.text = str(result['list'][3]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min4.text = str(result['list'][4]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max4.text = str(result['list'][4]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.current.ids.temperature.text = str(result['list'][0]['temp']['eve']) +' '+ self.temp_str
            
            self.parent.ids.current.ids.conditions_image = "http://openweathermap.org/img/w/{}.png".format(result['list'][0]['weather'][0]['icon'])
            self.parent.ids.wholeweek.ids.conditions_image1 = "http://openweathermap.org/img/w/{}.png".format(result['list'][1]['weather'][0]['icon'])
            self.parent.ids.wholeweek.ids.conditions_image2 = "http://openweathermap.org/img/w/{}.png".format(result['list'][2]['weather'][0]['icon'])
            self.parent.ids.wholeweek.ids.conditions_image3 = "http://openweathermap.org/img/w/{}.png".format(result['list'][3]['weather'][0]['icon'])
            self.parent.ids.wholeweek.ids.conditions_image4 = "http://openweathermap.org/img/w/{}.png".format(result['list'][4]['weather'][0]['icon'])
            
            print "made it"
            try:
                self.out_file = open("global_name.json","w")
                self.city_name = self.parent.ids.current.ids.location.text
                json.dump(self.city_name,self.out_file, indent=4)
                self.out_file.close()
            except:
                print "failed to load file"
            self.parent.ids.status_label.text = "updated"
        except:
            traceback.print_exc()
            
            self.in_file = open("weather.json","r")
            result = json.load(self.in_file)
            
            self.parent.ids.current.ids.location.text = str(result['city']['name'] +'('+ result['city']['country']+')')
            self.parent.ids.current.ids.conditions.text = str(result['list'][0]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions1.text = str(result['list'][1]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions2.text = str(result['list'][2]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions3.text = str(result['list'][3]['weather'][0]['description'])
            self.parent.ids.wholeweek.ids.conditions4.text = str(result['list'][4]['weather'][0]['description'])
            
            
            self.parent.ids.current.ids.temp_min.text = 'Low: '+str(result['list'][0]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.current.ids.temp_max.text = 'High: ' + str(result['list'][0]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min1.text ='Low: '+ str(result['list'][1]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max1.text = 'High: ' +str(result['list'][1]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min2.text = 'Low: '+str(result['list'][2]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max2.text = 'High: ' +str(result['list'][2]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min3.text = 'Low: '+str(result['list'][3]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max3.text = 'High: ' +str(result['list'][3]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.wholeweek.ids.temp_min4.text ='Low: '+ str(result['list'][4]['temp']['min'])+' '+ self.temp_str
            self.parent.ids.wholeweek.ids.temp_max4.text = 'High: ' +str(result['list'][4]['temp']['max'])+' '+ self.temp_str
            
            self.parent.ids.current.ids.temperature.text = str(result['list'][0]['temp']['eve']) +' '+ self.temp_str
            
            self.parent.ids.current.ids.conditions_image = "./icons/wc0.png"
            self.parent.ids.wholeweek.ids.conditions_image1 = "./icons/wc1.png"
            self.parent.ids.wholeweek.ids.conditions_image2 = "./icons/wc2.png"
            self.parent.ids.wholeweek.ids.conditions_image3 = "./icons/wc3.png"
            self.parent.ids.wholeweek.ids.conditions_image4 = "./icons/wc4.png"
            
            self.in_file.close()
            self.parent.ids.status_label.text = "update failed"
    
    def show_help(self, *args):
        threading.Thread(target=self.sixth_thread).start()
        
    def sixth_thread(self):
        self.helpdialog = HelpDialog()
        self.helpdialog.open()

class Locations(BoxLayout):
    search_input = ObjectProperty()
    search_results = ObjectProperty()
    locationtext = ObjectProperty()
    
    class LocationButton(ListItemButton):
        location = ListProperty()
        
    def update(self,*args):
        threading.Thread(target=self.fifth_thread(args[0][0],args[0][1])).start()
    
    def fifth_thread(self,*args):
        config = MainApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        self.place = '{},{}'.format(args[0],args[1])
        global getname
        getname = self.place
        #print self.place
        if temp_type == "metric":
            self.temp_str = "C"
            
        elif temp_type == "imperial":
            self.temp_str = "F"
            
        try:
            url = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q={}&mode=json&units={}'.format(self.place,temp_type)).read()
            result = json.loads(url) 
            
            print "starting"

            self.parent.parent.load_next()
            self.parent.parent.parent.parent.parent.ids.current.ids.location.text = str(result['city']['name'] +'('+ result['city']['country']+')')
            
            self.parent.parent.parent.parent.parent.ids.current.ids.conditions.text = str(result['list'][0]['weather'][0]['description'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions1.text = str(result['list'][1]['weather'][0]['description'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions2.text = str(result['list'][2]['weather'][0]['description'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions3.text = str(result['list'][3]['weather'][0]['description'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions4.text = str(result['list'][4]['weather'][0]['description'])
            
            self.parent.parent.parent.parent.parent.ids.current.ids.temp_min.text = str(result['list'][0]['temp']['min'])+' '+ self.temp_str
            self.parent.parent.parent.parent.parent.ids.current.ids.temp_max.text = str(result['list'][0]['temp']['max'])+' '+ self.temp_str
            
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_min1.text = str(result['list'][1]['temp']['min'])+' '+ self.temp_str
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_max1.text = str(result['list'][1]['temp']['max'])+' '+ self.temp_str
            
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_min2.text = str(result['list'][2]['temp']['min'])+' '+ self.temp_str
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_max2.text = str(result['list'][2]['temp']['max'])+' '+ self.temp_str
            
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_min3.text = str(result['list'][3]['temp']['min'])+' '+ self.temp_str
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_max3.text = str(result['list'][3]['temp']['max'])+' '+ self.temp_str
            
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_min4.text = str(result['list'][4]['temp']['min'])+' '+ self.temp_str
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.temp_max4.text = str(result['list'][4]['temp']['max'])+' '+ self.temp_str
            
            self.parent.parent.parent.parent.parent.ids.current.ids.temperature.text = str(result['list'][0]['temp']['eve']) +' '+ self.temp_str
            
            
            self.parent.parent.parent.parent.parent.ids.current.ids.conditions_image = "http://openweathermap.org/img/w/{}.png".format(result['list'][0]['weather'][0]['icon'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions_image1 = "http://openweathermap.org/img/w/{}.png".format(result['list'][1]['weather'][0]['icon'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions_image2 = "http://openweathermap.org/img/w/{}.png".format(result['list'][2]['weather'][0]['icon'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions_image3 = "http://openweathermap.org/img/w/{}.png".format(result['list'][3]['weather'][0]['icon'])
            self.parent.parent.parent.parent.parent.ids.wholeweek.ids.conditions_image4 = "http://openweathermap.org/img/w/{}.png".format(result['list'][4]['weather'][0]['icon'])
            
            self.out_file = open("weather.json","w")
            json.dump(result,self.out_file, indent=4)
            self.out_file.close()
            print "made it"
            self.parent.parent.parent.parent.parent.ids.status_label.text = "updated"
        except:
            traceback.print_exc()
            self.parent.parent.parent.parent.parent.ids.status_label.text = "update failed"
            
    def search_location(self):
        search_template = "http://api.openweathermap.org/data/2.5/find?q={}&type=like"
        search_url =  search_template.format(self.search_input.text)
        print self.search_input.text
        #@param URL, method(request, response) to be called upon response
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, response):
        try:
            response = json.loads(response.decode()) if not isinstance(response, dict) else response
        #Fix_Ends
        #print response
            if response != {u'message': u'', u'cod': u'404'}:
                if response != {u'count': 0, u'message': u'like', u'list': [], u'cod': u'200'}:
                    
                    #change cities from list of string to list of tuples for easier processing while retriving data specific to the location
                    cities = [(d['name'], d['sys']['country']) for d in response['list']]
                    self.search_results.item_strings = cities
                
                    #the container involved is ObservableList so clear it
                    #self.search_results.adapter.data.clear()
                    #clear() on list is not available in python 2 so use
                    del self.search_results.adapter.data[:]
                    #donot delete list like this data = [] as it would assign normal list instead of ObservableList
                    #extend with new data
                    self.search_results.adapter.data.extend(cities)
                    #ListAdapter should update display when it sees data change but it ain't doing it, so force the update 
                    self.search_results._trigger_reset_populate()
                else:
                    self.search_input.text = "No results found"
            else:
                self.search_input.text = "No results found"
        except:
            self.search_input.text = "Didn't receive any response"
            self.parent.parent.parent.parent.parent.ids.status_label.text = "update failed"
            
        
    def args_converter(self,index, data_item):
    #index -> index of the item in list
    #data_item -> value
        city, country = data_item
        print city,country
        self.locationtext = "{}({})".format(city,country)
    #return value should be a dictionary of properties with their value
    #in this case the property location is set to the tuple
    #however since location is defined as ListProperty the tuple will be automatically converted into List
        return {'location': (city, country)}

class Current(BoxLayout):
    location = StringProperty()
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    conditions_image = ObjectProperty()
    temp_str = StringProperty()
    
    two = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(Current,self).__init__(**kwargs)
        threading.Thread(target=self.second_thread).start()
        try:
            self.in_file = open("weather.json","r")
            result = json.load(self.in_file)
            
            self.conditions = result['list'][0]['weather'][0]['description']
            
            self.temp_min = result['list'][0]['temp']['min']
            
            self.temp_max = result['list'][0]['temp']['max']
            
            self.temp = result['list'][0]['temp']['eve']
            
            self.conditions_image = "./icons/wc0.png"
            
            self.location = result['city']['name'] +'('+ result['city']['country']+')'
            
            self.in_file.close()
        except:
            traceback.print_exc()
            
    def second_thread(self):
        config = MainApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        if temp_type == "metric":
            self.temp_str = "C"
            print "C"
        elif temp_type == "imperial":
            self.temp_str = "F"
            print "F"
        try:
            global getname
            print getname
            print "____get_namne_here"
            url = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q={}&mode=json&units={}'.format(getname,temp_type)).read()
            result = json.loads(url) 
            self.location = result['city']['name'] +'('+ result['city']['country']+')'
            self.conditions = result['list'][0]['weather'][0]['description']
            self.conditions_image = "http://openweathermap.org/img/w/{}.png".format(result['list'][0]['weather'][0]['icon'])
            
            response0 = requests.get(self.conditions_image)
            if response0.status_code == 200:
                f = open("./icons/wc0.png", 'wb')
                f.write(response0.content)
                print "saving image 0"
                f.close()
            
            self.temp_min = result['list'][0]['temp']['min']
            self.temp_max = result['list'][0]['temp']['max']
            self.temp = result['list'][0]['temp']['eve']
            self.parent.parent.parent.parent.parent.ids.status_label.text = "updated"
        except:
            traceback.print_exc()
            print "fails"
            self.parent.parent.parent.parent.parent.ids.status_label.text = "update failed"
            

class WholeWeek(BoxLayout):
    location = StringProperty()
    conditions = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()
    conditions_image = ObjectProperty()
    temp_str = StringProperty()
    whole = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Monday','Tuesday','Wednesday','Thursday']
    now = datetime.datetime.now()
    today = whole.index(now.strftime("%A"))

    day1 = StringProperty(whole[today+1])
    day2 = StringProperty(whole[today+2])
    day3 = StringProperty(whole[today+3])
    day4 = StringProperty(whole[today+4])
    
    conditions1 = StringProperty()
    temp_min1 = NumericProperty()
    temp_max1 = NumericProperty()
    conditions_image1 = StringProperty()
    
    
    conditions2 = StringProperty()
    temp_min2 = NumericProperty()
    temp_max2 = NumericProperty()
    conditions_image2 = StringProperty()
    
    conditions3 = StringProperty()
    temp_min3 = NumericProperty()
    temp_max3 = NumericProperty()
    conditions_image3 = StringProperty()
    
    conditions4 = StringProperty()
    temp_min4 = NumericProperty()
    temp_max4 = NumericProperty()
    conditions_image4 = StringProperty()
    
    def __init__(self,**kwargs):
        super(WholeWeek,self).__init__(**kwargs)
        threading.Thread(target=self.third_thread).start()
        try:
            self.in_file = open("weather.json","r")
            result = json.load(self.in_file)
            
            self.conditions1 = result['list'][1]['weather'][0]['description']
            self.conditions2 = result['list'][2]['weather'][0]['description']
            self.conditions3 = result['list'][3]['weather'][0]['description']
            self.conditions4 = result['list'][4]['weather'][0]['description']
            
            self.temp_min1 = result['list'][1]['temp']['min']
            self.temp_max1 = result['list'][1]['temp']['max']
            
            self.temp_min2 = result['list'][2]['temp']['min']
            self.temp_max2 = result['list'][2]['temp']['max']
            
            self.temp_min3 = result['list'][3]['temp']['min']
            self.temp_max3 = result['list'][3]['temp']['max']
            
            self.temp_min4 = result['list'][4]['temp']['min']
            self.temp_max4 = result['list'][4]['temp']['max']
            
            self.conditions_image  = "./icons/wc0.png"
            self.conditions_image1 = "./icons/wc1.png"
            self.conditions_image2 = "./icons/wc2.png"
            self.conditions_image3 = "./icons/wc3.png"
            self.conditions_image4 = "./icons/wc4.png"
            self.in_file.close()
        except:
            traceback.print_exc()
            
    def third_thread(self):
        config = MainApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        if temp_type == "metric":
            self.temp_str = "C"
            print "C"
        elif temp_type == "imperial":
            self.temp_str = "F"
            print "F"
            
        try:
            global getname
            url = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?q={}&mode=json&units={}'.format(getname,temp_type)).read()
            result = json.loads(url) 
            self.out_file = open("weather.json","w")
            json.dump(result,self.out_file, indent=4)
            self.out_file.close()
            print "came here"
            #self.location = result['city']['name'] +'('+ result['city']['country']+')'
            #self.parent.ids.current.ids.conditions = result['list'][0]['weather'][0]['description']
            
            #self.parent.ids.current.ids.conditions_image = "http://openweathermap.org/img/w/{}.png".format(result['list'][0]['weather'][0]['icon'])
            self.conditions_image1 = "http://openweathermap.org/img/w/{}.png".format(result['list'][1]['weather'][0]['icon'])
            self.conditions_image2 = "http://openweathermap.org/img/w/{}.png".format(result['list'][2]['weather'][0]['icon'])
            self.conditions_image3 = "http://openweathermap.org/img/w/{}.png".format(result['list'][3]['weather'][0]['icon'])
            self.conditions_image4 = "http://openweathermap.org/img/w/{}.png".format(result['list'][4]['weather'][0]['icon'])
            
            response1 = requests.get(self.conditions_image1)
            response2 = requests.get(self.conditions_image2)
            response3 = requests.get(self.conditions_image3)
            response4 = requests.get(self.conditions_image4)
            if response1.status_code == 200:
                f = open("./icons/wc1.png", 'wb')
                f.write(response1.content)
                print "saving image 1"
                f.close()
            if response2.status_code == 200:
                f = open("./icons/wc2.png", 'wb')
                f.write(response2.content)
                print "saving image 2"
                f.close()
            if response3.status_code == 200:
                f = open("./icons/wc3.png", 'wb')
                f.write(response3.content)
                print "saving image 3"
                f.close()
            if response4.status_code == 200:
                f = open("./icons/wc4.png", 'wb')
                f.write(response4.content)
                print "saving image 4"
                f.close()
            #self.parent.ids.current.ids.temp_min = result['list'][0]['temp']['min']
            #self.parent.ids.current.ids.temp_max = result['list'][0]['temp']['max']
            
            self.conditions1 = result['list'][1]['weather'][0]['description']
            self.conditions2 = result['list'][2]['weather'][0]['description']
            self.conditions3 = result['list'][3]['weather'][0]['description']
            self.conditions4 = result['list'][4]['weather'][0]['description']
            
            self.temp_min1 = result['list'][1]['temp']['min']
            self.temp_max1 = result['list'][1]['temp']['max']
            
            self.temp_min2 = result['list'][2]['temp']['min']
            self.temp_max2 = result['list'][2]['temp']['max']
            
            self.temp_min3 = result['list'][3]['temp']['min']
            self.temp_max3 = result['list'][3]['temp']['max']
            
            self.temp_min4 = result['list'][4]['temp']['min']
            self.temp_max4 = result['list'][4]['temp']['max']
            
            #self.parent.ids.current.ids.temp = result['list'][0]['temp']['eve']
            print "made it"
            print self.parent.parent.parent.parent.parent.ids
            self.parent.parent.parent.parent.parent.ids.status_label.text = "updated"
        except:
            traceback.print_exc()
            print self.parent.parent
            self.parent.parent.parent.parent.parent.ids.status_label.text = "update failed"
            
    
    
class History(BoxLayout):
    pass


class Together(gesture.GestureBox):
    theme = StringProperty('')
    theme = StringProperty('')
    theme0 = NumericProperty()
    theme1 = NumericProperty()
    theme2 = NumericProperty('')
    theme3 = NumericProperty('')
    def __init__(self,**kwargs):
        super(Together,self).__init__(**kwargs)
        in_file = open("theme.json","r")
        self.theme =json.load(in_file)['theme']
        self.theme0 = float(self.theme.split(',')[0])
        self.theme1 = float(self.theme.split(',')[1])
        self.theme2 = float(self.theme.split(',')[2])
        self.theme3 = float(self.theme.split(',')[3])
        
        in_file.close()

    def on_touch_down(self, touch):
        try:
            gesture.GestureBox.on_touch_down(self, touch)
            color = (random(), 1, 1)
            with self.canvas:
                Color(*color, mode='hsv')
                touch.ud['line'] = Line(points=(touch.x, touch.y),width = 5)
        except:
            pass
            
    def on_touch_move(self, touch):
        try:
            gesture.GestureBox.on_touch_move(self, touch)
            if self.ids.manager.current == "game":
                touch.ud['line'].points = []
            else:
                touch.ud['line'].points += [touch.x, touch.y]
        except:
            pass
    
class User(BoxLayout):

    def callback1(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.266,.423,.701,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.266,.423,.701,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback2(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.839,.270,.254,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.839,.270,.254,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback3(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.749,.333,.925,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.749,.333,.925,1)),  
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback4(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.2,.431,.482,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.2,.431,.482,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback5(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.149,.560,.356,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.149,.560,.356,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback6(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.949,.470,.294,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.949,.470,.294,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback7(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.423,.478,.537,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.423,.478,.537,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback8(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.323,.7,.2,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.323,.7,.2,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    def callback9(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.323,.1,.32,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.canvas.before:
            Color(rgba = (.323,.1,.32,1)),
            Rectangle(pos=(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[0]-200,args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.pos[1]-200),
                      size=(max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500,max(args[0].parent.parent.parent.parent.parent.parent.parent.parent.parent.ids.together.size)+500))
    
    
from kivy.clock import Clock
from kivy.properties import BooleanProperty

if platform == "android":
    import android
    from jnius import autoclass, cast
    from android.runnable import run_on_ui_thread
    Toast = autoclass("android.widget.Toast")
    
    from jnius import autoclass
    # Context is a normal java class in the Android API
    Context = autoclass('android.content.Context')
    # PythonActivity is provided by the Kivy bootstrap app in python-for-android
    PythonActivity = autoclass('org.renpy.android.PythonActivity')
    # The PythonActivity stores a reference to the currently running activity
    # We need this to access the vibrator service
    #activity = PythonActivity.mActivity

class MainApp(App):
    exitnext = BooleanProperty(False)
    use_kivy_settings = False

    def __init__(self, *args, **kwargs):
        super(MainApp, self).__init__(*args, **kwargs)

    def build(self):
        if platform == "android":
            self.bind(on_start=self.post_build_init)
        return User()
    
    if platform == "android":
        @run_on_ui_thread
        def toast(self, text, duration):
            # Duration is either 0 = short = 2 sec, or 1 = long = 3.5 sec
            String = autoclass('java.lang.String')
            c = cast('java.lang.CharSequence', String(text))
            context = PythonActivity.mActivity.getApplicationContext()
            t = Toast.makeText(context, c, duration)
            t.show()
            return t
    else:
        pass
    
    
    def post_build_init(self, *args):
        # Map Android keys
        if platform == 'android':
            android.map_key(android.KEYCODE_BACK, 1000)
            android.map_key(android.KEYCODE_MENU, 1001)
        win = self._app_window
        win.bind(on_keyboard=self._key_handler)
 
    def _key_handler(self, *args):
        key = args[1]
        # Escape or Android's back key
        if key in (1000, 27):
            self.hide_kbd_or_exit()
            return True
 
    def hide_kbd_or_exit(self, *args):
        if platform == "android" and not self.exitnext:
            android.hide_keyboard()
            self.exitnext = True
            Clock.schedule_once(lambda *args: setattr(self, "exitnext", False), 2)
            self.toast(("Press Back again to exit"), 0)
        else:
            self.stop()
            
            
    def build_config(self, config):
        config.setdefaults('General', {'temp_type': "Metric"})
        
        
    def build_settings(self, settings):
        #param --> title, always self.config, filename or JSON data
        settings.add_json_panel("Weather Settings", self.config, data="""
            [
                {"type": "options",
                    "title": "Temperature System",
                    "section": "General",
                    "key": "temp_type",
                    "options": ["Metric", "Imperial"]
                }
            ]""")
        
    def on_config_change(self, config, section, key, value):
        if config is self.config and key == "temp_type":
            try:
                self.root.children[0].update_weather()
            #current root window has no update_weather method
            except AttributeError:
                pass

    def on_pause(self):
        return True

    def on_resume(self):
        pass
    
    def on_touch_down(self,touch):
        pass

    def callback1(self, *args):
        args[0].parent.open_submenu(
            choices=[
                dict(text='Theme 1', index=1, callback=self.callback2),
                dict(text='Theme 2', index=2, callback=self.callback3),
                dict(text='Theme 3', index=3, callback=self.callback7),
                dict(text='Theme 4', index=4, callback=self.callback8),
                dict(text='Theme 5', index=5, callback=self.callback9),
            ])
        
    def callback4(self,*args):
        args[0].parent.open_submenu(
            choices=[
                dict(text='Theme 6', index=1, callback=self.callback10),
                dict(text='Theme 7', index=2, callback=self.callback11),
                dict(text='Theme 8', index=3, callback=self.callback12),
                dict(text='Theme 9', index=4, callback=self.callback13),
            ])
    
    def callback2(self, *args):
        print args[0]
        out_file = open("theme.json","w")
        theme = {'theme': '.266,.423,.701,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.266,.423,.701,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callbackabout(self, *args):
        args[0].parent.parent.parent.ids.manager.current = 'about'
        args[0].parent.dismiss()
        
    def callback3(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.839,.270,.254,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.839,.270,.254,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback7(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.749,.333,.925,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.749,.333,.925,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback8(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.2,.431,.482,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.2,.431,.482,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback9(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.149,.560,.356,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.149,.560,.356,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback10(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.949,.470,.294,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.949,.470,.294,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback11(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.423,.478,.537,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.423,.478,.537,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))

    def callback12(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.323,.7,.2,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.323,.7,.2,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+500,max(args[0].parent.parent.parent.size)+500))

    def callback13(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.323,.1,.32,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.323,.1,.32,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+500,max(args[0].parent.parent.parent.size)+500))


    def callback5(self, *args):
        self.open_settings()
        args[0].parent.dismiss()
        
    def callback6(self, *args):
        out_file = open("theme.json","w")
        theme = {'theme': '.323,.2,.7,1'}
        json.dump(theme,out_file, indent=4) 
        out_file.close()
        with args[0].parent.parent.parent.canvas.before:
            Color(rgba = (.323,.7,.7,1)),
            Rectangle(pos=args[0].parent.parent.parent.pos, size=(max(args[0].parent.parent.parent.size)+200,max(args[0].parent.parent.parent.size)+200))
        args[0].parent.dismiss()


if __name__ == '__main__':
    MainApp().run()
