# Cloud-Based Student Task & Notes Management System
## Final Project Report

### 1. System Architecture
This project implements a cloud-heavy, decoupled architecture:
- **Frontend**: HTML5, Vanilla CSS, and Jinja2 templating.
- **Backend API**: Python Flask handling routing, authentication, and database integration.
- **Database**: MySQL containerized via Docker ensuring data persistence.
- **Storage**: AWS S3 Object Storage for uploading and serving student notes.
- **Hosting**: Cloud Virtual Machine (e.g., Ubuntu Server).

---

### 2. Security Implementation
The system incorporates security at both the application and infrastructure levels.

**Application-Level Role-Based Access:**
- Unauthenticated users are strictly routed to the `Login` or `Register` pages.
- Only logged-in students maintain a session state allowing them to:
  - Add, edit, and delete their specific tracking tasks.
  - Upload PDF notes directly to the Cloud Object Storage bucket.
  - View their personalized dashboard.

**Infrastructure-Level Security Groups (Firewalls):**
When deployed to the Cloud VM, the network security rules explicitly whitelist only required traffic:
- **Port 22 (SSH)**: Strictly for developer access to manage the server.
- **Port 80 (HTTP)**: General web traffic routing.
- **Port 5000 (App)**: Specifically opened to serve the underlying Flask application to the internet.

---

### 3. Monitoring strategy
To ensure high availability and application health, cloud-native monitoring tools (e.g., AWS CloudWatch) will be used to track critical metrics:
- **CPU Utilization**: Tracking spikes that could indicate high traffic or infinite loops.
- **Memory/Disk Usage**: Ensuring the instance doesn't run out of memory from intense Docker workloads or extensive log files.
- **Network In/Out**: Monitoring data egress/ingress traffic, highly relevant for the S3 PDF Note downloads.

---

### 4. Cloud Concepts Demonstrated
By completing this project, the following cloud computing concepts have been successfully implemented and demonstrated:

| Concept | Where/How Used |
|---|---|
| **IaaS (Infrastructure as a Service)** | Cloud Virtual Machine (Ubuntu EC2) hosting the platform. |
| **PaaS (Platform as a Service)** | Managed MySQL database running seamlessly in an isolated environment. |
| **SaaS Idea** | The web application itself acts as a student productivity tool. |
| **Containerization** | Docker utilized to guarantee "runs anywhere" environment parity. |
| **Version Control** | GitHub Integration bridging local development to Cloud deployment. |
| **Storage** | Object storage utilized via S3 for scalable file hosting. |
| **Networking** | Security groups tightly controlling access at the packet level. |
| **Monitoring (UI)** | Dashboard integrated with mock cloud metrics (CPU/Disk) to demonstrate real-time monitoring concepts. |

---

### 5. Enhanced Development Features (Phase 4)
To exceed the basic requirements, the system now includes:
- **Task Prioritization**: Enums used in the database (`Low`, `Medium`, `High`) to help students manage workloads.
- **Dynamic Filtering**: Real-time SQL-based search and priority filtering on the Dashboard.
- **Modern UX/UI**: A premium design system using Glassmorphism, CSS gradients, and the Outfit typography.
- **Cloud Metrics Dashboard**: Provides the user with a bird's-eye view of server health, simulating a managed cloud infrastructure.
