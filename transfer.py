from collections import deque

def cheapest_cost(nodes, edges, source, target):
    """Return exact minimum directed path cost, or None if unreachable."""
    if type(nodes) is not list or any(type(n) is not str or not n for n in nodes) or len(set(nodes)) != len(nodes):
        raise ValueError("nodes must be unique nonempty strings")
    known = set(nodes)
    if type(source) is not str or type(target) is not str or source not in known or target not in known:
        raise ValueError("unknown endpoint")
    if type(edges) is not list:
        raise ValueError("edges must be a list")
    adjacency = {n: [] for n in nodes}
    for edge in edges:
        if type(edge) is not tuple or len(edge) != 3:
            raise ValueError("edges must be triples")
        a, b, cost = edge
        if type(a) is not str or type(b) is not str or a not in known or b not in known or type(cost) is not int or cost < 0:
            raise ValueError("invalid edge")
        adjacency[a].append((b, cost))

    pending = deque([(source, 0)])
    seen = {source}
    while pending:
        node, cost = pending.popleft()
        if node == target:
            return cost
        for neighbor, weight in adjacency[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                pending.append((neighbor, cost + weight))
    return None
