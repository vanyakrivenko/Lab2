import unittest
from main import validate_ipv6, process_ips_from_file, fetch_ips_from_url

class TestIPv6Functions(unittest.TestCase):
  def test_valid_ipv6(self):
    valid_ips = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "2001:db8:85a3::8a2e:370:7334",
        "::1"
    ]
    for ip in valid_ips:
      with self.subTest(ip=ip):
        self.assertTrue(validate_ipv6(ip))

  def test_invalid_ipv6(self):
    invalid_ips = [
        "2001:db8:85a3:0:0:8a2e:0370:7334:1234",
        "2001:db8:85a3::8a2e:370:7334::",
        "12345::6789",
        "abcd:1234:5678:9abc:defg::1",
        "2001:db8:85a3:z:0:8a2e:0370:7334"
    ]
    for ip in invalid_ips:
      with self.subTest(ip=ip):
        self.assertFalse(validate_ipv6(ip))

  def test_process_ips_from_file(self):
    with open("test_ip.txt", "w", encoding="utf-8") as file:
      file.write("2001:0db8:85a3:0000:0000:8a2e:0370:7334\n")
      file.write("::1\n")
      file.write("12345::6789\n")

    expected_valid_ips = [
      "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
      "::1"
    ]
    valid_ips = process_ips_from_file("test_ips.txt")
    self.assertEqual(valid_ips, expected_valid_ips)
  def test_fetch_ips_from_url(self):
    import http.server
    import socketserver
    import threading

    class TestHandler(http.server.SimpleHTTPRequestHandler):
      def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"2001:0db8:85a3:0000:0000:8a2e:0370:7334\n::1\n12345::6789\n")

    PORT = 8000
    httpd = socketserver.TCPServer((", PORT), TestHandler)

    def start_server():
      httpd.serve_forever()

    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    try:
      url = f"http://localhost:{PORT}"
      expected_valid_ips = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "::1"
      ]
      valid_ips=fetch_ips_from_url(url)
      self.assertEqual(valid_ips, expected_valid_ips)
    finally:
    httpd.shutdown()
    server_thread.join()

if __name__ = "__main__":
  unittest.main()
      
