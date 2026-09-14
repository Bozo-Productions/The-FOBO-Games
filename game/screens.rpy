################################################################################
## Initialization
################################################################################

init offset = -1


################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)



################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on
    ## the phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-
## game menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"
            style "quick_menu"

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            #textbutton _("Q.Save") action QuickSave()
            #textbutton _("Q.Load") action QuickLoad()
            textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_menu is hbox
style quick_button is default
style quick_button_text is button_text

style quick_menu:
    xalign 0.5
    yalign 1.0

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.

screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            #textbutton _("Save") action ShowMenu("save")

        #textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

transform sun:
    xalign 0.05
    yalign 0.05
    zoom 1.4

    linear 60 rotate 360
    rotate 0
    repeat

transform dragon:
    xalign 0.8
    #yalign 0.5

    ease 1.3  yalign 0.45
    ease 1.3 yalign 0.55
    repeat

default start_anim = False

transform start_anim1:
    xalign -1.62
    ycenter 0.48
    linear 0.6 xcenter 0.192
    linear 0.1 yoffset 10.0
    linear 0.1 yoffset -10.0
    linear 0.1 yoffset 10.0
    linear 0.1 yoffset -10.0
    linear 0.1 yoffset 10.0
    linear 0.1 yoffset -10.0

transform start_anim2:
    xalign 2.62
    ycenter 0.48
    linear 0.6 xcenter 0.808
    linear 0.1 yoffset -10.0
    linear 0.1 yoffset 10.0
    linear 0.1 yoffset -10.0
    linear 0.1 yoffset 10.0
    linear 0.1 yoffset -10.0
    linear 0.1 yoffset 10.0

screen main_menu():
    tag menu

    timer 0.1 action Hide("select_screen")

    add color("#9d7e8d")

    add "images/main/sun.png" at sun
    add "images/main/dragon.png" at dragon
    add "images/main/title.png":
        xalign 0.05
        yalign 0.26
    add "images/main/town.png":
        xalign 1.0
        yalign 1.0

    add "images/main/bar.png":
        xalign 0.0
        yalign 1.0

    
    imagebutton auto "images/main/buttons/start_%s.png":
        #action ShowMenu("select_screen")
        action SetVariable("start_anim", True)
        xalign 0.02
        yalign 0.75

    imagebutton auto "images/main/buttons/help_%s.png":
        #action ShowMenu("preferences")
        action Notify("Help")
        xalign 0.02
        yalign 0.865

    imagebutton auto "images/main/buttons/settings_%s.png":
        action ShowMenu("preferences")
        xalign 0.02
        yalign 0.985

    imagebutton auto "images/main/buttons/quit_%s.png":
        action Quit(confirm=not main_menu)
        xalign 0.35
        yalign 0.985

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            #text "[config.name!t]":
            #    style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    if start_anim:
        add "images/main/door.png" at start_anim1
        add "images/main/door2.png" at start_anim2
        timer 1.2 action ShowMenu("select_screen")
            



default current_character = "none"

default strgth_display = 1
default spd_display = 1
default int_display = 1
default surv_display = 1

default selected_characters = []


transform hide_anim1:
    xcenter 0.192
    ycenter 0.48
    0.3
    linear 0.6 xalign -1.62

transform hide_anim2:
    xcenter 0.808
    ycenter 0.48
    0.3
    linear 0.6 xalign 2.62


