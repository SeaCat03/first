import os
import sys
import pygame
import requests
import pygame_gui

pygame.init()
geocoder_key = "40d1649f-0493-4b70-98ba-98533de7710b"
schirota, dolgota = 51.558403, 46.038191
schirota_metki, dolgota_metki = 51.558403, 46.038191
x_maschtab = 0.01
map_file = "map.png"
running = True
screen = pygame.display.set_mode((800, 450))
screen.fill((255, 255, 255))
fon = pygame.font.Font(None, 24)
GREEN = (0, 200, 64)
type_cart = 'map'
city_add = ''
login = ''
manager = pygame_gui.UIManager((800, 450), 'theme.json')
manager_hybrid = pygame_gui.UIManager((800, 450), 'theme_1.json')
manager_map = pygame_gui.UIManager((800, 450), 'theme2.json')
manager_sat = pygame_gui.UIManager((800, 450), 'theme3.json')
# -------------------------
#------------
map_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 20), (100, 40)),
    text='',
    manager=manager_map)
#pygame.draw.rect(screen, GREEN, (50, 20, 100, 40))
#--------------
#pygame.draw.rect(screen, GREEN, (50, 80, 100, 40))
sat_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 80), (100, 40)),
    text='',
    manager=manager_sat)
#---------------
#pygame.draw.rect(screen, GREEN, (50, 140, 100, 40))
hyb_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((50, 140), (100, 40)),
    text='',
    manager=manager_hybrid)
#----------
login_text = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((0, 200), (200, 25)), manager=manager)
#----------------
login_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((0, 250), (200, 50)),
    text='',
    manager=manager)

def get_coords():
    global schirota
    global dolgota
    global schirota_metki
    global dolgota_metki
    geo_req = 'http://geocode-maps.yandex.ru/1.x/'
    geo_param = {
        'apikey': geocoder_key,
        'geocode': city_add,
        'format': 'json'
    }
    geo_resp = requests.get(geo_req, params=geo_param)
    json_data = geo_resp.json()
    data = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    coord_adr = data["Point"]["pos"]
    dolgota, schirota = map(float, coord_adr.split(' '))
    dolgota_metki, schirota_metki = map(float, coord_adr.split(' '))

    # Сюда можно добавить анализ ответа на ошибку




def get_cart():
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={dolgota},{schirota}&size=600,450&spn={x_maschtab},{x_maschtab}&l={type_cart}&pt={dolgota_metki},{schirota_metki},flag"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    with open(map_file, "wb") as file:
        file.write(response.content)

#Саратов, ул.Державинская, дом 5

clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0
    get_cart()
    screen.blit(pygame.image.load(map_file), (200, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                print('mkjkj')
                if x_maschtab >= 0.001:
                    if x_maschtab <= 0.01:
                        n = x_maschtab / 2
                        x_maschtab -= n
                    else:
                        n = x_maschtab / 2
                        x_maschtab -= n
                    get_cart()
            elif event.key == pygame.K_PAGEUP:
                if x_maschtab <= 50:
                    n = 0.01
                    x_maschtab += x_maschtab
                    get_cart()
            elif event.key == pygame.K_UP:
                schirota += 0.01
                get_cart()
            elif event.key == pygame.K_DOWN:
                schirota -= 0.01
                get_cart()
            elif event.key == pygame.K_LEFT:
                dolgota -= 0.01
                get_cart()
            elif event.key == pygame.K_RIGHT:
                dolgota += 0.01
                get_cart()


        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == login_text:
                    login = event.text



            elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == login_button:
                    city_add = login
                    get_coords()
                elif event.ui_element == map_button:
                    type_cart = 'map'
                elif event.ui_element == sat_button:
                    type_cart = 'sat'
                elif event.ui_element == hyb_button:
                    type_cart = 'sat,skl'

        manager.process_events(event)
        manager_hybrid.process_events(event)
        manager_map.process_events(event)
        manager_sat.process_events(event)
    manager.update(time_delta)
    manager_sat.update(time_delta)
    manager_map.update(time_delta)
    manager_hybrid.update(time_delta)
    screen.blit(pygame.image.load(map_file), (200, 0))
    manager.draw_ui(screen)
    manager_sat.draw_ui(screen)
    manager_map.draw_ui(screen)
    manager_hybrid.draw_ui(screen)
    pygame.display.update()
    pygame.display.flip()

os.remove(map_file)

# 51.558403 46.038191
