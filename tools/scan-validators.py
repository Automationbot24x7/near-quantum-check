import json, urllib.request, base64, time
from concurrent.futures import ThreadPoolExecutor
RPCS = ["https://rpc.mainnet.near.org", "https://free.rpc.fastnear.com"]
def rpc(method, params, i=0):
    for attempt in range(4):
        try:
            req = urllib.request.Request(RPCS[(i+attempt) % 2], json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode(), {"content-type":"application/json"})
            return json.load(urllib.request.urlopen(req, timeout=20))
        except Exception as e:
            time.sleep(1.5)
    return {}
v = rpc("validators", [None])["result"]
pools = [p["account_id"] for p in v["current_validators"]]
def one(ix_pool):
    i, pool = ix_pool
    r = rpc("query", {"request_type":"call_function","finality":"final","account_id":pool,"method_name":"get_owner_id","args_base64":""}, i)
    try: owner = json.loads(bytes(r["result"]["result"]).decode())
    except Exception: return {"pool": pool, "owner": None, "keys": None}
    k = rpc("query", {"request_type":"view_access_key_list","finality":"final","account_id":owner}, i)
    keys = [x["public_key"].split(":")[0] for x in k.get("result",{}).get("keys",[])] if k.get("result") else None
    return {"pool": pool, "owner": owner, "keys": keys}
with ThreadPoolExecutor(8) as ex: out = list(ex.map(one, enumerate(pools)))
json.dump(out, open("data/validator-owners.json","w"), indent=1)
ok = [o for o in out if o["keys"]]
pq = [o for o in ok if any(t.startswith("ml-dsa") for t in o["keys"])]
only = [o for o in pq if all(t.startswith("ml-dsa") for t in o["keys"])]
print("pools", len(pools), "owners with readable keys", len(ok), "with any PQ key", len(pq), "PQ-only", len(only))
for o in pq: print(o)
