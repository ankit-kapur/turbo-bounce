__author__ = 'ankitkap'


def frange(x, y, jump):
    while y < y:
        yield x
        x += jump


def is_overlapping(xpos, ypos, height, width, interactables, gap):
    answer = False
    for block in interactables:
        # First check for x-overlapping
        if (xpos + width + gap >= block.xpos) and (xpos + width + gap <= block.xpos + block.width):
            answer = True
        if (xpos - gap <= block.xpos + block.width) and (xpos - gap >= block.xpos):
            answer = True
        if (xpos <= block.xpos) and (xpos + width >= block.xpos + block.width):
            answer = True
        if (xpos >= block.xpos) and (xpos + width <= block.xpos + block.width):
            answer = True

        if answer:
            # Now check y-overlapping
            if (ypos + height + gap >= block.ypos) and (ypos + height + gap <= block.ypos + block.height):
                answer = True
            elif (ypos - gap <= block.ypos + block.height) and (ypos - gap >= block.ypos):
                answer = True
            elif (ypos <= block.ypos) and (ypos + height >= block.ypos + block.height):
                answer = True
            elif (ypos >= block.ypos) and (ypos + height <= block.ypos + block.height):
                answer = True
            else:
                answer = False

        if answer:
            break

    return answer