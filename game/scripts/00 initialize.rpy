# The script of the game goes in this file.

# callback=speaker is needed for mouth flaps
define war = Character("Warren", callback=speaker("war"))
define paz = Character("Paz", callback=speaker("paz"))

init python:
    # define the BGs
    DefineImages('bgs', prepend='bg')

    # define the sprites with manual layer ordering
    #layerorder = None
    layerorder = ['base','blush','mouth','eyes', 'hair', 'sweat','heavysweat']
    DefineImages("sprites", overrideLayerOrder=layerorder)

    # manually create shortcuts to more complex expressions
    MapEmote('war angry',  'war ed sad md pout blush')

# override some default mouth flap behaviours
# image fang md surprised     = "fang mdo surprised"
# image alex pose1 md scared  = FlapMouth("alex pose1 m scared", "alex pose1 mc bitter")

# The game starts here.

label start:
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg computerlab

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show war angry:
        xalign 0.3

    # These display lines of dialogue.

    war "Hello, world."
    bubble war "This time with a bubble!"
    bubble scale 1.5 war "Make much bigger bubbles if there's lot to say..."
    bubble scale 0.6 war "...or smaller ones."
    bubble narrate "This is a narration text for the scene. It's not an active thought of the character, but more like an inner monologue of the main character."
    bubble think war "A thinking bubble would be more like this. Notice the mouth doesn't move here..."
    bubble whisper war "There's also a whisper bubble. Shh..."

    show war bigsmile blush
    bubble happy war "Or a happy, excited bubble!"

    show paz puff:
        xalign 0.7

    bubble shout paz "Which is different from a shouty bubble!"

    show paz sad blush
    bubble wobbly paz "There's also the wobbly bubble, for shaky voices..."

    show paz pout heavysweat
    bubble weird paz "Which is different from the supernaturally weird bubble..."

    show war default
    bubble diagonal war "There's also bubbles with extra diagonal arrowheads..."

    show paz smug
    bubble plain paz "...and bubbles with no arrowheads."

    bubble diagonal xalign 0.4 yalign 0.6 paz "You can put the bubbles anywhere, instead of having it folow a character..."
    bubble diagonal xflip yflip xalign 0.6 yalign 0.1 war "...flip it both vertically and horizontally AND choose a custom position."
    bubble paz "Or you chould just let the code decide for you."

    "Demo has ended."
    # This ends the game.

    return
