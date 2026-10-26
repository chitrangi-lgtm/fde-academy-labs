# Nudges (open only if stuck)

1. Parse the Dockerfile line by line: the tag is after ':' in the image name (watch out for registry ports like host:5000/img).

2. The containers live at manifest['spec']['template']['spec']['containers']; check each one and collect codes in a set.
