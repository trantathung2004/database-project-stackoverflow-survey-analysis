# COMP3030 - Database and Database Systems - Project
## Stackoverflow Developer Survey Analysis

### Project Description

This project involves designing and implementing a comprehensive database system to store, analyze, and visualize responses from the Stack Overflow Annual Developer Survey. Our solution will provide an interactive platform for exploring developer trends, demographics, technology preferences, and career insights. The database will serve as the foundation for a web-based interface that allows users to filter, compare, and visualize survey data through dynamic charts and reports. By effectively organizing and normalizing the extensive survey dataset, we aim to create a robust system that enables meaningful insights into the global developer community while demonstrating advanced database design and implementation techniques.

### Functional Requirements

- Database Management:
  - Store and manage all survey data in normalized relational tables.
  - Implement views to support frequently used query patterns.
  - Set up triggers to maintain data integrity and enable audit trails.
  - Optimize performance using indexing and partitioning strategies.

- Web Application Features:
  - Develop a responsive web interface that supports full CRUD (Create, Read, Update, Delete) operations for relevant entities.
  - Enable users to filter, search, and explore data in real time.
  - Provide dashboards for statistical summaries and visualizations using charts and graphs.

### Non-Functional Requirements

- Performance
  - Query response time under 2 seconds for standard reports
  - Support for concurrent users
  - Efficient handling of large datasets (5+ years of survey data)

- Security
  - Data encryption at rest and in transit
  - Secure authentication mechanisms

- Scalability
  - Horizontal scaling capability for increased user load
  - Modular architecture to support future feature expansion
  - Performance optimization for growing dataset sizes

### Planned Core Entities

- User: Represents a survey respondent.
  - Attributes: `user_id`, `country`, `age`, `gender`, `education_level`, `employment_status`, `years_of_experience`, etc.

- Technology: Represents a programming language, framework, or tool mentioned by users.
  - Attributes: `tech_id`, `name`, `category` (e.g., language, tool, database)

- UserTechnology: Represents a many-to-many relationship between users and technologies they use or want to learn.
  - Attributes: `user_id`, `tech_id`, `proficiency_level`, `interest_level`

- JobPreference: Stores job-seeking preferences and satisfaction.
  - Attributes: `user_id`, `remote_preference`, `salary_expectation`, `job_satisfaction`, `career_change_interest`

- SurveyResponse: Contains general responses not specific to other entities.
  - Attributes: `response_id`, `user_id`, `question_code`, `answer_text`, `timestamp`

- Question: Stores survey questions and metadata.
  - Attributes: `question_code`, `question_text`, `section`, `question_type`

### Tech Stack

- Database
  - MySQL - Primary relational database
  - Database design optimized for analytical queries
  - Stored procedures for complex analytical operations

- Backend
  - Python with FastAPI framework
  - RESTful API architecture
  - JWT authentication 
  - Pandas and NumPy for data processing
  - R for data visualization

- Frontend
  - React.js with Material UI components
  - Chart.js and D3.js for data visualization
  - Responsive design with CSS Grid and Flexbox

- Development Tools
  - Git for version control
  - Docker for containerization
  - GitHub Actions for CI/CD

### Team Members and Roles 
- Tran Tat Hung
- Dang Duc Dat 

### Timeline

| Milestone                                        | Deliverables                                                                                | Due Date        |
|------------------------------------------------- | ------------------------------------------------------------------------------------------- | --------------- |
| Team registration & topic selection              | Project proposal, README.md, Initial GitHub repository setup                                | Tuesday, May 6  |
| Peer review (evaluate other teams' proposals)    | Complete project requirements, Functional/Non-functional specs, Draft ERD                   | Tuesday, May 13 |
| Submit design document (ERD, DDL, task division) | Final ERD, DDL scripts, Database design documentation, Task division                        | Tuesday, May 20 |
| Final submission & presentation slide            | Complete database implementation, Working web interface, Documentation, Presentation slides | Tuesday, May 27 |

