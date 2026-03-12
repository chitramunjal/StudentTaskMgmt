# Comprehensive Technical Report: Cloud-Based Student Hub 

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

> [!TIP]
> **[SCREENSHOT 1: SYSTEM DASHBOARD]**  
> *Capture a full-page view of your application's dashboard showing the Glassmorphism UI, a few sample tasks, and the cloud health ribbon at the top.*

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

> [!TIP]
> **[SCREENSHOT 2: IAM USER LIST]**  
> *Capture the IAM User dashboard showing your `student-cloud-admin` user and the attached policies to prove secure access control.*

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
# Default region name: eu-north-1
```

---

## 3. AWS Networking & VPC (Prerequisites)
While often overlooked, the underlying VPC (Virtual Private Cloud) structure is critical for our system's isolation.

### 3.1 VPC & Subnetting
The application runs within the **Default VPC** which provides:
- **Internet Gateway**: Allows our EC2 instance to send files to S3.
- **Public Subnet**: Allows users to access the dashboard on Port 80.

### 3.2 Security Group (Firewall) Configuration
We implemented a strict "Least Privilege" security group.
- **GUI Steps**: EC2 Dashboard → **Security Groups** → **Create Security Group**.
- **Rules Configured**:
  | Protocol | Port | Source | Reason |
  | :--- | :--- | :--- | :--- |
  | SSH | 22 | My IP | Secure terminal access and IDE connection |
  | HTTP | 80 | 0.0.0.0/0 | Standard web traffic access |
  | Custom TCP | 5001 | 0.0.0.0/0 | Extended application port access |

> [!TIP]
> **[SCREENSHOT 3: SECURITY GROUP INBOUND RULES]**  
> *Capture the "Inbound Rules" table for your security group showing Port 80 and 22 are open. This is critical for proving network hardening.*

---

## 4. AWS S3: Object Storage Implementation
S3 was chosen for its 99.999999999% durability, ensuring students never lose their notes.

### 4.1 GUI Steps
1. Search **S3** → Click **Create bucket**.
2. **Naming**: `student-notes-bucket-chitra`.
3. **Region**: Match with your EC2 region (`eu-north-1`).
4. **Object Ownership**: ACLs disabled (recommended).
5. **Block Public Access**: Keep **ON** for security.

### 4.2 Application Integration (Boto3)
The Flask app uses the following logic to connect the server to the S3 bucket:
```python
s3_client = boto3.client(
    's3',
    aws_access_key_id='AKIA...', 
    aws_secret_access_key='dRhl...',
    region_name='eu-north-1'
)
```

> [!TIP]
> **[SCREENSHOT 4: S3 BUCKET CONTENTS]**  
> *Capture the inside of your S3 bucket showing the listed PDF files that you uploaded through the application. This proves the S3 integration works.*

---

## 5. AWS EC2: Virtual Machine Deployment
This is the "Brain" of the project where our Docker containers live.

### 5.1 GUI Configuration
1. **Launch Instance**: EC2 Dashboard → **Launch Instance**.
2. **AMI**: Ubuntu 24.04 LTS (Free Tier Eligible).
3. **Instance Type**: `t3.micro`.
4. **Key Pair**: Create new RSA `.pem` key (e.g., `ChitraSSH.pem`).
5. **Network**: Select the Security Group created in Section 3.

> [!TIP]
> **[SCREENSHOT 5: EC2 INSTANCE SUMMARY]**  
> *Capture the "Instance Summary" page showing the instance ID, the "Running" state, and the Public IP address (13.60.57.99).*

---

## 6. IDE-to-Cloud Integration (Professional Workflow)
We connected our local development IDE (VS Code) to the AWS Cloud to enable real-time debugging.

### 6.1 Configuration Steps
1. **Extension**: Install "Remote - SSH" in VS Code.
2. **Key Placement**: Move `.pem` key to `~/.ssh/` on your Mac.
3. **SSH Config**:
   ```bash
   Host student-aws
       HostName 13.60.57.99
       User ubuntu
       IdentityFile ~/.ssh/ChitraSSH.pem
   ```
4. **Connect**: Click bottom-left "><" icon → **Connect to Host** → `student-aws`.

> [!TIP]
> **[SCREENSHOT 6: VS CODE REMOTE SESSION]**  
> *Capture your VS Code window showing the "SSH: student-aws" label in the bottom-left corner and the project files open in the sidebar. This demonstrates IDE-to-Cloud connectivity.*

---

## 7. Containerized Deployment Strategy
The final step uses **Docker Compose** to orchestrate the backend and database.

### 7.1 Multi-Service Commands
On the EC2 server, we run the following to bring the whole system live:
```bash
# Launch production environment
docker-compose up -d --build
```

> [!TIP]
> **[SCREENSHOT 7: TERMINAL DOCKER STATUS]**  
> *Capture your terminal after running `docker-compose ps`. It should show both the `web` and `database` containers as "Up".*

---

## 8. Monitoring & Production Hardening
As a final step, we implemented features to ensure high availability:
1. **Database Retries**: Modified `app.py` to attempt DB connection 5 times to handle container startup latency.
2. **Cloud Metrics Ribbon**: Built a real-time monitor into the dashboard UI to track CPU and Memory health.
3. **AWS Logs**: Used Docker logs to monitor real-time traffic and errors.

> [!TIP]
> **[SCREENSHOT 8: APPLICATION LOGS]**  
> *Capture your terminal showing the output of `docker-compose logs --tail=20`. This proves you are monitoring the system logs.*

---

## 9. Conclusion
This project successfully integrates a robust Python backend with the power of AWS Cloud. By utilizing S3 for storage and EC2 for compute, we have created a scalable, secure, and professional-grade tool that demonstrates the full lifecycle of Cloud Application Development.

---

## Summary Checklist for Screenshots
- [ ] **Screenshot 1**: Web App Dashboard (at http://13.60.57.99)
- [ ] **Screenshot 2**: IAM Users list with student-cloud-admin
- [ ] **Screenshot 3**: Security Group Rules (Port 80/22)
- [ ] **Screenshot 4**: S3 Bucket showing PDF files
- [ ] **Screenshot 5**: EC2 Instance Summary (Running state)
- [ ] **Screenshot 6**: VS Code "Remote-SSH" connection bar
- [ ] **Screenshot 7**: Terminal output of `docker-compose ps`
- [ ] **Screenshot 8**: Terminal output of `docker-compose logs`
