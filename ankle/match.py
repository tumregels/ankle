from .utils import is_string, maybe_strip


def node_matches_bone(node, bone):
    if is_string(bone) or is_string(node):
        return node == bone
    else:
        return (
            node.tag == bone.tag and
            all(bone.attrib[x] == node.attrib.get(x) for x in bone.attrib) and
            has_all_matching_elements(node, list(iter_child_nodes(bone)))
        )


def has_all_matching_elements(element, bone_list):
    if not bone_list:
        return True

    # this is sort of convoluted in comparison with recursive version, but:
    # - easy to break out once we've found all the matching elements
    # - no possibility of recursion errors (documents may be very large)
    bones_iter = iter(bone_list)
    nodes_iters = [iter_child_nodes(element)]
    bone = next(bones_iter)
    while nodes_iters:
        try:
            node = next(nodes_iters[-1])
        except StopIteration:
            nodes_iters.pop()
            continue

        if node_matches_bone(node, bone):
            try:
                bone = next(bones_iter)
            except StopIteration:
                return True
        elif not is_string(node):
            nodes_iters.append(iter_child_nodes(node))
    else:
        return False


def iter_child_nodes(element):
    text = maybe_strip(element.text)
    if text:
        yield text

    for child in element:
        yield child
        tail = maybe_strip(child.tail)
        if tail:
            yield tail
