BASE_SPAWN_RATE = 0.02  # 2% chance every frame (60 frames per second)


def chance_spawn(no_items: int) -> float:
    if no_items == 0:
        return BASE_SPAWN_RATE
    return BASE_SPAWN_RATE/no_items
