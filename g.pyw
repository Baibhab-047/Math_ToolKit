import sympy
import pygame as pg
import sys
import numpy as np
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

pg.init()
pg.font.init()
real_height = 800
Width = 700
Height = 700
scale = 40 
v_line_width = 1
v_line_height = 700
h_line_width = 700
h_line_height = 1


x_axis = pg.rect.Rect(0, 349, h_line_width, h_line_height)
y_axis = pg.rect.Rect(349, 0, v_line_width, v_line_height)
FONT = pg.font.SysFont('Bahnschrift', 20)
Input_Type = False
Eq_Text = ''
Input_Rect = pg.rect.Rect(350, 705, 300, 35)


Graph_need = True
points = []

screen = pg.display.set_mode((Width, real_height))
pg.display.set_caption('Ultra-Fast Graphical Representation')
Clock = pg.time.Clock()

def draw_h_lines():
    no_of_lines_possible_u = x_axis.y // scale
    no_of_lines_possible_d = (700 - x_axis.y) // scale 
    for i in range(no_of_lines_possible_d + 1):
        pg.draw.rect(screen, 'lightgrey', (0, x_axis.y + i*scale, h_line_width, h_line_height))
    for i in range(no_of_lines_possible_u + 1):
        pg.draw.rect(screen, 'lightgrey', (0, x_axis.y - i*scale, h_line_width, h_line_height))

def draw_v_lines():
    no_of_lines_possible_r = (700 - y_axis.x) // scale
    no_of_lines_possible_l = (y_axis.x) // scale 
    for i in range(no_of_lines_possible_r + 1):
        pg.draw.rect(screen, 'lightgrey', (y_axis.x + i*scale, 0, v_line_width, v_line_height))
    for i in range(no_of_lines_possible_l + 1):
        pg.draw.rect(screen, 'lightgrey', (y_axis.x - i*scale, 0, v_line_width, v_line_height))

def write_parts_calculate(mouse_x, mouse_y):
    real_x = round((mouse_x - y_axis.x) / scale, 3)
    real_y = round((x_axis.y - mouse_y) / scale, 3)
    quadrant = get_quadrant(real_x, real_y)
    
    x_font = FONT.render(f'X Position: {real_x:.3f}', True, 'black')
    y_font = FONT.render(f'Y Position: {real_y:.3f}', True, 'black')
    quadrant_font = FONT.render(f'Quadrant: {quadrant}', True, 'black')
    return x_font, y_font, quadrant_font

def get_quadrant(r_x, r_y):
    if r_x != 0 and r_y != 0:
        q_map = {(True, True):"I", (False, True):"II", (False, False):"III", (True, False):"IV"}
        return q_map[(r_x > 0, r_y > 0)]
    return 'On Axis'

def solve_graph():
    global points
    if not Eq_Text:
        points = []
        return

    try:
        x_sym = sympy.symbols('x')
        transformations = (standard_transformations + (implicit_multiplication_application,))
        clean_eq = Eq_Text.replace('^', '**')
        equation = parse_expr(clean_eq, transformations=transformations)

        
        fast_func = sympy.lambdify(x_sym, equation, modules=['numpy'])

        
        l_bound = (0 - y_axis.x) / scale
        r_bound = (Width - y_axis.x) / scale
        
       
        x_vals = np.linspace(l_bound, r_bound, Width)
        
        
        y_vals = fast_func(x_vals)
        
        
        if isinstance(y_vals, (int, float)):
            y_vals = np.full_like(x_vals, y_vals)

        points = []
        
        for i in range(len(x_vals)):
            
            if np.isnan(y_vals[i]) or np.isinf(y_vals[i]):
                continue
                
            screen_x = y_axis.x + (x_vals[i] * scale)
            screen_y = x_axis.y - (y_vals[i] * scale)
            
            
            if -5000 < screen_y < 5000:
                points.append((screen_x, screen_y))

    except Exception as e:
        
        points = []


running = True
while running:
    for event in pg.event.get():
        keys = pg.mouse.get_pressed()
        
        if event.type == pg.QUIT:
            running = False
            
        elif event.type == pg.MOUSEWHEEL:
            Graph_need = True
            if event.y > 0:
                scale += 5
            elif event.y < 0:
                scale -= 5
            scale = max(5, min(scale, 500))
            
        elif event.type == pg.MOUSEMOTION and keys[0]:
            
            x_axis.centery += event.rel[1]
            y_axis.centerx += event.rel[0]
            Graph_need = True 
            
        elif event.type == pg.MOUSEBUTTONDOWN:
            if Input_Rect.collidepoint(event.pos):
                Input_Type = not Input_Type
            else:
                if Input_Type:
                    Graph_need = True 
                Input_Type = False
                
        elif event.type == pg.KEYDOWN:
            if Input_Type:
                if event.key == pg.K_RETURN:
                    Input_Type = False
                    Graph_need = True 
                elif event.key == pg.K_BACKSPACE:
                    Eq_Text = Eq_Text[:-1]
                else:
                    char = event.unicode
                    if char.isalnum() or char in "+-*/^.()":
                        Eq_Text += char

    
    if not Input_Type and Graph_need:
        solve_graph()
        Graph_need = False

    
    screen.fill('white')
    
    
    draw_h_lines()
    draw_v_lines()
    pg.draw.rect(screen, 'black', x_axis)
    pg.draw.rect(screen, 'black', y_axis)
    

    if not Input_Type and len(points) > 1:   
        pg.draw.aalines(screen, 'red', False, points)

    
    m_x, m_y = pg.mouse.get_pos()
    if 0 < m_x < 700 and 0 < m_y < 700:
        write = write_parts_calculate(m_x, m_y)
    else:
        write = write_parts_calculate(y_axis.x, x_axis.y) 
    pg.draw.rect(screen, 'white', (0, 700, 700, 100))

    pg.draw.line(screen, 'black', (0, 700), (700, 700), 2)
    screen.blit(write[0], (5, 705))
    screen.blit(write[1], (5, 735))
    screen.blit(write[2], (5, 765))
    
    
    box_color = (200, 220, 255) if Input_Type else (230, 230, 230)
    pg.draw.rect(screen, box_color, Input_Rect)
    pg.draw.rect(screen, 'black', Input_Rect, 2)
    
    
    cursor = "|" if Input_Type and (pg.time.get_ticks() % 1000 < 500) else ""
    text_surf = FONT.render("Eq: " + Eq_Text + cursor, True, 'black')
    screen.blit(text_surf, (Input_Rect.x + 10, Input_Rect.y + 10))
    
    pg.display.flip()
    Clock.tick(75)

pg.quit()
sys.exit()