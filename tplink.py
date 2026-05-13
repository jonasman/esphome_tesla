from scapy.all import srp1, Ether, Raw

# Define the custom interface (e.g., 'eth0' on Linux or network GUID on Windows)
interface = "wlan0"

# Craft the HomePlug AV protocol discovery frame
# 0x88e1 = HomePlug AV EtherType
# The Raw hex string represents a standard Qualcomm discovery payload structure
discovery_packet = Ether(dst="ff:ff:ff:ff:ff:ff", type=0x88e1) / Raw(load=b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

print("Sending Layer 2 HomePlug AV probe packet...")
# Send Layer 2 packet and wait for a single response frame
reply = srp1(discovery_packet, iface=interface, timeout=4, verbose=False)

if reply:
    print(f"SUCCESS: Powerline adapter is ALIVE.")
    print(f"Responding Adapter MAC Address: {reply.src}")
else:
    print("FAILED: No response from base powerline unit. It may be powered off, dead, or unlinked.")
