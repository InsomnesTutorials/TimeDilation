from manim import *
import math
from datetime import datetime

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 9
config.frame_height = 16

# used to flatten a traced path
class FlatenWrapper():
    def __init__(self):
        self.total_length = 0.0
        self.last_point = None
    
    def flatten_line(self, point, x, start_y):
        if self.last_point is None:
            self.last_point = point
        else:
            dist = math.pow((self.last_point[0] - point[0]),2) + math.pow((self.last_point[1]-point[1]), 2)
            dist = math.sqrt(dist)
            self.total_length += dist
            self.last_point = point
                
        return np.array([x, start_y + self.total_length, 0])

class MainScene2(Scene):
    def wait_for_keypress(self, message="Press Enter to continue..."):
        a = datetime.now()
        input(message)
        b = datetime.now()
        
        self.wait((b-a).total_seconds())
        
    def construct(self):
        total_time = 0
        time_to_move = 1
        direction = 1 
        is_moving = True
        
        line1 = Line(LEFT*1.5, RIGHT*1.5).shift(UP*1.5)
        line2 = Line(LEFT*1.5, RIGHT*1.5).shift(DOWN*1.5)
        
        # Create a glowing dot
        dot = Dot(radius=0.3, color=YELLOW).move_to(line1.get_center())
        glow = Dot(radius=0.4, color=YELLOW).set_opacity(0.5)
        glow.move_to(dot.get_center())
        glow.add_updater(lambda m: m.move_to(dot.get_center()))
        
        photon_clock = VGroup(line1, line2, dot, glow) 
        
        def update_dot(dot: Mobject, dt, line1, line2):
            nonlocal total_time, direction, is_moving
            if not is_moving:
                return
            if direction == 1 and total_time >= time_to_move:
                direction = -1
            elif direction == -1 and total_time <= 0:
                direction = 1
            
            total_time += dt * direction   
            dt = total_time / time_to_move
            
            dot.move_to((dt)*line1.get_center() + (1-dt)*line2.get_center()) 
        
        
        self.add(line1, line2)
        self.add(dot, glow)
        dot.add_updater(lambda m, dt: update_dot(m, dt, line1, line2))
        
        self.wait(4)
        photon_clock_brace = Brace(photon_clock, RIGHT)
        photon_clock_brace_label = MathTex("1s").next_to(photon_clock_brace, RIGHT, buff=0.1)
        self.play(GrowFromCenter(photon_clock_brace), Write(photon_clock_brace_label))
        self.wait(2)
        is_moving = False
        self.play(FadeOut(photon_clock_brace, photon_clock_brace_label), ScaleInPlace(photon_clock, 0.7))
        self.play(photon_clock.animate.shift(DOWN*5))
        
        
        # create a new photon clock
        line3 = Line(LEFT*1.5, RIGHT*1.5).shift(UP*1.5)
        line4 = Line(LEFT*1.5, RIGHT*1.5).shift(DOWN*1.5)
        
        dot_2 = Dot(radius=0.3, color=YELLOW).move_to(line4.get_center())
        glow_2 = Dot(radius=0.4, color=YELLOW).set_opacity(0.5)
        glow_2.add_updater(lambda m: m.move_to(dot_2.get_center()))
        dot_2.add_updater(lambda m, dt: update_dot(m, dt, line3, line4))
        
        photon_clock_2 = VGroup(line3, line4, dot_2, glow_2)
        
        photon_clock_2.scale(0.7)
        photon_clock_2.move_to(photon_clock.get_center())
        self.add(photon_clock_2) 
        
        self.play(photon_clock_2.animate.shift(UP*10+LEFT*3), dot.animate.move_to(line2.get_center()), run_time=2)
        
        
        bottom_path = TracedPath(dot.get_center, 
                              stroke_color=GREEN, 
                              stroke_width=4)
        top_path = TracedPath(dot_2.get_center, 
                              stroke_color=ORANGE,
                              stroke_width=4)
        
        # add paths
        self.add(bottom_path, top_path)
        
        total_time = 0
        time_to_move = 3
        is_moving = True
        
        self.play(photon_clock_2.animate.shift(RIGHT * 5), rate_func=linear, run_time=4)
        
        is_moving = False
        self.wait(1)
        
        self.play(FadeOut(line1, line2, line3, line4, dot, dot_2, glow, glow_2), run_time=2)
        
        path1_static = VMobject().set_points(top_path.get_points()).set_stroke(width=3, color=ORANGE)
        path2_static = VMobject().set_points(bottom_path.get_points()).set_stroke(width=3, color=GREEN) 
        
        self.remove(top_path, bottom_path)
        self.add(path1_static, path2_static)
        
        flattener_1 = FlatenWrapper() 
        flattener_2 = FlatenWrapper()
        
        self.play(
            path1_static.animate.apply_function(lambda p : flattener_1.flatten_line(p, -2, -6)),
            path2_static.animate.apply_function(lambda p : flattener_2.flatten_line(p, 2, -6)),
            run_time=2,
            rate_func=smooth,
        ) 
        
        self.wait(2)
        self.play(Indicate(path1_static))
        self.wait(2)
        self.play(Indicate(path2_static))
        
        self.wait(1)
        speeed_of_light = MathTex("c=2.9*10^8 m/s", font_size=60)
        self.play(Transform(VGroup(path1_static, path2_static), speeed_of_light), run_time=2)
        self.wait(1)
        self.play(FadeOut(speeed_of_light))
        self.wait(1)
        