def entry_sys(x):
    return {"role": "system", "content": x}


def entry_usr(x):
    return {"role": "user", "content": x}


entry_factory = {
    "usr": entry_usr,
    "sys": entry_sys,
}
