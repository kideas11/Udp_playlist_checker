import socket
import argparse

BUFFER_SIZE = 65535  # Maximum UDP packet size

def test_udp_link(channel_name, udp_link):
    try:
        # Parse the UDP link
        protocol, address = udp_link.split("://")[1].split("@")
        ip, port = address.split(":")

        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Set socket timeout to 20 seconds
            udp_socket.settimeout(20)

            # Bind the socket to the address
            udp_socket.bind(('0.0.0.0', int(port)))

            # Join the multicast group
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(ip) + socket.inet_aton('0.0.0.0'))

            # Attempt to receive data to test the link
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)

            print(f"Channel: {channel_name} - UDP link {udp_link} is working.")
        except socket.timeout:
            print(f"Channel: {channel_name} - UDP link {udp_link} failed: Timeout. Make sure the server is running and reachable.")
        except socket.error as e:
            if e.errno == 10040:
                print(f"Channel: {channel_name} - UDP link {udp_link} failed: Received data larger than buffer size.")
            else:
                print(f"Channel: {channel_name} - UDP link {udp_link} failed:", e)
        except Exception as e:
            print(f"Channel: {channel_name} - UDP link {udp_link} failed:", e)
        finally:
            udp_socket.close()
    except Exception as e:
        print("Invalid UDP link format:", e)

def test_playlist(playlist_file):
    try:
        with open(playlist_file, 'r') as f:
            lines = f.readlines()
            channel_name = None
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    channel_name = line.split(",")[1]
                elif line.startswith("udp://"):
                    if channel_name:
                        test_udp_link(channel_name, line)
                        channel_name = None
                    else:
                        print("Error: Channel name not found.")
    except Exception as e:
        print("Error reading playlist:", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test UDP links in an M3U playlist.")
    parser.add_argument("--playlist", help="Path to M3U playlist file", required=True)
    args = parser.parse_args()

    test_playlist(args.playlist)
