# AWS Cloud Deployment Guide 🚀

This guide provides step-by-step instructions to deploy your **Student Task & Notes Manager** to AWS using **EC2** (Virtual Machine) and **S3** (Object Storage).

---

## 1. Setup AWS S3 (Object Storage)
*The system uses S3 to store uploaded PDF notes.*

1.  **Create S3 Bucket**:
    - Log in to AWS Console → Search for **S3**.
    - Click **Create bucket**.
    - Name it (e.g., `student-notes-bucket-[your-name]`).
    - Keep "Block all public access" **ON** (recommended for security).
    - Click **Create bucket**.

2.  **Create IAM User (for access keys)**:
    - Search for **IAM** → **Users** → **Create user**.
    - Name: `student-hub-app`.
    - Select **Attach policies directly** → Search for `AmazonS3FullAccess` and check it.
    - Finish creating the user.
    - Click the user → **Security credentials** → **Create access key**.
    - Choose **Application running outside AWS** → **Next** → **Create access key**.
    - **SAVE THE ACCESS KEY AND SECRET KEY** (You will need these later).

---

## 2. Setup AWS EC2 (Virtual Machine)
*This will host your Flask app and MySQL database.*

1.  **Launch Instance**:
    - Search for **EC2** → **Instances** → **Launch instances**.
    - **Name**: `Student-Task-Manager-Server`.
    - **AMI**: Select **Ubuntu Server 24.04 LTS**.
    - **Instance type**: `t2.micro` (Free Tier eligible).
    - **Key pair**: Create one or select an existing one (to SSH into the server).

2.  **Configure Security Group (Firewall)**:
    - Under Network settings, create a new Security Group:
    - Add **Allow SSH (Port 22)** (Your IP only).
    - Add **Allow HTTP (Port 80)** (Anywhere).
    - Add **Allow Custom TCP (Port 5001)** (Anywhere) — *This is where the app runs.*

3.  **Launch** and wait for the instance to be "Running."

---

## 3. Prepare the EC2 Server
1.  **Connect to EC2**:
    ```bash
    ssh -i your-key.pem ubuntu@your-ec2-public-ip
    ```
2.  **Install Docker and Git**:
    ```bash
    sudo apt update
    sudo apt install docker.io docker-compose -y
    sudo usermod -aG docker ubuntu
    # Logout and log back in for docker permissions to take effect
    exit
    ssh -i your-key.pem ubuntu@your-ec2-public-ip
    ```

---

## 4. Deploy the Application
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/chitramunjal/StudentTaskMgmt.git
    cd StudentTaskMgmt
    ```
2.  **Configure Environment Variables**:
    - Open `docker-compose.yml`:
    ```bash
    nano docker-compose.yml
    ```
    - Under the `web` service, add your AWS credentials in the `environment` section:
    ```yaml
    environment:
      - AWS_ACCESS_KEY_ID=YOUR_KEY_HERE
      - AWS_SECRET_ACCESS_KEY=YOUR_SECRET_HERE
      - S3_BUCKET_NAME=your-bucket-name-here
      - AWS_REGION=your-region (e.g., us-east-1)
    ```
3.  **Start the Platform**:
    ```bash
    sudo docker-compose up -d --build
    ```

---

## 5. View Your Live Project!
Open your browser and navigate to:
👉 `http://your-ec2-public-ip:5001`

---

## 6. Security & Monitoring Tip
- **Monitoring**: Check the **Monitoring** tab on your EC2 instance dashboard to see real-time CPU and Disk utilization logs.
- **Security**: In your demo, explain how you used specific **Security Groups** to only open port 5001 to the public, keeping the database (3306) isolated.
