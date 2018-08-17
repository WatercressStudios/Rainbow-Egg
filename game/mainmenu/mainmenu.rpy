# Show fancy comic panel main menu

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

screen main_menu_buttons:
    imagebutton action Null:
        align (0.99, 0.5)
        idle "start_button"
    imagebutton action Jump("main_menu"):
        align (0.5, 0.01)
        idle "settings_button"
    imagebutton action Jump("main_menu"):
        align (0.5, 0.99)
        idle "continue_button"

label main_menu:
    scene black
    scene mm background with Dissolve(1.0):
        align (0.25, 0.53)

    call screen main_menu_buttons

label main_menu_start:
    show mm background:
        ease 1.5 align (1.0, 0.605) zoom 1.25
    pause 1.5
    scene bg computerlab with Dissolve(0.5):
    return
