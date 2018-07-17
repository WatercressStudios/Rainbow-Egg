###############################
#
# COPY AND PASTE THE "SCREEN SAY" CODE BELOW IN SCREENS.RPY
# ALSO, MIGHT WANT TO CONSIDER USING THE ACTION MAN FONT, AT LINE SPACING 8
#
# screen say(who, what, show_who=True, text_bounds=None, background_bounds=None, background=Image("gui/textbox.png")):
#     style_prefix "say"
# 
#     window:
#         id "window"
#         if background:
#             background background
#         if background_bounds:
#             xpos background_bounds[0]
#             ypos background_bounds[1]
#             xsize background_bounds[2]
#             ysize background_bounds[3]
# 
#         if show_who and who is not None:
#             window:
#                 style "namebox"
#                 text who id "who"
# 
#         if text_bounds:
#             text what id "what":
#                 xsize text_bounds[0]
#                 ysize text_bounds[1]
#                 xoffset text_bounds[2]
#                 yoffset text_bounds[3]
#                 xalign text_bounds[4]
#                 yalign text_bounds[5]
#                 text_align text_bounds[6]
#         else:
#             text what id "what"
# 
# 
#     ## If there's a side image, display it above the text. Do not display on the
#     ## phone variant - there's no room.
#     if not renpy.variant("small"):
#         add SideImage() xalign 0.0 yalign 1.0
#

python early:
    def parse_say(lex):
        who = lex.simple_expression()
        what = lex.rest()
        return (who, eval(what), None, None, False, False)

    def execute_generic_say(o, background, background_size, offset_size, y_range, text_bounds):
        who, what, xpos_actual, ypos_actual, xflip, yflip = o
        background = im.Scale(background, background_size[0], background_size[1])
        if not xpos_actual or not ypos_actual:
            xpos, ypos, width, height = renpy.get_image_bounds(who)
            background_size = (1.0*background_size[0]/renpy.config.screen_width, 1.0*background_size[1]/renpy.config.screen_height)
            offset_size = (1.0*offset_size[0]/renpy.config.screen_width, 1.0*offset_size[1]/renpy.config.screen_height)
            if not xpos_actual:
                xpos_center = (xpos + width/2.0) / renpy.config.screen_width
                if xpos_center - background_size[0]/2.0 - offset_size[0] > 0.0:
                    xpos_actual = xpos_center - background_size[0]/2.0 - offset_size[0]
                else:
                    xpos_actual = xpos_center - background_size[0]/2.0 + offset_size[0]
                    xflip = True
            if not ypos_actual:
                ypos_center = 1.0 * renpy.random.randint(y_range[0], y_range[1]) / renpy.config.screen_height
                ypos_actual = ypos_center - background_size[1]/2.0
        if xflip:
            background = im.Flip(background, horizontal=True)
        if yflip:
            background = im.Flip(background, vertical=True)
        background_bounds = xpos_actual, ypos_actual, background_size[0], background_size[1]
        renpy.say(eval(who), what, show_show_who=False, show_text_bounds=text_bounds, show_background_bounds=background_bounds, show_background=background)

    def execute_say(o):
        background = "speechbubble/speech_bubble_above.png"
        background_size = (500, 300)
        offset_size = (150, 150)
        y_range = (650, 750)
        
        text_size = (380, 200)
        text_offset = (165, 120)
        text_align = (0.5, 0.5)
        text_text_align = 0.5
        text_bounds = text_size[0], text_size[1], text_offset[0], text_offset[1], text_align[0], text_align[1], text_text_align

        execute_generic_say(o, background, background_size, offset_size, y_range, text_bounds)

    def execute_happy(o):
        background = "speechbubble/speech_bubble_happy_above.png"
        background_size = (500, 300)
        offset_size = (150, 150)
        y_range = (650, 750)
        
        text_size = (380, 200)
        text_offset = (180, 120)
        text_align = (0.5, 0.5)
        text_text_align = 0.5
        text_bounds = text_size[0], text_size[1], text_offset[0], text_offset[1], text_align[0], text_align[1], text_text_align

        execute_generic_say(o, background, background_size, offset_size, y_range, text_bounds)

    def execute_shout(o):
        background = "speechbubble/speech_bubble_shout.png"
        background_size = (500, 300)
        offset_size = (0, 0)
        y_range = (650, 750)
        
        text_size = (350, 200)
        text_offset = (165, 110)
        text_align = (0.5, 0.5)
        text_text_align = 0.5
        text_bounds = text_size[0], text_size[1], text_offset[0], text_offset[1], text_align[0], text_align[1], text_text_align

        execute_generic_say(o, background, background_size, offset_size, y_range, text_bounds)

    def lint_say(o):
        who, what = o
        try:
            eval(who)
        except:
            renpy.error("Character not defined: %s" % who)

        tte = renpy.check_text_tags(what)
        if tte:
            renpy.error(tte)

    renpy.register_statement("say", parse=parse_say, execute=execute_say, lint=lint_say)
    renpy.register_statement("happy", parse=parse_say, execute=execute_happy, lint=lint_say)
    renpy.register_statement("shout", parse=parse_say, execute=execute_shout, lint=lint_say)
