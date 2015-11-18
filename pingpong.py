from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
import random
from kivy.uix.popup import Popup
from kivy.uix.button import Button

class PongPaddle(Widget):
    score = NumericProperty(0)
    
    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx,vy = ball.velocity
            offset = (ball.center_y - self.center_y)/(self.height/2)+.1
            bounced = Vector(-1*vx,vy)
            a = bounced
            if a[0] >= 43 or a[0] <= -43:
                vel = bounced*1
            else:
                vel = bounced*1.1
                
            ball.velocity = vel.x,vel.y + offset
        
class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)
    
    def move(self):
        self.pos = Vector(*self.velocity)+ self.pos

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    check = 0
    opponent = 0
    
    def serve_ball(self,vel = (4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel
    
    def on_pause(self):
        Clock.unschedule(self.update)
        self.check = 1
    
    def on_resume(self):
        if self.check == 1:
            Clock.schedule_interval(self.update, 1.0 / 60.0)
            self.check = 0
        else: pass
    
    def on_fast(self):
        self.ball.velocity_y += 1
        if self.ball.velocity_x < 0:
            self.ball.velocity_x += -5
        elif self.ball.velocity_x > 0:
            self.ball.velocity_x += 5
        else:
            pass
        
    
    def on_restart(self):
        Clock.unschedule(self.update)
        self.opponent = 0
        self.gravity = 0
        self.player1.score = 0
        self.player2.score = 0
        if random.randint(0,1)%2 == 0:
            self.serve_ball(vel=(4,0))
        else:
            self.serve_ball(vel=(-4,0))
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
    def on_opponent(self):
        self.opponent = 1
        self.player1.center_y = self.ball.center_y
    
    def update(self,dt):
        self.ball.move()
        
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        
        if self.opponent == 1:
            self.player1.center_y = self.ball.center_y
            
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        if self.ball.x < self.x-10:
            self.player2.score +=1
            if self.player2.score == 10:
                Clock.unschedule(self.update)
                self._popup = Popup(title='About', content=Won1(),size_hint=(.4,.5),auto_dismiss=False)
                self._popup.open()
            self.serve_ball(vel=(4,0))
        
        if self.ball.x > self.width:
            self.player1.score += 1
            if self.player1.score == 10:
                Clock.unschedule(self.update)
                self._popup = Popup(title='About', content=Won2(),size_hint=(.4, .5),auto_dismiss=False)
                self._popup.open()
            self.serve_ball(vel=(-4,0))
        
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.ball.velocity_y > 0 :
                self.ball.velocity_y += 5
            if self.ball.velocity_y < 0:
                self.ball.velocity_y -=5
    
    def on_touch_move(self,touch):
        if self.opponent == 0:
            if touch.x < self.width/3:
                self.player1.center_y = touch.y
        else:
            pass
        if touch.x > self.width - self.width/3:
            self.player2.center_y = touch.y
        
            
class Won1(BoxLayout):
    pass

    
class Won2(BoxLayout):
    pass

class Game(BoxLayout):
    pass
