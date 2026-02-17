# Complete Setup Guide

## Prerequisites
Before setting up this project, ensure you have the following installed:
- **Node.js** (v18+)
- **Python** (v3.10+)
- **pip** (Python package installer)
- **npm** or **yarn**

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Backend Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000`

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
```

### 3. Start Development Server
```bash
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

## Using 3D Visualizations

The platform now includes two advanced 3D visualization components:

### ThreatGlobe3D
Visualizes global threat distribution on an interactive 3D globe.

```tsx
import ThreatGlobe3D from '@/components/ThreatGlobe3D';

const threats = [
  { id: 1, position: [1, 0, 0], severity: 'high', type: 'malware' },
  { id: 2, position: [0, 1, 0], severity: 'critical', type: 'ddos' },
];

<ThreatGlobe3D threats={threats} />
```

### NetworkGraph3D
Shows network topology with 3D interactive nodes and connections.

```tsx
import NetworkGraph3D from '@/components/NetworkGraph3D';

const nodes = [
  { id: 'server1', label: 'Main Server', position: [0, 0, 0], type: 'server' },
  { id: 'client1', label: 'Client', position: [2, 1, 0], type: 'client' },
];

const edges = [
  { source: 'server1', target: 'client1', strength: 0.8 },
];

<NetworkGraph3D nodes={nodes} edges={edges} />
```

## Environment Variables

Create a `.env` file in the backend directory:
```
DATABASE_URL=sqlite:///./security.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
```

Create a `.env.local` file in the frontend directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

### Backend Issues
- **Port Already in Use**: Change the port in the uvicorn command
- **Module Not Found**: Ensure all dependencies are installed and venv is activated

### Frontend Issues
- **3D Components Not Rendering**: Ensure Three.js dependencies are installed
- **API Connection Failed**: Check backend is running and CORS is configured

## Production Deployment

### Backend
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
npm run build
npm start
```

## Docker Setup (Optional)

Build and run with Docker Compose:
```bash
docker-compose up --build
```

## Support

For issues and questions, please open an issue on GitHub.
