from ics import Todo


def events2PlainText(events):
    assert isinstance(events, list)
    e1 = events[0]
    assert all(isinstance(e, Todo) for e in events)

    oStr = ''
    for t in events:
        oStr += ('> ' + t.name)
        oStr += (((t.description) if t.description else '') + "\n\n")

    return oStr


def events2KDETodoList(events, calendarName):
    assert isinstance(events, list)
    e1 = events[0]
    assert all(isinstance(e, Todo) for e in events)
    assert isinstance(calendarName, str)

    pre_finished = '* [x] '
    pre_not_finished = '* [ ] '

    oStr = "# " + calendarName + "\n\n"
    for t in events:
        oStr += (pre_not_finished + t.name)
        if t.description:
            des = t.description.replace("\n[ ]", "\n    " + pre_not_finished)
            des = des.replace("\n[x]", "\n    " + pre_finished)
            oStr += (des + '\n')
        else:
            oStr += '\n'

    return oStr
