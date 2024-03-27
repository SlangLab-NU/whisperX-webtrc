## **Deployment Guide for Amazon EC2**

#### *Disclaimer*:

This guide is authored by a recent graduate stepping into the vast and intricate world of software deployment and cloud services. As such, it represents a naive approach to deploying projects on Amazon EC2, aimed primarily at individuals or small teams seeking to understand the basics of cloud-based deployment.

It's important to recognize that this guide does not incorporate advanced practices such as automation, CI/CD pipelines, scalability strategies, or comprehensive security measures which are pivotal in professional environments. The intention behind this document is to offer a straightforward, manual deployment method for educational purposes and for those at the beginning of their cloud computing journey.

For those looking to delve into more advanced deployment strategies and best practices, it's encouraged to seek out additional resources, official documentation from cloud service providers, and contemporary literature on DevOps and cloud engineering.

#### **Preparation**
1. **Choosing the Right Instance**
   - **Requirement:** An instance with an NVIDIA GPU is **required** for this project. 
   - **Recommendation:** We recommend using the `g4dn.xlarge` instance, which includes a T4 GPU. This should suffice for most needs. However, you should assess your model's VRAM requirements and choose an appropriate GPU instance accordingly.
   - **Budgeting and pricing estimation** (for the recommended instance): **under 0.6 USD per hour** (i. e. under 14.4 USD per 24 hours) for a regular "on-demand" offer – that is, before any discounts.  [Check the up-to-date prices](https://aws.amazon.com/ec2/pricing/on-demand/). See the image showing the AWS's pricing-filter config.
   - **Deep Learning AMI:** For ease of setup, use the Amazon Deep Learning AMI, which comes pre-configured with the CUDA environment, eliminating the need for manual CUDA installation. If you opt for a different setup, follow the NVIDIA official guide to install CUDA.
     - **AMI Link:** [Amazon Machine Learning AMIs](https://aws.amazon.com/machine-learning/amis/)

2. **Security Group Configuration:**
   - **Standard API Access:** Ensure ports `80` (HTTP) and `443` (HTTPS) are open to allow standard API access.
   - **WebRTC:** If utilizing WebRTC for connections, open UDP ports `49152` to `65535`.

#### **Project Setup**
3. **Project Retrieval and Setup:**
   - After launching the instance, pull the project from GitHub and install the necessary dependencies as outlined in the project's README file on the front page.

4. **Service Automation:**
   - To ensure the service starts automatically with the system, create a bash script at `/home/ubuntu/whisperX-webtrc/backend/run.sh` with the following content:
     ```bash
     #!/bin/bash
     python3 /home/ubuntu/whisperX-webtrc/backend/backend.py
     ```
   - Then, create a systemd service file at `/etc/systemd/system/transcription-backend.service` with:
     ```
     [Unit]
     Description=Transcription Backend Service
     After=network.target

     [Service]
     WorkingDirectory=/home/ubuntu/whisperX-webtrc/backend
     ExecStart=/bin/bash run.sh
     Restart=always
     User=ubuntu

     [Install]
     WantedBy=multi-user.target
     ```
   - Enable and start the service with:
     ```bash
     sudo systemctl enable transcription-backend.service
     sudo systemctl start transcription-backend.service
     ```

#### **HTTPS Configuration**
5. **Reverse Proxy Setup (Caddy as Example):**
   - **Installation:** Follow the official guide to install Caddy from [Caddy's Installation Guide](https://caddyserver.com/docs/install).
   - **Domain Configuration:** Ensure your domain points to your EC2 instance's IP address.
   - **Caddy Configuration:** Define your reverse proxy and HTTPS redirection in `/etc/caddy/Caddyfile` as follows:
     ```
     api.yourdomain.com {
         reverse_proxy /transcription/* 127.0.0.1:5000
     }

     http://api.yourdomain.com {
         redir https://{host}{uri} permanent
     }
     ```
   - After configuring, restart the Caddy service: `sudo systemctl restart caddy`.


#### **Final Steps**
6. **Verification:**
   - Ensure that the backend service is running and that the Caddy server is correctly redirecting and reverse proxying requests. Verify that you can access the backend API through `https://api.yourdomain.com`.
