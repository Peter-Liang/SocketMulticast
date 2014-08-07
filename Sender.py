__author__ = 'Peter Liang'

import socket
import struct
from datetime import datetime

message = 'very important data'
multicast_group = ('224.3.29.71', 9999)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(1)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 2)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

try:


    while True:
        # Send data to the multicast group
        print('"%s": sending "%s"' % (datetime.now().strftime('%H:%M:%S'), message))
        sent = sock.sendto(message.encode('utf-8'), multicast_group)

        # Look for responses from all recipients
        print('%s: waiting to receive' % datetime.now().strftime('%H:%M:%S'))
        try:
            data, server = sock.recvfrom(16)
        except socket.timeout:
            print('timed out, no more responses')
            # break
        else:
            print('received "%s" from %s' % (data, server))

finally:
    print('closing socket')
    sock.close()