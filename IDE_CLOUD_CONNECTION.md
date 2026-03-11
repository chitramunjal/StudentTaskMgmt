# Connecting VS Code to AWS EC2 ☁️

Follow these steps to connect your local IDE directly to your AWS Cloud instance for seamless development and debugging.

### 1. Install Required Extension
1. Open **VS Code** on your Mac.
2. Click on the **Extensions** icon (or press `Cmd + Shift + X`).
3. Search for and install: **"Remote - SSH"** by Microsoft.

---

### 2. Configure SSH Connection
1. Press `Cmd + Shift + P` to open the Command Palette.
2. Type **"Remote-SSH: Add New SSH Host..."** and select it.
3. Enter the SSH connection string:
   ```bash
   ssh -i "/path/to/your-key.pem" ubuntu@your-ec2-public-ip
   ```
   *(Replace with your actual .pem path and EC2 IP)*.
4. Select the default SSH config file (usually `/Users/chitramunjal/.ssh/config`).

---

### 3. Connect to the Cloud
1. Click the **Blue Icon** (><) in the bottom-left corner of VS Code.
2. Select **"Connect to Host..."** and choose the IP you just added.
3. A new VS Code window will open. If asked, select **"Linux"** as the platform.
4. Click **"Open Folder"** and navigate to your project directory:
   `/home/ubuntu/StudentTaskMgmt`

---

### 4. Benefits for your Demo
- **Live Coding**: You can edit the code in the IDE, and it will save directly to the AWS server.
- **Terminal Access**: You get a built-in terminal that is already logged into your EC2 instance.
- **Docker Visibility**: You can use the VS Code Docker extension (Remotely) to see your containers running in the cloud!

> [!IMPORTANT]
> Ensure your **Security Group** in AWS allows SSH traffic (Port 22) from your IP address, or VS Code will time out!