screen select_screen():
    #tag menu

    timer 0.1 action Hide("main_menu")
    timer 0.1 action SetVariable("start_anim", False)

    add "images/select/frame2.png":
        xalign 1.003
        yalign 0.5
    add "images/select/frame.png":
        xalign 0.0
        yalign 0.5

    
    viewport:
        mousewheel True
        draggable True
        area (540, 171, 1300, 736)

        vbox:
            
            hbox:
                imagebutton auto("images/select/buttons/uber_%s.png"):
                    action Notify("Uber")
                    hovered SetVariable("current_character", "uber")
                
                #imagebutton auto("images/select/buttons/stick_%s.png"):
                #    action Notify("Stick")
                #    hovered SetVariable("current_character", "stick")

                imagebutton auto("images/select/buttons/dna_%s.png"):
                    action Notify("Dina")
                    hovered SetVariable("current_character", "dna")

                imagebutton auto("images/select/buttons/elf_%s.png"):
                    action Notify("Elf")
                    hovered SetVariable("current_character", "elf")

                imagebutton auto("images/select/buttons/lispura_%s.png"):
                    action Notify("Lispura")
                    hovered SetVariable("current_character", "lispura")

            hbox:
                #imagebutton auto("images/select/buttons/cyn_%s.png"):
                #    action Notify("Cyn")
                #    hovered SetVariable("current_character", "cyn")
                
                imagebutton auto("images/select/buttons/tino_%s.png"):
                    action Notify("Tino")
                    hovered SetVariable("current_character", "tino")

                imagebutton auto("images/select/buttons/draco_%s.png"):
                    action Notify("Draco")
                    hovered SetVariable("current_character", "draco")

                imagebutton auto("images/select/buttons/marsh_%s.png"):
                    action Notify("Marsh")
                    hovered SetVariable("current_character", "marsh")

                imagebutton auto("images/select/buttons/layton_%s.png"):
                    action Notify("Layton")
                    hovered SetVariable("current_character", "layton")

            hbox:
                imagebutton auto("images/select/buttons/jely_%s.png"):
                    action Notify("Jely")
                    hovered SetVariable("current_character", "jely")

                imagebutton auto("images/select/buttons/primordi_%s.png"):
                    action Notify("Primordi")
                    hovered SetVariable("current_character", "primordi")

                imagebutton auto("images/select/buttons/Forgot_%s.png"):
                    action Notify("Forgot")
                    hovered SetVariable("current_character", "forgot")

                imagebutton auto("images/select/buttons/Spring_%s.png"):
                    action Notify("Spring")
                    hovered SetVariable("current_character", "spring")

            hbox:
                imagebutton auto("images/select/buttons/erica_%s.png"):
                    action Notify("Erica")
                    hovered SetVariable("current_character", "erica")

                imagebutton auto("images/select/buttons/star_%s.png"):
                    action Notify("Star")
                    hovered SetVariable("current_character", "star")

                imagebutton auto("images/select/buttons/pg_%s.png"):
                    action Notify("PG")
                    hovered SetVariable("current_character", "pg")

                imagebutton auto("images/select/buttons/leo_%s.png"):
                    action Notify("Leo")
                    hovered SetVariable("current_character", "leo")

            hbox:
                imagebutton auto("images/select/buttons/lummi_%s.png"):
                    action Notify("Lummi")
                    hovered SetVariable("current_character", "lummi")

                imagebutton auto("images/select/buttons/clover_%s.png"):
                    action Notify("Clover")
                    hovered SetVariable("current_character", "clover")

                imagebutton auto("images/select/buttons/med_%s.png"):
                    action Notify("Med")
                    hovered SetVariable("current_character", "med")

                imagebutton auto("images/select/buttons/teddy_%s.png"):
                    action Notify("Teddy")
                    hovered SetVariable("current_character", "teddy")

            hbox:
                imagebutton auto("images/select/buttons/bec_%s.png"):
                    action Notify("Bec")
                    hovered SetVariable("current_character", "bec")

                imagebutton auto("images/select/buttons/laney_%s.png"):
                    action Notify("Laney")
                    hovered SetVariable("current_character", "laney")

                imagebutton auto("images/select/buttons/veli_%s.png"):
                    action Notify("Veli")
                    hovered SetVariable("current_character", "veli")

                imagebutton auto("images/select/buttons/slayer_%s.png"):
                    action Notify("Slayer")
                    hovered SetVariable("current_character", "slayer")

            hbox:
                imagebutton auto("images/select/buttons/zekky_%s.png"):
                    action Notify("Zekky")
                    hovered SetVariable("current_character", "zekky")

                imagebutton auto("images/select/buttons/dragon_%s.png"):
                    action Notify("Dragon")
                    hovered SetVariable("current_character", "dragon")

                imagebutton auto("images/select/buttons/pey_%s.png"):
                    action Notify("Pey")
                    hovered SetVariable("current_character", "pey")



    


    if current_character == "none":
        add "images/select/portraits/none.png":
            xalign 0.0508
            yalign 0.2

    elif current_character == "uber":
        add "images/select/portraits/uber.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Uber"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 1
        $ spd_display = 6
        $ int_display = 6
        $ surv_display = 7
        add Text("{size=17}Born Leader: Uber's natural charisma increases his chance of successfully forming a team. While in a team, he boosts everyone's damage. When Uber inevitebly decices to betray his team, his backstabs will deal 30% more damage."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "stick":
        add "images/select/portraits/stick.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Stick"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 5
        $ spd_display = 5
        $ int_display = 5
        $ surv_display = 5
        add Text("{size=17}Admin Abuse: Stick channels his bloodlust, offering it up to an ancient god to transport him to anywhere on the map. This ability starts with one use, Stick gains another use with each kill."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "dna":
        add "images/select/portraits/dna.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}DNA-D2"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 5
        $ spd_display = 5
        $ int_display = 5
        $ surv_display = 5
        add Text("{size=17}Identity Retrieve: DiNA will not go down easy. Upon death, DiNA will revive once, copying the stats and ability of whoever killed her. Ability only activates if she is killed by another player. \"I'm you now.\""):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "elf":
        add "images/select/portraits/elf.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Elf"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 6
        $ spd_display = 3
        $ int_display = 5
        $ surv_display = 6
        add Text("{size=17}True Architect: Elf is passionate about her work, and puts a lot of thought into it. Any trap built by Elf has a higher chance of succeding. It would be dumb to chase her anywhere..."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "lispura":
        add "images/select/portraits/lispura.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Lispura"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 6
        $ int_display = 8
        $ surv_display = 8
        add Text("{size=17}Thick Skin: Lispura doesn't let anything bother him, this has caused him to care very little about anything, even damage. Lispura starts off with more health than average, and takes reduced damage from all sources."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "cyn":
        add "images/select/portraits/cyn.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Cyn"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 1
        $ spd_display = 1
        $ int_display = 1
        $ surv_display = 1
        add Text("{size=17}Dragon Tamer: Cyn starts the game with a baby dragon. This dragon can be leveled up with food and kills. Each level increases its damage and health, maxing out at level 5. The dragon will mimic Cyn's abilities, but once it's killed, its gone forever..."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "draco":
        add "images/select/portraits/draco.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Draco"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 4
        $ spd_display = 8
        $ int_display = 3
        $ surv_display = 5
        add Text("{size=17}Stern Glance: Draco is naturally intimidating, even a glance can petrify others. Draco has a higher chance of intimidating someone out of a fight, if sucessful, the opponents speed will be reduced for a turn."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "marsh":
        add "images/select/portraits/marsh.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Marsh"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 3
        $ spd_display = 4
        $ int_display = 7
        $ surv_display = 6
        add Text("{size=17}Sharp Shooter: Marsh is naturally adept with a bow, carrying one with them everywhere. Marsh starts the game with a bow and 2 arrows. Increases their chance of finding ranged weapons and ammo."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "layton":
        add "images/select/portraits/layton.png":
            xalign 0.0508
            yalign 0.15
        add Text("{size=60}{b}{color=#ffaa5e}Layton"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 6
        $ spd_display = 2
        $ int_display = 5
        $ surv_display = 7
        add Text("{size=17}True Magician: Layton has the inate ability to channel magic. Each round he survives he builds more mana. During a fight he can cast a spell, using all his mana. Depending on the ammount of mana, the spell will be different."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "jely":
        add "images/select/portraits/jely.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Jely"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 3
        $ int_display = 8
        $ surv_display = 7
        add Text("{size=17}Pure Pacafist: Jely dislikes violence, because of this, he will try his best to avoid it. Jely has an increased chance of talking his way out of a fight. If Jely sucessfully ends the fight, he gains 30% overhealth for 2 rounds, stackable."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "primordi":
        add "images/select/portraits/primordi.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Primordi"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 5
        $ int_display = 7
        $ surv_display = 6
        add Text("{size=17}Fleet Foot: Primordi is naturally quick, and always prepared to go faster. Primordi gains a permenant speed buff with each kill, consuming a vegetable will give her a temporary speed buff, and normal speed buffs are twice as effective. Don't try to outrun her..."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "forgot":
        add "images/select/portraits/forgot.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Forgot"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 7
        $ spd_display = 3
        $ int_display = 4
        $ surv_display = 6
        add Text("{size=17}Always Hungry: Forgot is a man who is naturally hungry, due to this fact however, his body processes food at a slower rate to make it last longer. Forgot looses hunger slower than anyone else, and has an increased chance of finding food."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "spring":
        add "images/select/portraits/spring.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Spring"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 1
        $ spd_display = 10
        $ int_display = 4
        $ surv_display = 1
        add Text("{size=17}Dumb Luck: Spring is an idiot, but even idiots get lucky. The first killing blow Spring recieves will be completely negated. The fight will end, and Springs speed will be massively buffed for that round before dropping to a 20% permenant boost. This ability only activates once."):
            xsize 248
            xalign 0.054
            yalign 0.75
        textbutton("Alt"):
            action SetVariable("current_character", "spring2")
            xcenter 0.11
            ycenter 0.813

    elif current_character == "spring2":
        add "images/select/portraits/spring2.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Spring"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 1
        $ spd_display = 10
        $ int_display = 4
        $ surv_display = 1
        add Text("{size=17}Dumb Luck: Spring is an idiot, but even idiots get lucky. The first killing blow Spring recieves will be completely negated. The fight will end, and Springs speed will be massively buffed for that round before dropping to a 20% permenant boost. This ability only activates once."):
            xsize 248
            xalign 0.054
            yalign 0.75
        textbutton("Alt"):
            action SetVariable("current_character", "spring")
            xcenter 0.11
            ycenter 0.813

    elif current_character == "erica":
        add "images/select/portraits/erica.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Erica"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 3
        $ spd_display = 4
        $ int_display = 7
        $ surv_display = 6
        add Text("{size=17}Creator: Erica channels energy flowing through the air around her to create items from nothing. Erica can generate a random item once per round. This item can range from a resource to the deadliest of weapons, just not food."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "star":
        add "images/select/portraits/star.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Star"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 5
        $ spd_display = 5
        $ int_display = 5
        $ surv_display = 5
        add Text("{size=17}Annoying Pest: Star likes to annoy others, giving him an increased chance to start a fight with someone. If he does start a fight, he gets a 50% speed boost on escape. Pretty much, he'll piss you off, then run away. \"I must follow my main on there!\""):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "pg":
        add "images/select/portraits/pg.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}PG"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 7
        $ int_display = 7
        $ surv_display = 4
        add Text("{size=17}Second Best: There's nothing that PG isn't good at! There's also nothing he's the best at. PG can copy any other players base stats, but they will be slightly worse than whoever he copies."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "leo":
        add "images/select/portraits/leo.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Leo"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 3
        $ spd_display = 9
        $ int_display = 5
        $ surv_display = 3
        add Text("{size=17}In Fire: Leo loves playing with the flames. Leo will light himself on fire, dealing 1 damage to himself per round until extinguished, but it will increase his output damage by 2, and ignite anyone he attacks."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "lummi":
        add "images/select/portraits/lummi.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Lummi"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 3
        $ spd_display = 5
        $ int_display = 5
        $ surv_display = 7
        add Text("{size=17}Pro Cosplayer: \"A wild Lummo has appeared!\" Lummi loves to dress as her favorite characters, in this case, her friends! Lummi can dress as any other player, copying their ability. The effect ends when she cancels it, or drops below 50% max health."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "clover":
        add "images/select/portraits/clover.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Clover"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 6
        $ spd_display = 4
        $ int_display = 5
        $ surv_display = 5
        add Text("{size=17}Sneak Attack!:Clover is a gremlin who loves chaos. If Clover starts a fight sucessfully, they will deal a light attack before the other player can react. In normal combat, Clover has a small chance to deal double damage on an attack."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "med":
        add "images/select/portraits/med.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Medabic"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 7
        $ int_display = 7
        $ surv_display = 4
        add Text("{size=17}Overwhelming Aura: Med is too cool, especially with those shades. Med has a random chance of halving the damage of a direct attack, and any even smaller chance to negate it completely. \"Those... eyes...\""):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "teddy":
        add "images/select/portraits/teddy.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Teddy"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 2
        $ spd_display = 4
        $ int_display = 7
        $ surv_display = 7
        add Text("{size=17}Always Okay: Nothing can get Teddy down, they're always okay! Negative status effects don't work on Teddy, but neither do positive ones... Maybe always being just \"okay\" isn't the best thing..."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "bec":
        add "images/select/portraits/bec.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Becca"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 4
        $ spd_display = 2
        $ int_display = 5
        $ surv_display = 3
        add Text("{size=17}Sneak 1000: Becca is very sneaky, and able to outmanuver almost anyone. Becca has an increased chance of evading other players, and can go undeteced in group scenarios."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "laney":
        add "images/select/portraits/laney.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Laney"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 4
        $ spd_display = 4
        $ int_display = 6
        $ surv_display = 6
        add Text("{size=17}Laggiest Warrior: Sadly, Laney is very laggy, but in this scenario, she can use it to her advantage. Laney has an increased chance of \"lagging\" out of the line of attacks, increasing her dodge chance."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "veli":
        add "images/select/portraits/veli.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Veli"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 6
        $ spd_display = 6
        $ int_display = 3
        $ surv_display = 5
        add Text("{size=17}Unyielding Warrior: Veli likes to protect their friends, carrying a shield with them wherever they go. Veli starts the game with a shield, has a higher defense stat, and an increased chance of finding defense based items."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "slayer":
        add "images/select/portraits/slayer.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Slayer"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 8
        $ spd_display = 3
        $ int_display = 5
        $ surv_display = 4
        add Text("{size=17}Killer Instinct: Slayer is a man you don't want to mess with. Slayer starts the game with a dull blade, worn down from previous battles. Slayer will grow stronger each round he goes without killing, stats reverting back to normal when he finally does. Has an increased chance of finding melee weapons."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "zekky":
        add "images/select/portraits/zekky.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Zekky"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 3
        $ spd_display = 5
        $ int_display = 8
        $ surv_display = 4
        add Text("{size=17}Pro Athlete: Zekky takes care to stay fast and fit. Zekky drops into a running stance, for the next 3 rounds, his speed is buffed by 30%, his attack is buffed by 20% and his survivability is buffed by 30%."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "dragon":
        add "images/select/portraits/dragon.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Dragon"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 5
        $ spd_display = 5
        $ int_display = 4
        $ surv_display = 6
        add Text("{size=17}Venomous Sting: Dragon's much more vicious than he lets on. During a fight, Dragon can sting the opponent with his tail, poisoning them till they find an antidote. This sting has a 3 round cooldown, and buffs his speed by 20% for the same amount of time."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "pey":
        add "images/select/portraits/pey.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Pey"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 4
        $ spd_display = 3
        $ int_display = 8
        $ surv_display = 5
        add Text("{size=17}Ancient Magic: Pey has spent years studying magical runes to increas their abilities. Pey can write these runes on their body to buff any given stat by 15% until it is switched to another rune. Stacks with other buffs."):
            xsize 248
            xalign 0.054
            yalign 0.75

    elif current_character == "tino":
        add "images/select/portraits/tino.png":
            xalign 0.0508
            yalign 0.2
        add Text("{size=60}{b}{color=#ffaa5e}Tino"):
            xcenter 0.112
            yalign 0.42
        $ strgth_display = 4
        $ spd_display = 2
        $ int_display = 8
        $ surv_display = 6
        add Text("{size=17}Reallocate: Tino is very adept and capable of adapting to any situation. Tino is able to reallocate his own base stats, moving points from one stat to another mid game. All stats still cap at 10. Cannot be used during a fight."):
            xsize 248
            xalign 0.054
            yalign 0.75


    add Text("{size=25}Strgth"):
        xalign 0.05
        yalign 0.475
    add DynamicImage("images/select/stats/strength/"  + str(strgth_display) + ".png"):
        xalign 0.0991
        yalign 0.477

    add Text("{size=25}Spd"):
        xalign 0.05
        yalign 0.505
    add DynamicImage("images/select/stats/speed/"  + str(spd_display) + ".png"):
        xalign 0.0991
        yalign 0.507

    add Text("{size=25}Int"):
        xalign 0.05
        yalign 0.535
    add DynamicImage("images/select/stats/intelligence/"  + str(int_display) + ".png"):
        xalign 0.0991
        yalign 0.537

    add Text("{size=25}Surv"):
        xalign 0.05
        yalign 0.565
    add DynamicImage("images/select/stats/survival/"  + str(surv_display) + ".png"):
        xalign 0.0991
        yalign 0.567




    textbutton "return" action Return():
        xalign 0.03
        yalign 0.97

    add "images/main/door.png" at hide_anim1
    add "images/main/door2.png" at hide_anim2



style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of
            ## the buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()
                    key "save_page_prev" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()
                    key "save_page_next" action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5
    xalign 0.5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better
## suit themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can
                ## be added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0, spacing=gui.history_spacing):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character,
                        ## if set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")

    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide, B/Right Button")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly
        ## if config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed
## at once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using
## speech bubbles. The bubble screen takes the same parameters as the say
## screen, must create a displayable with the id of "what", and can create
## displayables with the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

        default ctc = None
        showif ctc:
            add ctc

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style "quick_menu"
            style_prefix "quick"

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style game_menu_viewport:
    variant "small"
    xsize 1305

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
