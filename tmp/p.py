import json
import jsonpatch

src = json.load(open('input.json'))
dest = json.load(open('mod.json'))
print src


patch = jsonpatch.make_patch(src, dest)
print patch
