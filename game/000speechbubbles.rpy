###############################
#
# COPY AND REPLACE THE "SCREEN SAY" FUNCTION BELOW IN SCREENS.RPY
# ALSO, MIGHT WANT TO CONSIDER USING THE ACTION MAN FONT WITH LINE SPACING 10
#
# screen say(who, what, show_who=True, text_params=None, bubble_params=None):
#     style_prefix "say"
# 
#     window:
#         id "window"
# 
#         if bubble_params:
#             xalign None
#             yalign None
#             xpos bubble_params[0][0]
#             ypos bubble_params[0][1]
#             xsize bubble_params[1][0]
#             ysize bubble_params[1][1]
#             background bubble_params[2]
#         else:
#             background Image("gui/textbox.png")
# 
#         if show_who and who is not None:
#             window:
#                 style "namebox"
#                 text who id "who"
# 
#         if text_params:
#             window:
#                 pos (None, None)
#                 align (None, None)
#                 offset (None, None)
#                 xsize None
#                 ysize None
#                 xfill True
#                 yfill True
#                 background None
#                 text what id "what":
#                     xoffset text_params[0][0]
#                     yoffset text_params[0][1]
#                     xsize text_params[1][0]
#                     ysize text_params[1][1]
#                     xalign text_params[2][0]
#                     yalign text_params[2][1]
#                     text_align text_params[3]
#         else:
#             text what id "what"
# 
#     ## If there's a side image, display it above the text. Do not display on the
#     ## phone variant - there's no room.
#     if not renpy.variant("small"):
#         add SideImage() xalign 0.0 yalign 1.0
#

