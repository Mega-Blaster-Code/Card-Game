import time
from os import environ


environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import sys
import get_card_info as info
import threading
import socket
import random

import server
import client

def obter_ip_local():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)
Net_S = server.Net_Server(obter_ip_local())
Net_C = client.Net_Client()

pygame.init()
WIDTH = 600
HEIGHT = 850
fWIDTH = 600
fHEIGHT = 850
screen = pygame.display.set_mode((fWIDTH, fHEIGHT), pygame.NOEVENT)
clock = pygame.time.Clock()

cache = {}

scroll = 0
scroll_target = 0
scroll_size = 50
scroll_speed = 0.25
scroll_max = 0
click = False

def render():
    pygame.display.flip()
    screen.fill((255,255,255))
    clock.tick(90)

class draw_sistem:
    def __init__(self):
        self.local_cache = {}
        self.local_cache = {}
        self.font_cache = {}

    def draw_image(self,path, pos, size):
        if pos[0] > -size[0] and pos[0] < WIDTH + size[0] and pos[1] > -size[1] and pos[1] < HEIGHT + size[1]:
            image = self.load_image(path)
            image = pygame.transform.scale(image, size)
            screen.blit(image, pos)

    def load_image(self, path):
        image = pygame.image.load(path)
        return image

    def transfome_image(self,img,size):
        image = pygame.transform.scale(img,size)
        return image
    def draw_circle(self,pos, size, color, width=0):
        pygame.draw.circle(screen, color, pos, size, width)

    def draw_rectangle(self,pos, size, color, rotation, opacity, width=0, round=0):
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        pygame.draw.rect(screen, color, rect, width, round)

    def draw_triangle(self,pos, size, color, width=0):
        points = [
            (pos[0], pos[1] - size[1] / 2),
            (pos[0] - size[0] / 2, pos[1] + size[1] / 2),
            (pos[0] + size[0] / 2, pos[1] + size[1] / 2)
        ]
        pygame.draw.polygon(screen, color, points, width)

    def draw_line(self,start_pos, end_pos, size, color, opacity, width=1):
        pygame.draw.line(screen, color, start_pos, end_pos, width)

    def get_font(self, font_name, size):
        key = (font_name, size)
        if key not in self.font_cache:
            self.font_cache[key] = pygame.font.SysFont(font_name, size)
        return self.font_cache[key]

    def draw_text(self, text, pos, size, color, rotation, opacity, font=None):
        font = self.get_font(font, size)
        text_surface = font.render(text, True, color)
        text_surface.set_alpha(opacity)
        text_surface = pygame.transform.rotate(text_surface, rotation)
        screen.blit(text_surface, pos)

    def check_click(self):
        return pygame.mouse.get_pressed(3)[0]

    def mouse_pos(self):
        return pygame.mouse.get_pos()

    def click_in_rect(self, rect):
        global click
        if click:
            if self.inside_rect(rect):
                return True
        return False
    def inside_rect(self, rect):
        x1 = rect[0]
        y1 = rect[1]
        x2 = rect[2] + x1
        y2 = rect[3] + y1
        mouse = self.mouse_pos()
        if mouse[0] > x1 and mouse[0] < x2:
            if mouse[1] > y1 and mouse[1] < y2:
                return True
        return False


ds = draw_sistem()

menu_pos = [50,40]
menu_size = [WIDTH-100,75]

def draw_grid(start,size, num, spacing, color, dir):
    global menu, key
    text = ["Library", "Battle","Shop","Trade"]
    for i in range(num):
        if dir:

            if i == menu:
                ds.draw_rectangle([start[0]+i*(spacing+size[0]),start[1]],size,[140,140,140],0,255,0,7)
                ds.draw_rectangle([start[0] + i * (spacing + size[0]), start[1]], size, [100, 100, 100], 0, 255, 2, 7)
            else:
                ds.draw_rectangle([start[0] + i * (spacing + size[0]), start[1]], size, color, 0, 255, 0, 7)
                ds.draw_rectangle([start[0] + i * (spacing + size[0]), start[1]], size, [200, 200, 200], 0, 255, 2, 7)
            if ds.click_in_rect([start[0]+i*(spacing+size[0]),start[1], size[0], size[1]]):
                menu = i
                key = []
            ds.draw_text(text[i], [start[0] + i * (spacing + size[0])+15, start[1]+9], 28, [0,0,0], 0, 255)
        else:
            ds.draw_rectangle([start[0], start[1]+i*(spacing+size[1])], size, color, 0, 255, 0, 3)


