from manim import *

class MainScene(Scene):
    def construct(self):
        total_time = 0
        time_to_move = 1
        direction = 1 
        is_moving = True
        
        line1 = Line(LEFT, RIGHT).shift(UP)
        line2 = Line(LEFT, RIGHT).shift(DOWN)
        
        # Create a glowing dot
        dot = Dot(radius=0.2, color=YELLOW).move_to(line1.get_center())
        glow = Dot(radius=0.3, color=YELLOW).set_opacity(0.5)
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
        
        self.wait(1)
        photon_clock_brace = Brace(photon_clock, RIGHT)
        photon_clock_brace_label = MathTex("1s").next_to(photon_clock_brace, RIGHT, buff=0.1)
        self.play(GrowFromCenter(photon_clock_brace), Write(photon_clock_brace_label))
        self.wait(2)
        is_moving = False
        self.play(FadeOut(photon_clock_brace, photon_clock_brace_label), ScaleInPlace(photon_clock, 0.7))
        self.play(photon_clock.animate.shift(DOWN*3))
        
        
        # create a new photon clock
        line3 = Line(LEFT, RIGHT).shift(UP)
        line4 = Line(LEFT, RIGHT).shift(DOWN)
        
        dot_2 = Dot(radius=0.2, color=YELLOW).move_to(line1.get_center())
        glow_2 = Dot(radius=0.3, color=YELLOW).set_opacity(0.5)
        glow_2.add_updater(lambda m: m.move_to(dot_2.get_center()))
        dot_2.add_updater(lambda m, dt: update_dot(m, dt, line3, line4))
        
        dot_2.move_to(line3.get_center())
        photon_clock_2 = VGroup(line3, line4, dot_2, glow_2)
        
        photon_clock_2.scale(0.7)
        photon_clock_2.move_to(photon_clock.get_center())
        self.add(photon_clock_2) 
        
        self.play(photon_clock_2.animate.shift(UP*5+LEFT))
        
        
        bottom_path = TracedPath(dot.get_center, 
                              stroke_color=GREEN, 
                              stroke_width=3)
        top_path = TracedPath(dot_2.get_center, 
                              stroke_color=ORANGE,
                              stroke_width=3)
        
        # add paths
        self.add(bottom_path, top_path)
        
        is_moving = True
        
        self.play(photon_clock_2.animate.shift(RIGHT * 2), animation_func=linear, run_time=3)

        self.wait(5)
        
        ''' 
        for _ in range(5):  
            self.play(dot.animate.move_to(line1.get_center()), rate_func=linear)
            self.play(dot.animate.move_to(line2.get_center()), rate_func=linear) 
        '''