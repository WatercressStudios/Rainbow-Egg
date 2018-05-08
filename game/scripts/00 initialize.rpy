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
    show fang surprised flip

    # These display lines of dialogue.

    fang "Hello, world, and hello again."

    hide fang
    #show alex pose1 shinyarm ed scared md scared brow scared
    show alex pose1 scared
    #show alex scared

    alex "You've created a new Ren'Py game."
    hide alex

    show fang happy

    fang "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
