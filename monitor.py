import json
from transfer import cheapest_cost
NODES = ['ingest', 'relay', 'archive']
EDGES = [('ingest', 'archive', 90), ('ingest', 'relay', 15), ('relay', 'archive', 20)]
if __name__ == '__main__':
    observed = cheapest_cost(NODES, EDGES, 'ingest', 'archive')
    ok = observed == 35
    print(json.dumps({'fixture':'synthetic offline transfer estimate', 'observed_cost':observed, 'acceptance_ceiling':40, 'result':'PASS' if ok else 'FAIL'}, indent=2))
    raise SystemExit(0 if ok else 1)