python early:

    def parse_bubble(lex):
        # Default values
        who = None
        what = None

        bubble_pos = [None, None]
        bubble_size = [500, 300]
        bubble_background = "speechbubble/speech_bubble_above.png"
        bubble_flip = [None, None]
        bubble_offset = [150, 150]
        bubble_y_range = [400, 930]
        
        text_offset = [-10, 15]
        text_size = [380, 200]
        text_align = [0.5, 0.5]
        text_text_align = 0.5

        # Based on what the user passed in, overwrite  the default values
        while not lex.eol():
            token = lex.simple_expression()
            if token == "shout":
                bubble_background = "speechbubble/speech_bubble_shout.png"
                bubble_size = [550, 300]
                bubble_offset = [0, 0]
                text_offset = [8, 5]
                text_size = [350, 200]
            elif token == "happy":
                bubble_background = "speechbubble/speech_bubble_happy.png"
                text_offset = [-3, 12]
            elif token == "wobbly":
                bubble_background = "speechbubble/speech_bubble_wobbly.png"
                bubble_offset = [250, 250]
                text_offset = [-3, 12]
            elif token == "diagonal":
                bubble_background = "speechbubble/speech_bubble_diagonal.png"
                bubble_offset = [300, 300]
                bubble_y_range = [500, 600]
                text_offset = [-3, 12]
            elif token == "plain":
                bubble_background = "speechbubble/speech_bubble.png"
                text_offset = [-3, 5]
                bubble_offset = [0, 0]
            elif token == "weird":
                bubble_background = "speechbubble/speech_bubble_weird.png"
                bubble_size = [550, 300]
                text_offset = [0, 15]
                bubble_offset = [0, 0]
            elif token == "whisper":
                bubble_background = "speechbubble/speech_bubble_whisper.png"
                text_offset = [-3, 12]
                bubble_offset = [0, 0]
            elif token == "think":
                bubble_background = "speechbubble/speech_bubble_think.png"
                bubble_offset = [200, 200]
                bubble_y_range = [350, 450]
                text_offset = [-3, 18]
            elif token == "narrate":
                bubble_background = "speechbubble/speech_bubble_narrate.png"
                bubble_size = [450, 600]
                bubble_offset = [0, 0]
                text_offset = [-5, 0]
                text_size = [380, 530]
            elif token == "xflip":
                bubble_flip[0] = True
            elif token == "yflip":
                bubble_flip[1] = True
            elif token == "xpos":
                bubble_pos[0] = float(lex.simple_expression().strip("\"'"))
                if bubble_pos[0] > 1.0:
                    bubble_pos[0] = int(bubble_pos[0])
            elif token == "ypos":
                bubble_pos[1] = float(lex.simple_expression().strip("\"'"))
                if bubble_pos[1] > 1.0:
                    bubble_pos[1] = int(bubble_pos[1])
            elif token == "xalign":
                bubble_pos[0] = int(float(lex.simple_expression().strip("\"'")) * (renpy.config.screen_width - bubble_size[0]))
            elif token == "yalign":
                bubble_pos[1] = int(float(lex.simple_expression().strip("\"'")) * (renpy.config.screen_height - bubble_size[1]))
            elif token == "xscale":
                scale = float(lex.simple_expression().strip("\"'"))
                bubble_size[0] = int(scale * bubble_size[0])
                text_size[0] = int(scale * text_size[0])
            elif token == "yscale":
                scale = float(lex.simple_expression().strip("\"'"))
                bubble_size[1] = int(scale * bubble_size[1])
                text_size[1] = int(scale * text_size[1])
            elif token == "scale":
                scale = float(lex.simple_expression().strip("\"'"))
                bubble_size[0] = int(scale * bubble_size[0])
                text_size[0] = int(scale * text_size[0])
                bubble_size[1] = int(scale * bubble_size[1])
                text_size[1] = int(scale * text_size[1])
            elif lex.eol():
                who = "narrator"
                if bubble_pos[0] is None:
                    bubble_pos[0] = renpy.config.screen_width - bubble_size[0]
                if bubble_pos[1] is None:
                    bubble_pos[1] = 0
                what = token
            else:
                who = token
                what = lex.rest()

        # Wrap up the params and return it to renpy
        bubble_params = bubble_pos, bubble_size, bubble_background, bubble_flip, bubble_offset, bubble_y_range
        text_params = text_offset, text_size, text_align, text_text_align
        return (who, eval(what), bubble_params, text_params)


    def execute_bubble(o):
        # Unwrap all variables - there are a lot!
        who, what, bubble_params, text_params = o
        text_offset, text_size, text_align, text_text_align = text_params
        bubble_pos, bubble_size, bubble_background, bubble_flip, bubble_offset, bubble_y_range = bubble_params
        think = "_think" in bubble_background
        if not who == "narrator":
            xpos, ypos, width, height = renpy.get_image_bounds(who)

        # Making copies so they don't overwrite the originals, which may still be needed
        text_offset = list(text_offset)
        text_size = list(text_size)
        text_align = list(text_align)
        bubble_pos = list(bubble_pos)
        bubble_size = list(bubble_size)
        bubble_background = Image(bubble_background)
        bubble_flip = list(bubble_flip)
        bubble_offset = list(bubble_offset)
        bubble_y_range = list(bubble_y_range)

        # Scale image to the requested size, and all coordinates to 0-1 space
        bubble_background = im.Scale(bubble_background, bubble_size[0], bubble_size[1])
        bubble_size = (1.0*bubble_size[0]/renpy.config.screen_width, 1.0*bubble_size[1]/renpy.config.screen_height)
        bubble_offset = (1.0*bubble_offset[0]/renpy.config.screen_width, 1.0*bubble_offset[1]/renpy.config.screen_height)

        # Automatically determine xpos of bubble if not set
        if bubble_pos[0] is None:
            xpos_center = (xpos + width/2.0) / renpy.config.screen_width
            if xpos_center - bubble_size[0]/2.0 - bubble_offset[0] < 0.0:
                # If bubble goes over the left edge, place it on the right
                bubble_pos[0] = xpos_center - bubble_size[0]/2.0 + bubble_offset[0]
                if bubble_flip[0] is None:
                    bubble_flip[0] = True
            elif xpos_center + bubble_size[0]/2.0 + bubble_offset[0] > 1.0:
                # If bubble goes over the right edge, place it on the left
                bubble_pos[0] = xpos_center - bubble_size[0]/2.0 - bubble_offset[0]
            else:
                # Decide based on other characters on screen
                left_nearest = 1.0
                right_nearest = 1.0
                for cha in renpy.get_showing_tags():
                    if cha in ('bg', 'cg', who):
                        continue
                    xpos2, ypos2, width2, height2 = renpy.get_image_bounds(cha)
                    xpos2_center = (xpos2 + width2/2.0) / renpy.config.screen_width
                    if xpos2_center < xpos_center:
                        left_nearest = min(left_nearest, xpos_center - xpos2_center)
                    else:
                        right_nearest = min(right_nearest, xpos2_center - xpos_center)
                if right_nearest > left_nearest:
                    # If character on the left is nearer, put speech bubble on the right
                    bubble_pos[0] = xpos_center - bubble_size[0]/2.0 + bubble_offset[0]
                    if bubble_flip[0] is None:
                        bubble_flip[0] = True
                else:
                    # Otherwise default to left
                    bubble_pos[0] = xpos_center - bubble_size[0]/2.0 - bubble_offset[0]
            if bubble_pos[0] < 0.0:
                bubble_pos[0] = 0.0
            elif bubble_pos[0] + bubble_size[0] > 1.0:
                bubble_pos[0] = 1.0 - bubble_size[0]

        # Automatically determine ypos of bubble if not set
        if bubble_pos[1] is None:
            ypos_center = 1.0 * renpy.random.randint(bubble_y_range[0], bubble_y_range[1]) / renpy.config.screen_height
            bubble_pos[1] = ypos_center - bubble_size[1]/2.0
            if bubble_pos[1] < 0.0:
                bubble_pos[1] = 0.0
            elif bubble_pos[1] + bubble_size[1] > 1.0:
                bubble_pos[1] = 1.0 - bubble_size[1]

        # Apply the flips on the background
        if bubble_flip[0]:
            bubble_background = im.Flip(bubble_background, horizontal=True)
        if bubble_flip[1]:
            bubble_background = im.Flip(bubble_background, vertical=True)

        if think:
            who = "narrator"
#         if bubble_flip[0]:
#             text_offset[0] = -text_offset[0]
#             text_align[0] = 1.0 - text_align[0]
#         if bubble_flip[1]:
#             text_offset[1] = -text_offset[1]
#             text_align[1] = 1.0 - text_align[1]

        # Rewrap the text and bubble params and now send everything to "screen say"
        text_params = text_offset, text_size, text_align, text_text_align
        bubble_params = bubble_pos, bubble_size, bubble_background, bubble_flip, bubble_offset, bubble_y_range
        renpy.say(eval(who), what, show_show_who=False, show_text_params=text_params, show_bubble_params=bubble_params)


    def lint_bubble(o):
        who, what, bubble_params, text_params = o
        try:
            eval(who)
        except:
            renpy.error("Character not defined: %s" % who)

        tte = renpy.check_text_tags(what)
        if tte:
            renpy.error(tte)

    renpy.register_statement("bubble", parse=parse_bubble, execute=execute_bubble, lint=lint_bubble)