def draw_menu():
    ds.draw_rectangle([0,0], [WIDTH, 150], [255,255,255], 0, 0, 0, 0)
    ds.draw_rectangle([50,40],[WIDTH-100,61],[220,220,220], 0, 0, 0, 5)
    draw_grid([75,53],[100, 35],4,15,[210,210,210],True)

menu = 0

# 1 = library

def draw_card(id, level, pos, size):
    if (f"{id}:{level}") in cache:
        img = cache[f"{id}:{level}"]
    else:
        img = ds.load_image(f"card{id}.png")
        font = pygame.font.SysFont("Consolas", 12)
        text_surface = font.render("Life : 500", True, [255, 255, 255])
        img.blit(text_surface, [12, 170])
        text_surface = font.render("Ataq : 25", True, [255, 255, 255])
        img.blit(text_surface, [12, 207])
        text_surface = font.render(f"{level}", True, [255, 255, 255])
        img.blit(text_surface, [115, 207])
        font = pygame.font.SysFont("Consolas", 12)
        text_surface = font.render(f"{id}", True, [0,0,0])
        img.blit(text_surface, [7, 7])
        img = ds.transfome_image(img, size)
        cache[f"{id}:{level}"] = img
    if pos[0] > -size[0] and pos[0] < WIDTH + size[0] and pos[1] > -size[1] and pos[1] < HEIGHT + size[1]:
        screen.blit(img, pos)

menu_now = 0
menu_n = 0
def update_menu():
    global menu, menu_now, menu_n
    smoothing = 0.1
    target = menu * 100
    menu_n += (target - menu_n) * smoothing
    menu_now = -menu_n / 100


