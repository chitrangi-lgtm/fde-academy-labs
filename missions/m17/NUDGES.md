# Nudges (open only if stuck)

1. Parse the Dockerfile line by line: the tag is after ':' in the image name (watch out for registry ports like host:5000/img).

2. The containers live at manifest['spec']['template']['spec']['containers']; check each one and collect codes in a set.

## The approach, in plain English (open last)

1. Read the Dockerfile line by line, ignoring blanks and comments.
2. For each FROM line, look at the image name after the last slash and decide whether it has a real tag.
3. Collect the USER lines and judge the last one; no USER line at all also means root.
4. In the manifest, find the containers and check probes, limits, environment variables and the security context for each one.
5. Collect codes in a set and return them sorted.
