# The script of the game goes in this file.

# callback=speaker is needed for mouth flaps
define fang = Character("Fang", callback=speaker("fang"))
define alex = Character("Alex", callback=speaker("alex"))

init python:
    # define the BGs
    DefineImages('bgs', prepend='bg')

    # define the sprites with manual layer ordering
    #layerorder = None
    layerorder = ['base','blush','mouth','eyes','tears','brow']
    DefineImages("sprites", overrideLayerOrder=layerorder)

    # manually create shortcuts to more complex expressions
    MapEmote('fang surprised',  'fang ed sad md surprised')
    MapEmote('fang happy',      'fang ec default md happy')
    MapEmote('alex scared',     'alex pose1 md scared ed scared blush')

# override some default mouth flap behaviours
image fang md surprised     = "fang mdo surprised"
image alex pose1 md scared  = FlapMouth("alex pose1 m scared", "alex pose1 mc bitter")

# The game starts here.

label start:
    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg street

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    #show fang base ed default md default
    show fang default at left

    # These display lines of dialogue.

    fang "Hello, world."
    bubble fang "...and hello again."
    bubble scale 1.5 fang "Make much bigger bubbles if there's lot to say..."
    bubble scale 0.6 fang "...or smaller ones."
    bubble narrate "This is a narration text for the scene. It's not an active thought of the character, but more like an inner monologue of the main character."
    bubble think fang "A thinking bubble would be more like this."
    bubble whisper fang "There's also a whisper bubble. Shh..."

    show fang happy
    bubble happy fang "Or a happy, excited bubble!"

    #hide fang
    #show alex pose1 shinyarm ed scared md scared brow scared
    #show alex pose1 shinyarm scared
    show alex scared shinyarm at right

    bubble shout alex "Which is different from a shouty bubble!"
    bubble wobbly alex "There's also the wobbly bubble, for shaky voices..."
    bubble weird alex "Which is different from the supernaturally weird bubble..."
    #hide alex

    bubble diagonal fang "There's also bubbles with extra diagonal arrowheads..."
    bubble plain alex "...and bubbles with no arrowheads."
    bubble diagonal xalign 0.4 yalign 0.6 alex "You can put the bubbles anywhere, instead of having it folow a character..."
    bubble diagonal xflip yflip xalign 0.6 yalign 0.4 fang "...flip it both vertically and horizontally AND choose a custom position."
    bubble alex "Or you chould just let the code decide for you."

    alex "Demo has ended."
    # This ends the game.

    return
