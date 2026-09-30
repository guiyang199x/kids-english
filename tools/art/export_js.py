import json
import build1, build2, build3, build4, build5, build6, build7, build8, build9, build10, build11, build12, build13, build14, build15, build16, build17, build18, build19, build20, build21, build22, build23, build24, build25
from common import INK

def svg(vb, inner):
    return f'<svg viewBox="{vb}" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{inner}</svg>'

AV = "-82 -68 164 136"
art = {
 "apple": svg(AV, build1.APPLE), "ball": svg(AV, build1.ball()), "cat": svg(AV, build1.CAT),
 "dog": svg(AV, build1.DOG), "elephant": svg(AV, build1.ELEPHANT), "fish": svg(AV, build1.FISH),
}
for _L, _w, _fn in build5.ITEMS:
    art[_w] = svg(AV, _fn())
for _i, _w in enumerate(build6.NUMBERS):
    art[_w] = svg(AV, build6.number(_i + 1))
for _w, _fn in build6.SHAPES + build7.FRUITS + build7.FOOD + build8.BODY + build8.FAMILY + build8.WEATHER + build9.VEHICLES + build9.CLOTHES + build10.JOBS + build10.ROOM + build11.PREPOSITIONS + build12.ACTIONS + build13.WORDS + build18.TOYS + build21.SEA + build21.VEGETABLES + build21.BUGS + build22.ZOO + build25.ALL:
    art[_w] = svg(AV, _fn())
FV = "-76 -66 152 128"
for name, a, *_ in build3.CARDS:
    art[name] = svg(FV, a)
for name, main, dark, text, hb, rot in build2.COLORS:
    c = build2.crayon(main, dark, 112)
    art[name] = svg("-68 -68 136 136", f'<g transform="rotate(40) translate(0 71)">{c}</g>')

# scene with clickable labels
PL = [("sun",584,160,None),("cloud",262,60,(207,66)),("bird",330,170,(296,140)),("tree",62,282,(93,266)),
      ("house",560,268,(494,268)),("flower",88,378,(130,376)),("butterfly",300,414,(280,374)),
      ("dog",468,398,(514,392)),("ball",618,370,(618,403))]
labels = "".join(f'<g class="tag" data-word="{w}" tabindex="0" role="button" aria-label="{w}">{build4.pill(w,x,y,to)}</g>' for w,x,y,to in PL)
scene = (f'<defs><clipPath id="k-scene"><rect x="20" y="12" width="640" height="440" rx="24"/></clipPath></defs>'
   f'<g clip-path="url(#k-scene)">{"".join(build4.scene)}</g>'
   f'<rect x="20" y="12" width="640" height="440" rx="24" fill="none" stroke="{INK}" stroke-width="3"/>{labels}')
art["_scene"] = f'<svg viewBox="0 0 680 464" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A sunny day picture with labeled words">{scene}</svg>'
# Pip the panda (mascot). Keys start with "_" so they can't clash with a word.
for name, inner in build14.PIP.items():
    art[name] = svg(build14.PIP_VB, inner)
# more scenes, plus a small picture of each for its stop on the home map
for name, aria in (("kitchen", "A kitchen"), ("beach", "A day at the beach"), ("classroom", "A classroom"),
                   ("farm", "A farm"), ("park", "A park"), ("market", "A supermarket")):
    art["_scene-" + name] = build15.scene_svg(name, aria + " picture with labeled words")
art["_icon-kitchen"] = svg(AV, f'<g transform="translate(-10 -10) scale(1.8)">{build15.kettle(0, 30)}</g>')
art["_icon-beach"] = svg(AV, f'<g transform="translate(0 2) scale(1.3)">{build15.crab(0, 4)}</g>')
art["_icon-classroom"] = svg(AV, f'<g transform="translate(0 0) scale(1.3)">{build15.backpack(0, 40)}</g>')
art["_icon-farm"] = svg(AV, build15.cow(14, 54))
art["_icon-park"] = svg(AV, f'<g transform="scale(.95)">{build15.slide(-76, 64)}</g>')
art["_icon-market"] = svg(AV, build15.cart(4, 64))
# the world map and the inside of each island, plus where things are on them (window.WORLD, used by js/views/world.js and island.js)
isle_art, world = build16.export()
art.update(isle_art)
# Pip says: the room to drag the cat around in, and Pip with parts to touch
art.update(build17.export())
art.update(build19.export())  # the coloring page
art.update(build20.export())  # Pip acting out the moves
# Pip's house: the room inside (the house on the world map is drawn with the map, in build16)
home_art, world["home"] = build23.export()
art.update(build24.export())  # Halloween: the Ghost Ship, its words and the night scene for its story
art.update(home_art)
out = "window.ART = " + json.dumps(art, indent=0) + ";\n"
out += "window.WORLD = " + json.dumps(world) + ";\n"

import os; os.makedirs(os.path.join(os.path.dirname(__file__), "../../js")+"", exist_ok=True)
open(os.path.join(os.path.dirname(__file__), "../../js")+"/art.js","w").write(out)
print(len(out), sorted(art))
