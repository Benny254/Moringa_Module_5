from data import inventory


def get_all_items():
    return inventory


def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(item):
    inventory.append(item)
    return item


def update_item(item_id, updates):
    item = get_item(item_id)

    if item:
        item.update(updates)
        return item

    return None


def delete_item(item_id):
    item = get_item(item_id)

    if item:
        inventory.remove(item)
        return True

    return False