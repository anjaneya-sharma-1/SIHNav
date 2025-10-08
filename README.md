# 🧭 SIHNav - Smart Indoor Navigation System

<div align="center">

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com/)

**An intelligent indoor navigation solution designed for Smart India Hackathon 2024**

[Live Demo](https://sih-nav.vercel.app/) • [Report Bug](https://github.com/anjaneya-sharma-1/SIHNav/issues) • [Request Feature](https://github.com/anjaneya-sharma-1/SIHNav/issues)

</div>

---

## 🌟 Overview

**SIHNav** is an advanced indoor navigation system that leverages cutting-edge technologies to provide seamless wayfinding experiences in complex indoor environments. Built as part of the Smart India Hackathon initiative, this platform addresses the critical challenge of indoor navigation where traditional GPS systems fail.

The system combines real-time positioning, intelligent pathfinding algorithms, and an intuitive user interface to guide users through multi-floor buildings, campuses, shopping malls, hospitals, and other large indoor facilities.

### 🎯 Key Highlights

- **Real-time Navigation**: Get instant directions and live updates as you move
- **Multi-floor Support**: Seamlessly navigate across different building levels
- **Accessibility-focused**: Optimized routes for users with different accessibility needs
- **Smart Pathfinding**: AI-powered algorithms find the most efficient routes
- **Cross-platform**: Works on desktop, mobile, and tablet devices
- **Offline Capability**: Download maps for offline navigation

---

## ✨ Features

### 🗺️ Navigation Core

- **Interactive Floor Plans**: High-resolution, interactive maps with zoom and pan functionality
- **Turn-by-Turn Directions**: Clear, step-by-step navigation guidance
- **Multi-destination Routing**: Plan routes with multiple waypoints
- **Dynamic Rerouting**: Automatically adjusts routes based on real-time conditions
- **Voice Guidance**: Audio navigation instructions for hands-free operation

### 🎨 User Experience

- **Intuitive Interface**: Clean, modern UI built with React and TypeScript
- **Search Functionality**: Quick search for rooms, departments, or facilities
- **Favorites & History**: Save frequently visited locations
- **Custom Markers**: Add personal notes and markers on maps
- **Dark Mode**: Eye-friendly interface for low-light environments

### 🔧 Technical Features

- **Real-time Position Tracking**: WiFi/Bluetooth-based indoor positioning
- **Optimized Performance**: Fast load times and smooth animations
- **Responsive Design**: Adapts seamlessly to all screen sizes
- **Progressive Web App**: Install as a standalone app on any device
- **Analytics Dashboard**: Track usage patterns and popular routes

### ♿ Accessibility

- **Wheelchair-friendly Routes**: Special routing for accessibility needs
- **Screen Reader Support**: Full WCAG 2.1 compliance
- **High Contrast Mode**: Enhanced visibility options
- **Adjustable Font Sizes**: Customizable text display

---

## 🛠️ Tech Stack

### Frontend

- **React** - Component-based UI library
- **TypeScript** - Type-safe JavaScript
- **React Router** - Client-side routing
- **Leaflet.js** - Interactive mapping library
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Animation library
- **Axios** - HTTP client

### Backend

- **Python** - Core backend language
- **Flask/FastAPI** - RESTful API framework
- **NumPy** - Numerical computing
- **Pathfinding Algorithms** - Dijkstra's, A* implementation

### Infrastructure

- **Vercel** - Frontend deployment and hosting
- **MongoDB** - Database for map data and user information
- **Redis** - Caching layer for performance
- **GitHub Actions** - CI/CD pipeline

### Development Tools

- **Vite** - Fast build tool and dev server
- **ESLint** - Code linting
- **Prettier** - Code formatting
- **Jest** - Unit testing
- **Cypress** - E2E testing

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v18.0.0 or higher)
- **Python** (v3.9 or higher)
- **npm** or **yarn** package manager
- **Git** for version control

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/anjaneya-sharma-1/SIHNav.git
cd SIHNav
```

2. **Install frontend dependencies**

```bash
npm install
# or
yarn install
```

3. **Install backend dependencies**

```bash
cd backend
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the root directory:

```env
VITE_API_URL=http://localhost:5000
VITE_MAP_API_KEY=your_map_api_key
DATABASE_URL=your_mongodb_url
REDIS_URL=your_redis_url
```

5. **Run the development server**

**Frontend:**
```bash
npm run dev
# or
yarn dev
```

**Backend:**
```bash
cd backend
python app.py
```

6. **Open your browser**

Navigate to `http://localhost:5173` to see the application running.

### Building for Production

```bash
npm run build
# or
yarn build
```

The production-ready files will be generated in the `dist` directory.

---

## 📖 Usage

### Basic Navigation

1. **Search for a destination**: Use the search bar to find rooms, departments, or facilities
2. **Select your starting point**: The app will auto-detect your location or you can manually select it
3. **View the route**: The system will display the optimal path with turn-by-turn directions
4. **Start navigation**: Follow the highlighted path and voice/text instructions

### Advanced Features

#### Multi-waypoint Routing

```javascript
// Add multiple destinations to your route
const waypoints = [
  { name: 'Cafeteria', floor: 1 },
  { name: 'Library', floor: 2 },
  { name: 'Lab 301', floor: 3 }
];
```

#### Custom Route Preferences

- **Shortest Distance**: Minimize walking distance
- **Fastest Route**: Consider walking speed and congestion
- **Accessible Route**: Elevator and ramp-only paths
- **Scenic Route**: Pass through aesthetically pleasing areas

---

## 📁 Project Structure

```
SIHNav/
├── src/
│   ├── components/          # React components
│   │   ├── Map/            # Map-related components
│   │   ├── Navigation/     # Navigation UI components
│   │   ├── Search/         # Search functionality
│   │   └── Common/         # Reusable components
│   ├── pages/              # Page components
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   ├── types/              # TypeScript type definitions
│   ├── styles/             # Global styles
│   └── App.tsx             # Root component
├── backend/
│   ├── app.py              # Flask/FastAPI application
│   ├── routes/             # API routes
│   ├── models/             # Data models
│   ├── algorithms/         # Pathfinding algorithms
│   └── utils/              # Helper functions
├── public/                 # Static assets
├── tests/                  # Test files
├── .github/                # GitHub workflows
├── package.json            # Frontend dependencies
├── requirements.txt        # Backend dependencies
├── vite.config.ts          # Vite configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Contribution Guidelines

- Follow the existing code style and conventions
- Write meaningful commit messages
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

### Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) to maintain a respectful and inclusive community.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Developer & Maintainer**: [Anjaneya Sharma](https://github.com/anjaneya-sharma-1)

Built with ❤️ for Smart India Hackathon 2024

---

## 🙏 Acknowledgments

- Smart India Hackathon organizing committee
- Open-source community for amazing tools and libraries
- Beta testers and early adopters for valuable feedback
- All contributors who have helped improve this project

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/anjaneya-sharma-1/SIHNav/issues)
- **Discussions**: [GitHub Discussions](https://github.com/anjaneya-sharma-1/SIHNav/discussions)
- **Website**: [sih-nav.vercel.app](https://sih-nav.vercel.app/)

---

<div align="center">

**⭐ If you find this project helpful, please give it a star!**

Made with 💙 by [Anjaneya Sharma](https://github.com/anjaneya-sharma-1)

</div>
