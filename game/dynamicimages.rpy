###############################
#
# INCLUDE THIS FILE FOR USEFUL & AUTOMATIC DEFINITIONS
#
###############################

init:
    transform blinkeyes(eyes1, eyes2):
        eyes1
        choice:
            3.5
        choice:
            2.5
        choice:
            1.5
        # This randomizes the time between blinking.
        eyes2
        .25
        repeat

    transform flapmouth(mouth1, mouth2):
        mouth1
        .2
        mouth2
        .2
        repeat

    transform flipimage:
        xzoom -1.0

    transform centerleft:
        xpos 0.25
        ypos 0.0
        xanchor 0.5
        yalign 1.0

    transform centerright:
        xpos 0.75
        ypos 0.0
        xanchor 0.5
        yalign 1.0


init -100 python:
    import os
    import sys
    import logging

    # absolute path to the game directory, which is formatted according
    # to the conventions of the local OS
    gamedir = os.path.normpath(config.gamedir)

    # required to make the above work with with RenPy:
    config.reject_backslash = False

    # setting the window on center
    # useful if game is launched in the window mode
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    sys.setdefaultencoding('utf-8')

    # Game may bug out on saving, in such case, comment should be removed
    # config.use_cpickle = False
    
    # enable logging via the 'logging' module
    try:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(name)-15s %(message)s')
        devlog = logging.getLogger(" ".join([config.name, config.version]))
        devlogfile = logging.FileHandler(os.path.join(gamedir, "devlog.txt"))
        devlogfile.setLevel(logging.DEBUG)
        devlog.addHandler(devlogfile)
        devlog.critical("\n--- launch game ---")
        fm = logging.Formatter('%(levelname)-8s %(name)-15s %(message)s')
        devlogfile.setFormatter(fm)
        del fm
        devlog.info("Game directory: %s" % gamedir)
    except:
        devlog.removeHandler(devlogfile)

    def pretty(d, indent=0):
        if isinstance(d, list):
            for value in d:
                pretty(value, indent)
        elif isinstance(d, dict):
            for key, value in d.items():
                devlog.info('\t' * indent + str(key))
                pretty(value, indent+1)
        else:
            devlog.info('\t' * (indent) + str(d))


