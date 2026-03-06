# Cloud-Based Student Task & Notes Management System

This repository contains the source code for a cloud-ready Student Task and Notes Management system as requested by the assignment. 

## Local Development (Docker)
1. Ensure Docker and Docker Compose are installed.
2. Run the application:
   ```bash
   docker-compose up --build
   ```
3. Open your browser and navigate to `http://localhost:5001`

## Cloud Deployment Guide (Demo)
During your project demo, follow these steps to demonstrate the full application running on your Cloud VM (e.g., AWS EC2, Ubuntu Server):

1. **Launch Cloud Instance**: Make sure you have opened ports 22 (SSH), 80 (HTTP), and 5001 (app).
2. **Install Docker** on the Cloud VM:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   ```
3. **Deploy**:
   ```bash
   git clone <your-github-repo-url>
   cd student-task-manager-cloud
   sudo docker-compose up -d --build
   ```
4. **Access the Application**:
   Navigate to `http://<YOUR_VM_PUBLIC_IP>:5001`

### Important Cloud Concepts Demonstrated
- **SaaS idea**: Web Application interface for task tracking.
- **Containerization**: Application runs isolated in Docker containers.
- **Database**: Automated MySQL data persistence via Docker volumes.
- **Cloud Storage**: File URLs prepared for AWS S3 bucket integration (simulated when S3 keys aren't provided).

> **Note on S3 Integration**: In `app.py`, S3 upload relies on `boto3`. For a real demo where files are uploaded to an AWS S3 Bucket, set the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, and `S3_BUCKET_NAME` environment variables in `docker-compose.yml` under the `web` service. If not provided, the application will catch the exception and simply store the file metadata and a simulated cloud URL to ensure the demo continues flawlessly.
