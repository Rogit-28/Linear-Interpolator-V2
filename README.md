# Scaling Range Desktop Application 📏

A desktop application for linear scaling of 3D coordinates with real-time calculations and history tracking.

## Features

### Core Functionality
- **Real-time Scaling**: Calculates scaled values as you type
- **Multi-axis Support**: Scale based on X, Y, or Z coordinates with automatic calculation of others
- **Hexadecimal Support**: Handle hexadecimal values in Z coordinate calculations
- **Range-based Scaling**: Define input ranges (X1-X2, Y1-Y2, Z1-Z2) for scaling

### User Interface
- **Desktop Application**: Native desktop experience built with Tauri
- **React Frontend**: Modern React interface with TypeScript
- **Modal Interface**: Clean modal-based UI with tabbed views
- **History Tracking**: Stores calculation history in localStorage

## Tech Stack

### Backend
- **Python 3.8+**: Core scaling logic
- **FastAPI**: REST API server
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server

### Frontend
- **React 19**: Component-based UI
- **Next.js 16**: Full-stack framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling framework
- **Radix UI**: Accessible components

### Desktop
- **Tauri**: Desktop application framework
- **Rust**: Native performance

## Architecture

### Project Structure
```
Scaling-Range/
├── backend/                 # Python FastAPI backend
│   ├── scaling_logic.py     # Core algorithms
│   ├── tauri_backend.py     # Tauri API integration
│   ├── requirements.txt     # Python dependencies
│   ├── test_scaling_logic.py # Unit tests
│   └── test_api.py         # API tests
├── Frontend/scaling/       # Next.js frontend
│   ├── components/         # React components
│   │   ├── scaling-range-modal.tsx # Main calculator
│   │   └── ui/            # UI primitives
│   ├── app/               # Next.js pages
│   ├── lib/utils.ts       # Utility functions
│   └── public/            # Static assets
└── src-tauri/             # Tauri configuration
    ├── Cargo.toml         # Rust dependencies
    └── src/main.rs        # Tauri entry point
```

### Data Flow
1. User inputs coordinates and ranges in React UI
2. Frontend makes POST request to `http://127.0.0.1:8001/scale`
3. FastAPI backend processes request using scaling logic
4. Results returned as JSON response
5. History automatically saved to localStorage

## Getting Started

### Prerequisites
- Node.js (v18+)
- Rust (v1.70+)
- Python (v3.8+)
- npm or yarn

### Installation

1. **Clone and navigate to project**
   ```bash
   git clone <repository-url>
   cd Scaling-Range
   ```

2. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd Frontend/scaling
   npm install
   ```

### Running Development Mode

1. **Start backend server**
   ```bash
   cd backend
   python tauri_backend.py
   ```
   Server starts on `http://127.0.0.1:8001`

2. **Start frontend development server**
   ```bash
   cd Frontend/scaling
   npm run dev
   ```

### Building for Production

**Automatic build**:
```bash
python build_tauri.py
```

**Manual build**:
```bash
# Build frontend
cd Frontend/scaling
npm run build

# Build Tauri app
cd ../src-tauri
cargo tauri build
```

Built executable will be in `src-tauri/target/release/`

## Usage Guide

### Basic Scaling
1. Enter range values (X1-X2, Y1-Y2, Z1-Z2)
2. Select scaling axis (X, Y, or Z) using radio buttons
3. Input value in the selected axis field
4. Other coordinates calculate automatically

### Hexadecimal Mode
1. Check "Z in Hex" checkbox
2. Enter hex values (with or without "0x" prefix)
3. Results display in hexadecimal format

### History Management
- All calculations automatically saved
- Switch to "History" tab to view past calculations
- Clear history using "Clear All" button

## Testing

### Backend Tests
```bash
cd backend
python -m pytest test_scaling_logic.py # Core logic tests
python -m pytest test_api.py           # API endpoint tests
```

### Running All Tests
```bash
cd backend
python -m pytest  # Run all backend tests
```

## API Documentation

### Scaling Endpoint
```
POST /scale
Content-Type: application/json
```

**Request**:
```json
{
  "x_input": "string",
  "y_input": "string",
  "z_input": "string", 
  "x1": "string",
  "x2": "string",
  "y1": "string",
  "y2": "string",
  "z1": "string",
  "z2": "string",
  "scale_from": "x|y|z",
  "z_in_hex": boolean
}
```

**Response**:
```json
{
  "x": "string",
  "y": "string",
  "z": "string"
}
```

### Health Check
```
GET /health
```

## Scaling Algorithm

The application uses linear interpolation:
```
scaled_value = slope * input_value + intercept
slope = (output_end - output_start) / (input_end - input_start)  
intercept = output_start - (slope * input_start)
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature-name`)
3. Make changes
4. Add tests if applicable
5. Run tests (`npm test` and `pytest`)
6. Commit with conventional messages
7. Push and create pull request
