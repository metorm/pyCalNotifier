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
