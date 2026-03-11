# Comprehensive Technical Report: Cloud-Based Student Hub ☁️🎓

**Project Name:** Student Task & Notes Management System  
**Framework:** Flask (Python)  
**Infrastructure:** AWS (EC2, S3, IAM)  
**Deployment:** Docker & Docker Compose  

---

## 1. System Introduction & Architecture
The **Student Task & Notes Management System** is a cloud-native platform designed to solve the common student need for centralized organization. The system enables users to manage academic tasks with priority tracking and securely store PDF study notes in the cloud.

### 1.1 Architecture Design
The application utilizes a **Decoupled Three-Tier Architecture**:
1.  **Frontend (UI)**: A premium "Glassmorphism" interface built using Jinja2 templates and modern CSS. It provides a visual feedback loop for task completion and cloud health.
2.  **Backend (API)**: A Python Flask server that handles authentication, database CRUD operations, and multi-part file uploads to the cloud.
3.  **Persistence Layer**: 
    - **MySQL**: Handles structured relational data (User profiles, Task lists).
    - **AWS S3**: Handles unstructured object storage (PDF Files).

### 1.2 Underlying Cloud Logic
To ensure institutional-grade performance, the system is containerized using **Docker**. This allows the environment to remain identical whether running on a local developer Mac or an AWS Ubuntu instance, eliminating the legacy "it works on my machine" problem.

---

## 2. AWS Identity & Access Management (IAM)
Before any cloud resources were provisioned, we established a security-first foundation using IAM.

### 2.1 GUI Steps (AWS Console)
1. **Navigate**: Open AWS Console → Search for **IAM**.
2. **Create User**: Click **Users** → **Create user**.
3. **Identity**: Set Name as `student-cloud-admin`.
4. **Permissions**: Select **Attach policies directly**. 
   - Search for `AmazonS3FullAccess` and check it.
   - Search for `AmazonEC2FullAccess` and check it (for instance management).
5. **Finalize**: Click **Create user**.

### 2.2 Generating Access Keys
1. Click on the new user `student-cloud-admin`.
2. Go to the **Security credentials** tab.
3. Scroll to **Access keys** → **Create access key**.
4. Select **Command Line Interface (CLI)**.
5. Save the **Access Key ID** and **Secret Access Key**.

### 2.3 CLI Integration Command
To connect these credentials to the terminal for automation:
```bash
# Command to configure local CLI with AWS Account
aws configure
# Follow prompts to enter:
# AWS Access Key ID: [Your Key]
# AWS Secret Access Key: [Your Secret]
# Default region name: us-east-1
```

---

## 3. AWS Networking & VPC (Prerequisites)
While often overlooked, the underlying VPC (Virtual Private Cloud) structure is critical for our system's isolation.

### 3.1 VPC & Subnetting
The application runs within the **Default VPC** which provides:
- **Internet Gateway**: Allows our EC2 instance to send files to S3.
- **Public Subnet**: Allows users to access the dashboard on Port 5001.

### 3.2 Security Group (Firewall) Configuration
We implemented a strict "Least Privilege" security group.
- **GUI Steps**: EC2 Dashboard → **Security Groups** → **Create Security Group**.
- **Rules Configured**:
  | Protocol | Port | Source | Reason |
  | :--- | :--- | :--- | :--- |
  | SSH | 22 | My IP | Secure terminal access and IDE connection |
  | Custom TCP | 5001 | 0.0.0.0/0 | Public access to the Student Dashboard |
  | HTTP | 80 | 0.0.0.0/0 | Standard web traffic redirection |

---

## 4. AWS S3: Object Storage Implementation
S3 was chosen for its 99.999999999% durability, ensuring students never lose their notes.

### 4.1 GUI Steps
1. Search **S3** → Click **Create bucket**.
2. **Naming**: `student-task-manager-storage-unique-id`.
3. **Region**: Match with your EC2 region (e.g., US East 1).
4. **Object Ownership**: ACLs disabled (recommended).
5. **Block Public Access**: Keep **ON** for security.

### 4.2 Application Integration (Boto3)
The Flask app uses the following logic to connect the server to the S3 bucket:
```python
import boto3
s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_KEY',
    aws_secret_access_key='YOUR_SECRET'
)
# Command to upload a file to the cloud
s3_client.upload_fileobj(file, BUCKET_NAME, filename)
```

---

## 5. AWS EC2: Virtual Machine Deployment
This is the "Brain" of the project where our Docker containers live.

### 5.1 GUI Configuration
1. **Launch Instance**: EC2 Dashboard → **Launch Instance**.
2. **AMI**: Ubuntu 24.04 LTS (Free Tier Eligible).
3. **Instance Type**: `t2.micro`.
4. **Key Pair**: Create new RSA `.pem` key (e.g., `student-cloud-key.pem`).
5. **Network**: Select the Security Group created in Section 3.

### 5.2 Command Line Provisioning
Once the VM is running, we execute these commands to prepare the environment:
```bash
# Update the system
sudo apt update && sudo apt upgrade -y

# Install Docker Engine & Compose
sudo apt install docker.io docker-compose -y

# Add User to Docker Group (Removes need for 'sudo' for docker commands)
sudo usermod -aG docker ubuntu
exit # Re-login to apply
```

---

## 6. IDE-to-Cloud Integration (Professional Workflow)
We connected our local development IDE (VS Code) to the AWS Cloud to enable real-time debugging.

### 6.1 Configuration Steps
1. **Extension**: Install "Remote - SSH" in VS Code.
2. **Key Placement**: Move `.pem` key to `~/.ssh/` on your Mac.
3. **SSH Config**:
   ```bash
   Host student-aws
       HostName [EC2_PUBLIC_IP]
       User ubuntu
       IdentityFile ~/.ssh/student-cloud-key.pem
   ```
4. **Connect**: Click bottom-left "><" icon → **Connect to Host** → `student-aws`.

This allows us to write code locally while it executes directly on the AWS Hardware.

---

## 7. Containerized Deployment Strategy
The final step uses **Docker Compose** to orchestrate the backend and database.

### 7.1 Multi-Service Commands
On the EC2 server, we run the following to bring the whole system live:
```bash
# Clone the repository
git clone https://github.com/chitramunjal/StudentTaskMgmt.git
cd StudentTaskMgmt

# Launch production environment
docker-compose up -d --build
```

---

## 8. Monitoring & Production Hardening
As a final step, we implemented features to ensure high availability:
1. **Database Retries**: Modified `app.py` to attempt DB connection 5 times with a 2-second sleep, ensuring it handles slow container startups.
2. **Cloud Metrics Ribbon**: Built a real-time monitor into the dashboard UI to track CPU and Memory health.
3. **AWS CloudWatch**: Utilized the native monitoring service to watch for instance crashes or high latency.

---

## 9. Conclusion
This project successfully integrates a robust Python backend with the power of AWS Cloud. By utilizing S3 for storage and EC2 for compute, we have created a scalable, secure, and professional-grade tool that demonstrates the full lifecycle of Cloud Application Development.
