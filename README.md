# COMP3030 - Database and Database Systems - Project
## Stack Overflow Survey Analysis Backend

This is the backend service for the Stack Overflow Survey Analysis project. It provides a FastAPI-based REST API with MySQL database integration.

### Prerequisites

- Docker and Docker Compose installed on your system
- Git (for cloning the repository)

### Environment Setup

1. Create a `.env` file in the `app` directory with the following variables:
```env
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=mydb
MYSQL_USER=user
MYSQL_PASSWORD=userpassword
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin_password
```

### Project Structure

```
app/
├── db/
│   ├── cleaned-data/        # CSV data files
│   └── database-init/       # Database initialization scripts
├── docker-compose.yml       # Docker services configuration
├── Dockerfile              # Backend service container definition
├── import_docker.sh        # Data import script
├── main.py                 # FastAPI application
├── models.py               # Database models
├── auth.py                 # Authentication logic
├── database.py             # Database connection
└── requirements.txt        # Python dependencies
```

### Setup and Running Instructions

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd database-project-stackoverflow-survey-analysis
```

#### 2. Start the Services
From the `app` directory, run:
```bash
docker-compose up --build
```

This command will:
- Build and start the MySQL database
- Build and start the FastAPI backend service
- Import the initial data from CSV files
- Create an admin account
- Start the API server on port 8000

#### 3. Verify the Setup

The backend service will be available at `http://localhost:8000`

You can access:
- API documentation at `http://localhost:8000/docs`
- Alternative API documentation at `http://localhost:8000/redoc`

#### 4. Stopping the Services

To stop all services:
```bash
docker-compose down
```

To stop services and remove volumes (this will delete all data):
```bash
docker-compose down -v
```

### API Endpoints

The API provides several endpoints for data analysis and user management. For detailed API documentation, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Troubleshooting

1. If the database fails to start:
   - Check if port 3306 is available
   - Verify MySQL credentials in `.env` file

2. If data import fails:
   - Check if CSV files are present in `db/cleaned-data/`
   - Verify file permissions on `import_docker.sh`

3. If the backend service fails to start:
   - Check if port 8000 is available
   - Verify all environment variables are set correctly

### Development

To make changes to the code:
1. Modify the relevant files
2. Rebuild the containers:
```bash
docker-compose up --build
```

### Data Files

The project uses cleaned CSV data files located in `app/db/cleaned-data/`. These files are automatically imported into the database during the initial setup.

