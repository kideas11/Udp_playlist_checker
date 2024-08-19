import socket
import argparse
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime

BUFFER_SIZE = 65535  # Maximum UDP packet size

def parse_udp_link(udp_link):
    try:
        protocol, address = udp_link.split("://")
        if "@" in address:
            _, address = address.split("@")
        ip, port = address.split(":")
        return ip, int(port)
    except Exception as e:
        raise ValueError(f"Invalid UDP link format: {udp_link} - {str(e)}")
def parse_rtp_link(rtp_link):
    try:
        protocol, address = rtp_link.split("://")
        if "@" in address:
            _, address = address.split("@")
        ip, port = address.split(":")
        return ip, int(port)
    except Exception as e:
        raise ValueError(f"Invalid UDP link format: {rtp_link} - {str(e)}")

def test_udp_link(channel_name, udp_link):
    status = "Failed"
    error_message = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Parse the UDP link
        ip, port = parse_udp_link(udp_link)

        # Create a UDP socket
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            # Set socket timeout to 20 seconds
            udp_socket.settimeout(20)

            # Bind the socket to the address
            udp_socket.bind(('0.0.0.0', port))

            # Join the multicast group
            udp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(ip) + socket.inet_aton('0.0.0.0'))

            # Attempt to receive data to test the link
            data, addr = udp_socket.recvfrom(BUFFER_SIZE)

            status = "Working"
            print(f"Channel: {channel_name} - UDP link {udp_link} is working.")
        except socket.timeout:
            error_message = "Timeout. Make sure the server is running and reachable."
            print(f"Channel: {channel_name} - UDP link {udp_link} failed: {error_message}")
        except socket.error as e:
            if e.errno == 10040:
                error_message = "Received data larger than buffer size."
                print(f"Channel: {channel_name} - UDP link {udp_link} failed: {error_message}")
            else:
                error_message = str(e)
                print(f"Channel: {channel_name} - UDP link {udp_link} failed: {error_message}")
        except Exception as e:
            error_message = str(e)
            print(f"Channel: {channel_name} - UDP link {udp_link} failed: {error_message}")
        finally:
            udp_socket.close()
    except Exception as e:
        error_message = str(e)
        print(error_message)

    return {"timestamp": timestamp, "channel_name": channel_name, "link": udp_link, "protocol": "UDP", "status": status, "error_message": error_message}

def test_rtp_link(channel_name, rtp_link):
    status = "Failed"
    error_message = ""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Parse the UDP link
        ip, port = parse_rtp_link(rtp_link)

        # Create a UDP socket
        rtp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    

        try:
            # Set socket timeout to 20 seconds
            rtp_socket.settimeout(20)

            # Bind the socket to the address
            rtp_socket.bind(('0.0.0.0', int(port)))

            # Join the multicast group
            rtp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(ip) + socket.inet_aton('0.0.0.0'))

            # Attempt to receive data to test the link
            data, addr = rtp_socket.recvfrom(BUFFER_SIZE)

            status = "Working"
            print(f"Channel: {channel_name} - RTP link {rtp_link} is working.")
        except socket.timeout:
            error_message = "Timeout. Make sure the server is running and reachable."
            print(f"Channel: {channel_name} - RTP link {rtp_link} failed: {error_message}")
        except socket.error as e:
            if e.errno == 10040:
                error_message = "Received data larger than buffer size."
                print(f"Channel: {channel_name} - RTP link {rtp_link} failed: {error_message}")
            else:
                error_message = str(e)
                print(f"Channel: {channel_name} - RTP link {rtp_link} failed: {error_message}")
        except Exception as e:
            error_message = str(e)
            print(f"Channel: {channel_name} - RTP link {rtp_link} failed: {error_message}")
        finally:
            rtp_socket.close()
    except Exception as e:
        error_message = "Invalid RTP link format: " + str(e)
        print(error_message)

    return {"timestamp": timestamp, "channel_name": channel_name, "link": rtp_link, "protocol": "RTP", "status": status, "error_message": error_message}

def test_playlist(playlist_file, test_all=False, report_file=None):
    results = []
    try:
        with open(playlist_file, 'r') as f:
            lines = f.readlines()
            channel_name = None
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF:"):
                    channel_name = line.split(",")[1]
                elif line.startswith("udp://") or line.startswith("rtp://"):
                    if channel_name or test_all:
                        if line.startswith("udp://"):
                            result = test_udp_link(channel_name if channel_name else "Unknown Channel", line)
                        elif line.startswith("rtp://"):
                            result = test_rtp_link(channel_name if channel_name else "Unknown Channel", line)
                        results.append(result)
                        channel_name = None
                    else:
                        print("Error: Channel name not found.")
    except Exception as e:
        print("Error reading playlist:", e)

    if report_file:
        generate_report(results, report_file)

    return results

def generate_report(results, report_file):
    try:
        with open(report_file, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'channel_name', 'link', 'protocol', 'status', 'error_message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in results:
                writer.writerow(result)
        print(f"Report generated: {report_file}")
    except Exception as e:
        print(f"Error generating report: {e}")

def send_email(report_file, email_recipient, email_sender, email_password):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = email_recipient
        msg['Subject'] = "UDP/RTP Link Test Report"

        body = "Please find the attached report for the UDP/RTP link tests."
        msg.attach(MIMEText(body, 'plain'))

        # Attach the report file
        attachment = open(report_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {report_file}")
        msg.attach(part)

        # Connect to the server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, email_password)
        text = msg.as_string()
        server.sendmail(email_sender, email_recipient, text)
        server.quit()

        print(f"Report sent to {email_recipient}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test UDP and RTP links in an M3U playlist.")
    parser.add_argument("--playlist", help="Path to M3U playlist file", required=False)
    parser.add_argument("--link", help="Single UDP link to test", required=False)
    parser.add_argument("--rtp_link", help="Single RTP link to test", required=False)
    parser.add_argument("--rtp_playlist", help="Path to RTP M3U playlist file", required=False)
    parser.add_argument("--all", help="Test all URLs in the specified M3U playlist file", required=False)
    parser.add_argument("--report", help="Generate a CSV report", required=False)
    parser.add_argument("--email", help="Send report to the specified email address", required=False)
    parser.add_argument("--email_sender", help="Email address to send the report from", required=False)
    parser.add_argument("--email_password", help="Password for the sender email address", required=False)
    parser.add_argument("--info", help="Contact us at kideas11 or email us as khaleeq@duck.com", required=False)
    args = parser.parse_args()

    results = []

    if args.all:
        results = test_playlist(args.all, test_all=True, report_file=args.report)
    elif args.playlist:
        results = test_playlist(args.playlist, test_all=False, report_file=args.report)
    elif args.link:
        result = test_udp_link("Single Link", args.link)
        results.append(result)
        if args.report:
            generate_report([result], args.report)
    elif args.rtp_link:
        result = test_rtp_link("Single RTP Link", args.rtp_link)
        results.append(result)
        if args.report:
            generate_report([result], args.report)
    elif args.rtp_playlist:
        results = test_playlist(args.rtp_playlist, test_all=True, report_file=args.report)
    else:
        print("Please provide either a playlist file with --playlist, a single UDP link with --link, a single RTP link with --rtp_link, an RTP playlist file with --rtp_playlist, or use --all with a specified M3U playlist file to test all URLs.")

    if args.email and args.report:
        if args.email_sender and args.email_password:
            send_email(args.report, args.email, args.email_sender, args.email_password)
        else:
            print("Email sender and password are required to send email.")
