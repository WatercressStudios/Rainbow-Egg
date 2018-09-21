label day1:
    scene bg twins
    scene bg twins:
        parallel:
            easeout 2.0 zoom 2.5
        parallel:
            easein 2.0 yalign 0.5 xalign 1.0
    pause 2.0
    bubble plain xalign 0.58 yalign 0.2 "So how’s the spring semester going, you guys?"
    show war smile with Dissolve(1.0):
        xalign 0.3 zoom 1.25
    bubble war "Um, it's good, I—"

    show paz:
        xalign 0.9 zoom 2.0 alpha 0.0
        ease 0.15 zoom 1.1 alpha 1.0
        ease 0.15 zoom 1.25
    pause 0.3
    bubble happy paz "Oh, it's been {b}great!{/b}"
    bubble happy paz "I met this girl on the cheerleading squad, Lydia, and we hit it off immediately."
    bubble happy paz "We’ve been going out for about a week now!"
    bubble plain xalign 0.58 yalign 0.2 "...{i}Lydia?{/i} What happened to your last girlfriend?"
    bubble narrate xalign 0.0 "That's our mom on Skype. Normally it's my twin sister Paz who delivers the shocking news of the day, but today..."
    bubble happy paz "Kendra? Kendra’s {b}great!{/b} We went on a date Wednesday night."

    show war smile sweat
    bubble war "Umm..."
    bubble plain xalign 0.58 yalign 0.2 "Who is {b}Kendra?{/b}I was talking about Sabeen!"
    bubble happy paz "Sabeen’s good too! She says hi!"
    bubble plain xalign 0.58 yalign 0.2 "Wait, are you dating {i}three{/i} different women?"
    bubble happy paz "Don’t be ridiculous!"
    bubble paz "...I'm dating nine."
    bubble plain xalign 0.58 yalign 0.2 "...Oh."
    bubble plain xalign 0.58 yalign 0.2 "..."
    bubble plain xalign 0.58 yalign 0.2 "...So, are you using prote—"

    show war angry sweat with hpunch
    bubble shout war "Mom!!"
    show war smile sweat
    bubble war "Wasn’t there something you wanted to tell us?"
    bubble plain xalign 0.58 yalign 0.2 "Oh. Yes."
    bubble happy xalign 0.58 yalign 0.2 yflip "I have some exciting news for you kids!"
    bubble paz "..."
    show war smile
    bubble war "..."
    bubble plain xalign 0.58 yalign 0.2 "Well, aren’t you going to guess?"
    bubble war "..."
    bubble wobbly war "No?"
    bubble happy paz "Did you find the dried-up body of an old sea captain in the attic?"
    show war angry
    bubble war "{i}What?!{/i}"
    bubble plain xalign 0.58 yalign 0.2 "No, that was in the old house."
    show war angry sweat
    bubble war "Hold on."
    bubble happy xalign 0.58 yalign 0.2 yflip "So, exciting news!"
    show war angry heavysweat
    bubble war "Wait, no, go back."
    bubble happy xalign 0.58 yalign 0.2 yflip "In seven months you’re gonna have a little brother!"
    bubble paz "..."
    show war angry
    bubble war "..."

    show war angry heavysweat with hpunch
    bubble shout xalign 0.6 yalign 0.8 "{b}WHAT?!{/b}"


    show war:
        ease 0.5 xalign 0.5
    pause 0.5
    menu:
        "Minor choice number 1.":
            show war:
                ease 0.5 xalign 0.3
            pause 0.5
            bubble war "I picked choice number 1."

        "Minor choice number 2.":
            show war:
                ease 0.5 xalign 0.3
            pause 0.5
            bubble war "I picked choice number 2."

    bubble narrate "Now trying the OTHER choice style..."

    show war:
        ease 0.5 xalign 0.5
    show josh_classroom:
        xpos -1.0
        ease 0.5 xpos -0.65
    show mel_computerlab:
        xpos 1.0
        ease 0.5 xpos 0.65
    pause 0.5
    bubble think war "Major choice...Josh or Mel?"

    "Demo has ended."
    # This ends the game.

    return
