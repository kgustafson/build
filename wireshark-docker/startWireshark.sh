docker run -d -p 14500:14500 --restart unless-stopped --name wireshark --privileged -e XPRA_PW=wireshark ffeldhaus/wireshark
echo "open the following URL in your browser: https://localhost:14500/?username=wireshark=password=wireshark"
