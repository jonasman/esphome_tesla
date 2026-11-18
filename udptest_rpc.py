import socket, json, time

LISTEN_PORT = 1111
SHELLY_ADDR = '10.0.1.39'  # informational only, not used for filtering

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', LISTEN_PORT))

print(f"Listening for unicast RPC on :{LISTEN_PORT} (expecting {SHELLY_ADDR})...")
last = None
count = 0
while True:
    data, addr = sock.recvfrom(8192)
    now = time.time()
    count += 1
    delta = f"+{now-last:.2f}s" if last else "    -   "
    last = now

    try:
        obj = json.loads(data.decode('utf-8'))
        method = obj.get('method')
        params = obj.get('params', obj)
        em = params.get('em1:2', {})
        em_summary = ""
        if em:
            em_summary = f" em1:2 V={em.get('voltage')} I={em.get('current')} P={em.get('act_power')}"
        print(f"[{count:4d}] {delta} from {addr[0]} method={method} keys={list(params.keys())}{em_summary}")
        if method == 'NotifyEvent':
            print(f"       events={json.dumps(params.get('events'))}")
    except json.JSONDecodeError as e:
        print(f"[{count}] {delta} from {addr[0]} JSON error: {e} ({len(data)}B) -- raw: {data[:300]!r}")