def draw_library():
    global menu_now
    cards_num = len(info.get_cards())
    cards = info.get_cards()
    columns = 3
    card_width = 150
    card_height = 250
    spacing = 15
    rows = (cards_num + columns - 1) // columns
    x_offset = int((WIDTH * menu_now))
    y_offset = 185 + scroll
    sy = rows * (card_height + spacing)+5
    if cards_num == 0:
        sy = HEIGHT/2
    ds.draw_rectangle([WIDTH // 4 - 100+x_offset, y_offset], [WIDTH - 100, sy], [220, 220, 220], 0, 255, 0, 8)
    ds.draw_rectangle([WIDTH // 4 - 100+x_offset, y_offset-30],[150,25],[210,210,210],0,0,0,4)
    ds.draw_text(f"Cards : {cards_num}",[WIDTH // 4 - 100+x_offset, y_offset-30], 20,[15,15,15],0,255, "Arial")
    if cards_num==0:
        ds.draw_text(f"You don't have any cards", [WIDTH /4-5+x_offset, HEIGHT / 2-120], 25, [15, 15, 15], 0, 255, "Consolas")
        return
    for i, card in enumerate(cards):
        row = i // columns
        col = i % columns
        x = WIDTH // 4 + col * (card_width + spacing) - 90 + x_offset
        y = y_offset + row * (card_height + spacing) + 10

        try:
            draw_card(card[0], card[1], [x, y], [card_width, card_height])
        except:
            draw_card(1, 1, [x, y], [card_width, card_height])

active_pop_up = []


def update_pop_up():
    global active_pop_up
    for i, pop_up in enumerate(active_pop_up[:]):

        x = max(0, pop_up[2])

        ds.draw_rectangle([x, HEIGHT - 100], [WIDTH + 15, 100], [210, 210, 210], 0, 255, 0, 2)
        ds.draw_text(pop_up[0],[x+25,HEIGHT-96],45,[0,0,0],0,255)
        ds.draw_text(pop_up[1], [x + 100, HEIGHT - 66], 25, [0, 0, 0], 0, 255)

        pop_up[2] -= 12

        if pop_up[2] < -WIDTH*3:
            active_pop_up.remove(pop_up)
            return
        print(pop_up)
        active_pop_up[i] = pop_up


def pop_up_notification(titulo, mensagem):
    global active_pop_up
    active_pop_up.append([titulo, mensagem, WIDTH])

class battle_handle:
    def __init__(self):
        self.type = "None"
        self.connected = False
        self.user_name = ""

    def search(self, ip):
        print("procurando ip")
        pop_up_notification(f"starting connection to IP:{ip}", "")

    def get_user_name(self):
        with open("player_info", "r") as arq:
            info = arq.read().split("\n")
            name = info[0]
            return name

    def start_Net(self):
        if self.type == "Server":
            info = Net_S.wait_message()
            print(info)
            Net_S.send("Hi")
        elif self.type == "Client":
            Net_C.send("Hello")
            info = Net_C.wait_message()
            print(info)

    def draw_ip_section(self,x_offset):
        ds.draw_text("Seu IP local:", [WIDTH / 3 - 50 + x_offset, HEIGHT / 3 - 68], 25, [150, 150, 150], 0, 255)
        ds.draw_rectangle([WIDTH / 3 - 50 + x_offset, HEIGHT / 3 - 50], [300, 35], [220, 220, 220], 0, 255, 0, 5)

        # ip shower ou hider
        if ds.inside_rect([WIDTH / 3 + 255 + x_offset, HEIGHT / 3 - 43, 42, 20]):
            ds.draw_text(f"{obter_ip_local()}", [WIDTH / 3 - 50 + x_offset, HEIGHT / 3 - 43], 25, [0, 0, 0], 0, 255,
                         "Consolas")
            ds.draw_image("ip_show.png", [WIDTH / 3 + 255 + x_offset, HEIGHT / 3 - 43], [42, 20])
        else:
            ds.draw_text("x.x.x.x", [WIDTH / 3 - 50 + x_offset, HEIGHT / 3 - 43], 25, [0, 0, 0], 0, 255, "Consolas")
            ds.draw_image("ip_hide.png", [WIDTH / 3 + 255 + x_offset, HEIGHT / 3 - 43], [42, 20])

    def draw_enemy_input_section(self, x_offset, ip):
        ds.draw_rectangle([WIDTH / 3 - 50 + x_offset, HEIGHT / 3], [300, 35], [220, 220, 220], 0, 255, 0, 5)

        # input prompter
        if len(key) == 0:
            ds.draw_text("Digite o IP do oponente", [WIDTH / 3 - 45 + x_offset, HEIGHT / 3 + 9], 25, [235, 235, 235], 0, 255)
        else:
            ds.draw_text(ip, [WIDTH / 3 - 45 + x_offset, HEIGHT / 3 + 9], 25, [0, 0, 0], 0, 255)

    def draw_search_button(self, x_offset, ip):
        button_rect = [WIDTH / 2 - 75 + x_offset, HEIGHT / 3 + 58, 150, 35]

        if ds.click_in_rect(button_rect) and self.type == "None":
            ds.draw_rectangle(button_rect[:2], button_rect[2:], [20, 180, 20], 0, 255, 0, 5)
            try:
                if ip:
                    print(f"serach {ip}")
                    ok = Net_C.conect(ip)
                    if ok != 0:
                        o = 1/0
                    Net_C.send(self.get_user_name())
                    name = Net_C.wait_message()
                    self.user_name = name
                    print(name)
            except:
                pop_up_notification(f"fail to connect to {ip}", f"A conecction to {ip} fail")
        else:
            ds.draw_rectangle(button_rect[:2], button_rect[2:], [20, 220, 20], 0, 255, 0, 5)

        ds.draw_text("Search Battle", [WIDTH / 2 - 58 + x_offset, HEIGHT / 3 + 40 + 28], 25, [235, 235, 235], 0, 255)

    def draw_start_server_button(self, x_offset):
        button_rect = [WIDTH / 2 - 75 + x_offset, HEIGHT / 3 + 200, 150, 35]

        if ds.click_in_rect(button_rect) and self.type == "None":
            ds.draw_rectangle(button_rect[:2], button_rect[2:], [225, 110, 0], 0, 255, 0, 5)
            Net_S.start()
            name = Net_S.wait_message()
            self.user_name = name
            print(name)
            Net_S.send(self.get_user_name())
        else:
            ds.draw_rectangle(button_rect[:2], button_rect[2:], [255, 140, 0], 0, 255, 0, 5)

        ds.draw_text("Start Battle", [WIDTH / 2 - 58 + x_offset, HEIGHT / 3 + 40 + 28], 25, [235, 235, 235], 0, 255)

    def draw_battle(self):
        x_offset = WIDTH + int((WIDTH * menu_now))
        y_offset = 185
        ip = "".join(key)
        if self.type == "None":
            self.draw_ip_section(x_offset)
            self.draw_enemy_input_section(x_offset, ip)
            self.draw_search_button(x_offset, ip)
            self.draw_start_server_button(x_offset)

login = False
user_name = None
cap = False
key = []

with open("player_info", "r") as arq:
    infos = [line.replace("\n","") for line in arq]
    if len(infos)>0:
        login = True
        user_name = infos[0]
        menu = 0



def draw_login():
    global login, user_name, menu
    ds.draw_text("Welcome", [WIDTH / 2 - 50, HEIGHT / 4-50], 30, [150, 150, 150], 0, 255)
    ds.draw_text("Login:", [WIDTH / 3 - 50, HEIGHT / 3 - 28], 25, [150, 150, 150], 0, 255)
    ds.draw_text(" Seu nome não pode ser alterado depois de confirmar:", [WIDTH / 3 - 50, HEIGHT / 3+37], 15, [150, 150, 150], 0, 255)
    ds.draw_rectangle([WIDTH / 3 - 50, HEIGHT / 3], [300, 35], [220, 220, 220], 0, 255, 0, 5)
    if len(key)==0:
        ds.draw_text(" Digite seu User Name", [WIDTH / 3 - 50, HEIGHT / 3+9], 25, [235, 235, 235], 0, 255)
    else:
        ds.draw_text("".join(key), [WIDTH / 3 - 45, HEIGHT / 3 + 9], 25, [0,0,0], 0, 255)
    if ds.click_in_rect([WIDTH / 2-75, HEIGHT / 3+58,150, 35]):
        ds.draw_rectangle([WIDTH / 2 - 75, HEIGHT / 3 + 58], [150, 35], [20, 180, 20], 0, 255, 0, 5)
        if len(key)>0:
            with open("player_info", "w") as arq:
                login = True
                user_name = "".join(key)
                arq.write(str(user_name))
                menu = 0
    else:
        ds.draw_rectangle([WIDTH / 2 - 75, HEIGHT / 3 + 58], [150, 35], [20, 220, 20], 0, 255, 0, 5)
    ds.draw_text(" Confirmar", [WIDTH / 2 - 45, HEIGHT / 3 + 40 + 26], 25, [235, 235, 235], 0, 255)

bh = battle_handle()
pygame.mouse.set_visible(False)
running = True
while running:
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:

            i = info.get_cards()
            scroll_max = len(i)//3 *265
            if scroll_max<0:
                scroll_max = 0
            if event.button == 4:
                scroll_target += scroll_size
                if scroll_target > 0:
                    scroll_target = 0
            elif event.button == 5:
                scroll_target -= scroll_size
                if scroll_target < -scroll_max:
                    scroll_target = -scroll_max
            click = True
        elif event.type == pygame.KEYDOWN:
            key_name = pygame.key.name(event.key)
            if len(key_name)==1 and len(key)<25:
                if key_name in ["1","2","3","4","5","6","7","8","9","0","","."]:
                    if cap:
                        key.append(key_name.upper())
                    else:
                        key.append(key_name)
            else:
                if key_name == "space":
                    key.append(" ")
                elif key_name == "backspace":
                    if len(key)>0:
                        key.pop()
                elif key_name == "caps lock":
                    cap = not cap

    scroll += (scroll_target - scroll) * scroll_speed
    pygame.display.set_caption(str(clock.get_fps()))

    if login:
        if round(abs(menu_now),2) > -0.5 and round(abs(menu_now),2) < 1.5:
            draw_library()
        if round(abs(menu_now),2) > 0.5 and round(abs(menu_now),2) < 2.5:
            bh.draw_battle()

        draw_menu()

    else:
        draw_login()
    update_menu()
    update_pop_up()
    ds.draw_image("Mouse.png",ds.mouse_pos(),[25,25])
    render()

pygame.quit()
sys.exit()
