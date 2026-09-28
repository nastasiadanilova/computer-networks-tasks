def elect_root(bridges: list) -> dict:
    def bridge_id(b):
        return (b["priority"], b["mac"])

    root = min(bridges, key=bridge_id)
    ids = [(b["id"], f"{b['priority']}:{b['mac']}") for b in bridges]
    return {"root": root, "bridge_ids": ids}

if __name__ == "__main__":
    import pprint
    bridges = [
        {"id":"SW1","priority":32768,"mac":"aa:bb:cc:dd:ee:01"},
        {"id":"SW2","priority":4096, "mac":"aa:bb:cc:dd:ee:02"},
        {"id":"SW3","priority":32768,"mac":"aa:bb:cc:dd:ee:03"},
    ]
    pprint.pprint(elect_root(bridges))
