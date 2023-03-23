entry_sys = lambda x: {"role": "system", "content": x}
entry_usr = lambda x: {"role": "user", "content": x}
entry_factory = {
    "usr": entry_usr,
    "sys": entry_sys,
}
