# Show fancy comic panel main menu

init python:
    config.layers += [ 'custommenu' ]

image start_button:
    zoom 0.8
    "mainmenu/start_button_1.png"
    pause 0.2
    "mainmenu/start_button_2.png"
    pause 0.2
    repeat

image settings_button:
    zoom 0.8
    "mainmenu/settings_button_1.png"
    pause 0.2
    "mainmenu/settings_button_2.png"
    pause 0.2
    repeat

image continue_button:
    zoom 0.8
    "mainmenu/continue_button_1.png"
    pause 0.2
    "mainmenu/continue_button_2.png"
    pause 0.2
    repeat

image back_button:
    zoom 0.8
    "mainmenu/back_button_1.png"
    pause 0.2
    "mainmenu/back_button_2.png"
    pause 0.2
    repeat

screen main_menu_buttons:
    layer "custommenu"
    image "mm vignette"
    imagebutton action Jump("main_menu_start"):
        align (0.99, 0.5)
        idle "start_button"
    imagebutton action Jump("settings_menu"):
        align (0.5, 0.01)
        idle "settings_button"
    imagebutton action Jump("continue_menu"):
        align (0.5, 0.99)
        idle "continue_button"

screen settings_buttons:
    layer "custommenu"
    image "mm vignette"
    imagebutton action Jump("back_main_menu"):
        align (0.5, 0.99)
        idle "back_button"

screen continue_buttons:
    layer "custommenu"
    image "mm vignette"
    imagebutton action Jump("back_main_menu"):
        align (0.5, 0.01)
        idle "back_button"

label settings_menu:
    show mm background:
        ease 1 align (0.3, 0.0) zoom 1.1
    show mm vignette onlayer custommenu
    $ renpy.pause(1, hard=True)
    hide mm vignette onlayer custommenu
    call screen settings_buttons

label continue_menu:
    show mm background:
        ease 1 align (0.1, 1.0) zoom 1.25
    show mm vignette onlayer custommenu
    $ renpy.pause(1, hard=True)
    hide mm vignette onlayer custommenu
    call screen continue_buttons

label back_main_menu:
    show mm background:
        ease 1 align (0.25, 0.53) zoom 1
    show mm vignette onlayer custommenu
    $ renpy.pause(1, hard=True)
    hide mm vignette onlayer custommenu
    call screen main_menu_buttons

label main_menu:
    scene black
    show mm background:
        align (0.25, 0.53)
        alpha 0
        linear 1.0 alpha 1.0
    call screen main_menu_buttons

label main_menu_start:
    show mm background:
        ease 1.5 align (1.0, 0.605) zoom 1.25
    show mm vignette onlayer custommenu
    hide mm vignette onlayer custommenu with Dissolve(1.5)
    scene bg computerlab with Dissolve(0.5):
    return