init -50 python:
    import os
    import itertools

    eyesdef = ('e', 'ec', 'ed')
    mouthdef = ('m', 'mc', 'md', 'mdo')
    eyesauto = ('ed', 'ec')
    mouthauto = ('md', )

    basedict = {}
    pathlist = {}
    def DefineImages(imageFolder, flip=True, composite=True, prepend=None, overrideCharname=None, overrideLayerOrder=None, allcombinations=False):
        if composite:
            imglist = []

        excludeFirstXFolders = len(imageFolder.split('/'))
        if prepend is None:
            prepend = []
        if type(prepend) is unicode:
            prepend = [prepend,]

        for path in renpy.list_files():
            if path.startswith(imageFolder + "/"):
                path_list = path.split("/")
                if ' ' in path_list[-1]:
                    path_list = path_list[0:-1] + path_list[-1].split()
                path_list[-1] = os.path.splitext(path_list[-1])[0]
                path_list = tuple(prepend + path_list[excludeFirstXFolders:])

                renpy.image(path_list, path)
                if flip and not composite:
                    renpy.image(path_list + ("flip", ), im.Flip(path, horizontal=True))

                if composite:
                    # keep ordered list of all images, and also the corresponding paths
                    imglist.append(path_list)
                    pathlist[path_list] = path

        if composite:
            baselist = []
            for path_list in imglist:
                # get the list of sprite pose folders, which are detected if they contain:
                # 1. a base ('/base.')
                # 2. default eye ('/e default.' or '/ec default.')
                # 3. default mouth ('/m default.' or '/mc default.')
                basepath = path_list[:-1]
                if basepath in baselist:
                    continue
                if u'base' in path_list[-1]:
                    has_eyes = False
                    if basepath + (u'e', u'default') in pathlist:
                        has_eyes = True
                    if basepath + (u'ec', u'default') in pathlist:
                        has_eyes = True

                    has_mouth = False
                    if basepath + (u'm', u'default') in pathlist:
                        has_mouth = True
                    if basepath + (u'mc', u'default') in pathlist:
                        has_mouth = True

                    if has_eyes and has_mouth:
                        baselist.append(basepath)

            for basepath in baselist:
                charname = overrideCharname
                if charname is None:
                    charname = basepath[0]
                #devlog.info('==== ' + charname)

                # build the lists
                basedict[basepath] = {}
                basedict[basepath]['bases'] = []
                basedict[basepath]['parts'] = []
                basedict[basepath]['emotes'] = []
                basedict[basepath]['list'] = []
                basedict[basepath]['extraparts'] = {}
                basedict[basepath]['optionals'] = []
                baselen = len(basepath)
                for path_list in imglist:
                    if path_list[:baselen] == basepath:
                        if len(path_list) - baselen == 1:
                            basedict[basepath]['bases'].append(path_list[-1])
                        if len(path_list) - baselen == 2:
                            part = path_list[-2]
                            emote = path_list[-1]
                            if part == 'optional':
                                basedict[basepath]['optionals'].append(emote)
                            elif not part in eyesdef + mouthdef:
                                default_path_list = path_list[:-1] + (u'default',)
                                if default_path_list in imglist:
                                    #devlog.info(path_list)
                                    if not part in basedict[basepath]['extraparts']:
                                        basedict[basepath]['extraparts'][part] = []
                                    basedict[basepath]['extraparts'][part].append(emote)
                                    if not emote in basedict[basepath]['emotes']:
                                        basedict[basepath]['emotes'].append(emote)
                            else:
                                if not part in basedict[basepath]['parts']:
                                    basedict[basepath]['parts'].append(part)
                                if not emote in basedict[basepath]['emotes']:
                                    basedict[basepath]['emotes'].append(emote)
                        basedict[basepath]['list'].append(path_list)

                # special case for 'e' and 'ec': build blinking eyes into 'ed'
                # fill in the missing files as "default"
                if 'e' in basedict[basepath]['parts'] or 'ec' in basedict[basepath]['parts']:
                    for emote in basedict[basepath]['emotes']:
                        eyesopen = basepath + (u'e', emote)
                        eyesclose = basepath + (u'ec', emote)
                        if not eyesopen in basedict[basepath]['list']:
                            renpy.image(eyesopen, ' '.join(basepath+(u'e', u'default')))
                        if not basepath+(u'e', u'default') in basedict[basepath]['list']:
                            renpy.image(basepath+(u'e', u'default'), ' '.join(basepath+(u'ec', u'default')))
                        if not eyesclose in basedict[basepath]['list']:
                            renpy.image(eyesclose, ' '.join(basepath+(u'ec', u'default')))
                        if not basepath+(u'ec', u'default') in basedict[basepath]['list']:
                            renpy.image(basepath+(u'ec', u'default'), ' '.join(basepath+(u'e', u'default')))
                        renpy.image(basepath + (u'ed', emote), blinkeyes(' '.join(eyesopen), ' '.join(eyesclose)))
                        basedict[basepath]['list'].append(basepath + (u'ed', emote))
                    basedict[basepath]['parts'].append('ed')

                # special case for 'm' and 'mc': build flapping mouth into 'md'
                # fill in the missing files as "default"
                if 'm' in basedict[basepath]['parts'] or 'mc' in basedict[basepath]['parts']:
                    for emote in basedict[basepath]['emotes']:
                        mouthopen = basepath + (u'm', emote)
                        mouthclose = basepath + (u'mc', emote)
                        if not mouthopen in basedict[basepath]['list']:
                            renpy.image(mouthopen, ' '.join(basepath+(u'm', u'default')))
                        if not basepath+(u'm', u'default') in basedict[basepath]['list']:
                            renpy.image(basepath+(u'm', u'default'), ' '.join(basepath+(u'mc', u'default')))
                        if not mouthclose in basedict[basepath]['list']:
                            renpy.image(mouthclose, ' '.join(basepath+(u'mc', u'default')))
                        if not basepath+(u'mc', u'default') in basedict[basepath]['list']:
                            renpy.image(basepath+(u'mc', u'default'), ' '.join(basepath+(u'm', u'default')))
                        renpy.image(basepath + (u'md', emote), FlapMouth(' '.join(mouthclose), ' '.join(mouthopen), cha=charname))
                        renpy.image(basepath + (u'mdo', emote), FlapMouth(' '.join(mouthopen), ' '.join(mouthclose), cha=charname))
                        basedict[basepath]['list'].append(basepath + (u'md', emote))
                        basedict[basepath]['list'].append(basepath + (u'mdo', emote))
                    basedict[basepath]['parts'].append('md')
                    basedict[basepath]['parts'].append('mdo')

                # go through the extras and fill in the missing files as "default"
                for ek in basedict[basepath]['extraparts']:
                    for emote in basedict[basepath]['emotes']:
                        ev = basepath + (ek, emote)
                        if not ev in basedict[basepath]['list']:
                            renpy.image(ev, ' '.join(basepath+(ek, u'default')))
                        basedict[basepath]['list'].append(basepath + (ek, emote))

                # determine the layer order
                layerorder = overrideLayerOrder
                if layerorder is None:
                    layerorder = ['base', 'eyes', 'mouth']
                    layerorder += sorted(basedict[basepath]['extraparts'].keys())
                    layerorder += basedict[basepath]['optionals']
                basedict[basepath]['layerorder'] = layerorder

                # create a list of all possible combinations of the extra parts
                extraperms = []
                eks = sorted(basedict[basepath]['extraparts'].keys())
                def addperms(ek=0, tempperm=[]):
                    if ek >= len(eks):
                        return
                    for emote in basedict[basepath]['emotes']:
                        tempperm2 = list(tempperm)
                        tempperm2.append((eks[ek], emote))
                        if ek < len(eks)-1:
                            addperms(ek+1, tempperm2)
                        else:
                            extraperms.append(tuple(tempperm2))
                addperms()
                if extraperms == []:
                    extraperms = [()]

                # build the livecomposites from bases and emotes
                for base in basedict[basepath]['bases']:
                    size = renpy.image_size(im.Image(pathlist[basepath+(base,)]))
                    basespr = BaseCSprite(' '.join(basepath+(base,)), size)
                    if allcombinations:
                        for eyes in basedict[basepath]['list']:
                            #if not eyes[-2] in (u'e', u'ec', u'ed'):
                            if not eyes[-2] in eyesauto:
                                continue
                            for mouth in basedict[basepath]['list']:
                                #if not mouth[-2] in (u'm', u'mc', u'md', u'mdo'):
                                if not mouth[-2] in mouthauto:
                                    continue
                                for ext in extraperms:
                                    for o in range(len(basedict[basepath]['optionals'])+1):
                                        for ops in itertools.combinations(basedict[basepath]['optionals'], o):
                                            layers = []
                                            pathtuple = list(basepath)
                                            for layer in layerorder:
                                                if layer == 'base':
                                                    layers.append(' '.join(basepath+(base,)))
                                                    pathtuple.append(base)
                                                elif layer == 'eyes':
                                                    layers.append(' '.join(eyes))
                                                    pathtuple += eyes[-2:]
                                                elif layer == 'mouth':
                                                    layers.append(' '.join(mouth))
                                                    pathtuple += mouth[-2:]
                                                elif layer in ops:
                                                    layers.append(' '.join(basepath + (u'optional', layer)))
                                                    pathtuple.append(layer)
                                                else:
                                                    for ex in ext:
                                                        if layer == ex[0]:
                                                            layers.append(' '.join(basepath + ex))
                                                            pathtuple += ex

                                            #devlog.info(' '.join(pathtuple))
                                            renpy.image(tuple(pathtuple), basespr(layers))
                                            if flip:
                                                renpy.image(tuple(pathtuple)+(u'flip',), flipimage(' '.join(pathtuple)))
                    else:
                        for emote in basedict[basepath]['emotes']:
                            eyes = basepath+(u'ed', emote)
                            mouth = basepath+(u'md', emote)
                            ext = []
                            for ex in sorted(basedict[basepath]['extraparts'].keys()):
                                ext.append((ex, emote))
                            for o in range(len(basedict[basepath]['optionals'])+1):
                                for ops in itertools.combinations(basedict[basepath]['optionals'], o):
                                    layers = []
                                    pathtuple = list(basepath)
                                    for layer in layerorder:
                                        if layer == 'base':
                                            layers.append(' '.join(basepath+(base,)))
                                            pathtuple.append(base)
                                        elif layer == 'eyes':
                                            layers.append(' '.join(eyes))
                                            pathtuple += eyes[-2:]
                                        elif layer == 'mouth':
                                            layers.append(' '.join(mouth))
                                            pathtuple += mouth[-2:]
                                        elif layer in ops:
                                            layers.append(' '.join(basepath + (u'optional', layer)))
                                            pathtuple.append(layer)
                                        else:
                                            for ex in ext:
                                                if layer == ex[0]:
                                                    layers.append(' '.join(basepath + ex))
                                                    pathtuple += ex

                                    #devlog.info(' '.join(pathtuple))
                                    renpy.image(tuple(pathtuple), basespr(layers))
                                    if flip:
                                        renpy.image(tuple(pathtuple)+(u'flip',), flipimage(' '.join(pathtuple)))
                    # shortcuts to emotes - default base can omit base
                    for emote in basedict[basepath]['emotes']:
                        if base == u'base':
                            newemote = basepath + (emote,)
                        else:
                            newemote = basepath + (base, emote)
                        oldemote = basepath + (base,) + (u'ed', emote) + (u'md', emote)
                        for ek in basedict[basepath]['extraparts']:
                            oldemote += (ek, emote)
                        MapEmote(' '.join(newemote), ' '.join(oldemote))

            #pretty(basedict)

    def MapEmote(newname, oldname, addOptionals=True, flip=True):
        newpath = tuple(newname.split())
        oldpath = oldname.split()

        basepath = None
        for basepath2 in basedict:
            if basepath2 == tuple(oldpath[:len(basepath2)]):
                basepath = basepath2
                break
        if basepath is None:
            return None

        bases = None
        eyes = ('ed', 'default')
        mouth = ('md', 'default')
        extraparts = {}
        for ek in basedict[basepath]['extraparts']:
            extraparts[ek] = (ek, 'default')
        optionals = []
        i = len(basepath)
        while i < len(oldpath):
            if oldpath[i] in basedict[basepath]['bases']:
                bases = [oldpath[i],]
            elif oldpath[i] in eyesdef:
                eyes = oldpath[i:i+2]
                i += 1
            elif oldpath[i] in mouthdef:
                mouth = oldpath[i:i+2]
                i += 1
            elif oldpath[i] in basedict[basepath]['extraparts']:
                extraparts[oldpath[i]] = oldpath[i:i+2]
                i += 1
            elif oldpath[i] in basedict[basepath]['optionals']:
                optionals.append(oldpath[i])
            i += 1
        optionals = tuple(sorted(optionals))

        autobases = False
        if bases is None:
            autobases = True
            bases = basedict[basepath]['bases']

        for base in bases:
            size = renpy.image_size(im.Image(pathlist[basepath+(base,)]))
            basespr = BaseCSprite(' '.join(basepath+(base,)), size)

            newpath2 = newpath
            if autobases and not base == 'base':
                 newpath2 += (base,)

            if addOptionals:
                for o in range(len(basedict[basepath]['optionals'])+1):
                    for ops in itertools.combinations(basedict[basepath]['optionals'], o):
                        layers = []
                        pathtuple = list(basepath)
                        for layer in basedict[basepath]['layerorder']:
                            if layer == 'base':
                                layers.append(' '.join(basepath+(base,)))
                                pathtuple.append(base)
                            elif layer == 'eyes':
                                layers.append(' '.join(basepath+tuple(eyes)))
                                pathtuple += eyes
                            elif layer == 'mouth':
                                layers.append(' '.join(basepath+tuple(mouth)))
                                pathtuple += mouth
                            elif layer in ops or layer in optionals:
                                layers.append(' '.join(basepath + (u'optional', layer)))
                                pathtuple.append(layer)
                            elif layer in extraparts:
                                layers.append(' '.join(basepath + tuple(extraparts[layer])))
                                pathtuple += extraparts[layer]

                        if not renpy.has_image(tuple(pathtuple), exact=True):
                            renpy.image(tuple(pathtuple), basespr(layers))
                            if flip:
                                renpy.image(tuple(pathtuple)+(u'flip',), flipimage(' '.join(pathtuple)))
                        renpy.image(newpath2+ops, ' '.join(pathtuple))
                        if flip:
                            renpy.image(newpath2+ops+(u'flip',), flipimage(' '.join(pathtuple)))
            else:
                layers = []
                pathtuple = list(basepath)
                for layer in basedict[basepath]['layerorder']:
                    if layer == 'base':
                        layers.append(' '.join(basepath+(base,)))
                        pathtuple.append(base)
                    elif layer == 'eyes':
                        layers.append(' '.join(basepath+tuple(eyes)))
                        pathtuple += eyes
                    elif layer == 'mouth':
                        layers.append(' '.join(basepath+tuple(mouth)))
                        pathtuple += mouth
                    elif layer in optionals:
                        layers.append(' '.join(basepath + (u'optional', layer)))
                        pathtuple.append(layer)
                    elif layer in extraparts:
                        layers.append(' '.join(basepath + tuple(extraparts[layer])))
                        pathtuple += extraparts[layer]

                if not renpy.has_image(tuple(pathtuple), exact=True):
                    renpy.image(tuple(pathtuple), basespr(layers))
                    if flip:
                        renpy.image(tuple(pathtuple)+(u'flip',), flipimage(' '.join(pathtuple)))
                renpy.image(newpath2, ' '.join(pathtuple))
                if flip:
                    renpy.image(newpath2+(u'flip',), flipimage(' '.join(pathtuple)))

    # This is set to the name of the character that is speaking, or
    # None if no character is currently speaking.
    speaking = None

    # This returns speaking if the character is speaking, and done if the
    # character is not.
    def while_speaking(name, speak_d, done_d, st, at):
        if (renpy.music.is_playing('voice') or not config.has_voice) and speaking == name:
            return speak_d, .1
        else:
            return done_d, None

    # Curried form of the above.
    curried_while_speaking = renpy.curry(while_speaking)

    # Displays speaking when the named character is speaking, and done otherwise.
    def WhileSpeaking(name, speaking_d, done_d=Null()):
        return DynamicDisplayable(curried_while_speaking(name, speaking_d, done_d))

    # This callback maintains the speaking variable.
    def speaker_callback(name, event, **kwargs):
        global speaking

        if config.has_voice:
            speaking = name
        else:
            if event == "show":
                speaking = name
            elif event == "slow_done":
                speaking = None
            elif event == "end":
                speaking = None

    # Curried form of the same.
    speaker = renpy.curry(speaker_callback)

    def FlapMouth(mouth1, mouth2, cha=None):
        if cha is None:
            cha = mouth1.split()[0]
        mouth = flapmouth(mouth1, mouth2)
        return WhileSpeaking(cha, mouth, mouth1)

    def BlinkEyes(eyes1, eyes2):
        return blinkeyes(eyes1, eyes2)

    def CSprite(base, size, *layers):
        if size is None or layers is None or len(layers) == 0:
            return base
        argslayers = []
        for l in layers:
            argslayers.append((0, 0))
            argslayers.append(l)
        return LiveComposite(
                size,
                *argslayers
            )

    class BaseCSprite:
        def __init__(self, basesprite, size):
            self.basesprite = basesprite
            self.size = size

        def __call__(self, layers=[]):
            return CSprite(self.basesprite, self.size, *layers)
