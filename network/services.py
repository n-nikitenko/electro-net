def get_network_level(node):
    """
    Рекурсивно вычисляем уровень узла сети на основе его поставщика.
    """
    if node.supplier is None:
        # Если у узла нет поставщика, значит это завод (уровень 0)
        return 0
    else:
        # Рекурсивно вычисляем уровень поставщика
        return get_network_level(node.supplier) + 1
