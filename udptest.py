import socket, struct, json, time, sys

MCAST_GRP = '239.1.1.1'   # match LNM addr
MCAST_PORT = 3333

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack('4sl', socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print(f"Listening on {MCAST_GRP}:{MCAST_PORT}...")
last = None
count = 0
while True:
    data, addr = sock.recvfrom(8192)
    now = time.time()
    count += 1

    if len(data) < 12:
        print(f"[{count}] too short ({len(data)}B) from {addr[0]}")
        continue

    magic = data[0:2]
    version = data[2]
    ptype = data[3]
    payload_len, meta_len = struct.unpack('<HH', data[4:8])

    if magic != b'SL':
        print(f"[{count}] bad magic {magic!r} from {addr[0]}")
        continue

    payload = data[12:12+payload_len].decode('utf-8', errors='replace')
    delta = f"+{now-last:.2f}s" if last else "    -   "
    last = now

    try:
        obj = json.loads(payload)
        status = obj.get('status', {})
        keys = list(status.keys())
        # Pull out em1:2 if present for a quick eyeball
        em = status.get('em1:2', {})
        em_summary = ""
        if em:
            em_summary = f" em1:2 V={em.get('voltage')} I={em.get('current')} P={em.get('act_power')}"
        print(f"[{count:4d}] {delta} from {addr[0]} v{version} type={ptype} keys={keys}{em_summary}")
    except json.JSONDecodeError as e:
        print(f"[{count}] {delta} JSON error: {e} -- raw: {payload[:200]}")
