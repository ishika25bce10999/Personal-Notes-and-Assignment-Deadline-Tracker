# Personal-Notes-and-Assignment-Deadline-Tracker
## Overview of the Project

An intelligent Python application that helps students manage notes and assignments with machine learning-powered risk prediction, automated scheduling, and smart prioritization for optimal academic performance.


## ● Problem Statement
- Students struggle with managing multiple assignments and deadlines efficiently
- No intelligent prioritization of tasks based on urgency and importance
- Lack of predictive insights for deadline risks and optimal work scheduling
- Manual tracking leads to missed deadlines and poor time management

## ● Objectives
- Develop an intelligent deadline tracking system with ML-powered risk assessment
- Provide automated work scheduling and task prioritization
- Enable efficient CRUD operations for notes and assignments
- Offer visual analytics for academic workload management
- Ensure data persistence and system reliability

## ● Functional Requirements
- **User Management**: Login and user session handling
- **Notes CRUD**: Create, read, update, delete personal notes with categories
- **Assignments CRUD**: Manage assignments with subjects, due dates, priorities
- **ML Predictions**: Risk assessment and completion probability scoring
- **Smart Scheduling**: Automated work schedule recommendations
- **Search & Filter**: Find notes/assignments by various criteria
- **Data Visualization**: Charts and analytics for academic workload
- **Data Persistence**: JSON-based local storage system

## ● Non-functional Requirements
- **Performance**: Fast response times (<2 seconds for all operations)
- **Security**: Input validation and secure data storage
- **Usability**: Intuitive menu-driven interface
- **Reliability**: 99% uptime with error recovery
- **Scalability**: Support for 1000+ notes and assignments
- **Maintainability**: Modular code with clear documentation
- **Resource Efficiency**: Low memory and CPU usage

## ● System Architecture Diagram
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Interface │    │   Core Services   │    │   Data Storage   │
│                 │    │                  │    │                 │
│ • Menu System   │◄──►│ • CRUD Service   │◄──►│ • JSON Files    │
│ • Input/Output  │    │ • ML Service     │    │ • Notes DB      │
│ • Display       │    │ • Analytics      │    │ • Assignments DB│
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│   Utilities      │    │   ML Models       │
│                 │    │                  │
│ • Validators    │    │ • Risk Predictor │
│ • Logging       │    │ • Scheduler      │
│ • Security      │    │ • Classifier     │
└─────────────────┘    └──────────────────┘
```

## ● Process Flow or Workflow Diagram
```
Start → Login → Main Menu → Select Module → Perform Operation → Save Data → Continue/Exit
     │          │           │              │               │          │
     │          │           ├─Notes CRUD───┤─Create/Read───┤          │
     │          │           │              │─Update/Delete─┤          │
     │          │           ├─Assignments──┤─Add/View──────┤          │
     │          │           │              │─Modify/Complete│          │
     │          │           ├─ML Analytics─┤─Risk Analysis─┤          │
     │          │           │              │─Schedule Rec──┤          │
     │          │           └─View Data────┤─Statistics────┤          │
     │          │                          │─Search───────┤          │
     └──────────┴──────────────────────────┴──────────────┴──────────┘
```

## ● UML Diagrams

### ○ Use Case Diagram
```
┌─────────────┐
│   Student   │
└──────┬──────┘
       │
       │ ┌─────────────────────────────────┐
       ├─┤ Manage Notes                    │
       │ │ • Create Note                   │
       │ │ • View Notes                    │
       │ │ • Update Note                   │
       │ │ • Delete Note                   │
       │ └─────────────────────────────────┘
       │
       │ ┌─────────────────────────────────┐
       ├─┤ Manage Assignments              │
       │ │ • Add Assignment               │
       │ │ • View Assignments             │
       │ │ • Mark Complete                │
       │ │ • Update Details               │
       │ └─────────────────────────────────┘
       │
       │ ┌─────────────────────────────────┐
       ├─┤ Get ML Insights                 │
       │ │ • Risk Analysis                │
       │ │ • Work Schedule                │
       │ │ • Priority Classification      │
       │ └─────────────────────────────────┘
       │
       │ ┌─────────────────────────────────┐
       └─┤ View Analytics                  │
         │ • Statistics                   │
         │ • Search Data                  │
         └─────────────────────────────────┘
```

### ○ Class Diagram
```
┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   Note           │       │   Assignment     │       │   NoteRepository │
├──────────────────┤       ├──────────────────┤       ├──────────────────┤
│ - id: int        │       │ - id: int        │       │ - storage_file   │
│ - title: str     │       │ - title: str     │       ├──────────────────┤
│ - content: str   │       │ - description: str│       │ + create()      │
│ - priority: Enum │       │ - subject: Enum  │       │ + get_all()      │
│ - category: Enum │       │ - due_date: dt   │       │ + update()       │
│ - created_at: dt │       │ - status: Enum   │       │ + delete()       │
│ - updated_at: dt │       │ - priority: int  │       │ + search()       │
│ - tags: List[str]│       │ - estimated_hrs: float └──────────────────┘
└──────────────────┘       │ - created_at: dt │
          ▲                │ - tags: List[str]│       ┌──────────────────┐
          │                └──────────────────┘       │ AssignmentRepo   │
          │                         ▲                 ├──────────────────┤
          │                         │                 │ - storage_file   │
┌──────────────────┐       ┌──────────────────┐       ├──────────────────┤
│   DeadlineTracker│       │   MLService      │       │ + create()      │
├──────────────────┤       ├──────────────────┤       │ + get_all()      │
│ - note_repo      │──────▶│ - priority_weights│       │ + update()       │
│ - assignment_repo│       ├──────────────────┤       │ + delete()       │
│ - ml_service     │       │ + predict_risk() │       │ + get_upcoming() │
│ - config         │       │ + classify()     │       └──────────────────┘
├──────────────────┤       │ + schedule()     │
│ + run()          │       └──────────────────┘
│ + menu_handlers()│
└──────────────────┘
```

### ○ Sequence Diagram - Adding Assignment
```
Student          UI            CRUD Service      ML Service      Repository
  │               │               │               │               │
  │Add Assignment │               │               │               │
  │──────────────▶│               │               │               │
  │               │Validate Input │               │               │
  │               │──────────────▶│               │               │
  │               │               │Create Object  │               │
  │               │               │───────────────┼──────────────▶│
  │               │               │               │               │Save to JSON
  │               │               │               │Predict Risk   │
  │               │               │──────────────▶│               │
  │               │               │               │Return Risk    │
  │               │Display Success│◀──────────────│               │
  │◀──────────────│               │               │               │
```

## ● Database/Storage Design

### ○ ER Diagram
```
┌─────────────┐        ┌───────────────┐
│    NOTE     │        │  ASSIGNMENT   │
├─────────────┤        ├───────────────┤
│ PK id       │        │ PK id         │
│ title       │        │ title         │
│ content     │        │ description   │
│ priority    │        │ subject       │
│ category    │        │ due_date      │
│ created_at  │        │ status        │
│ updated_at  │        │ priority      │
│ tags[]      │        │ estimated_hrs │
│ is_archived │        │ created_at    │
└─────────────┘        │ tags[]        │
                       └───────────────┘


## Features

Smart Notes Management: Create, organize, and search personal notes with categories and tags
Assignment Tracking: Complete assignment lifecycle management with deadline monitoring
ML Risk Prediction: AI-powered completion risk assessment using multiple factors
Automated Scheduling: Intelligent work schedule recommendations based on priorities
Visual Analytics: Data visualization for workload management and progress tracking
Search & Filter: Advanced search across notes and assignments
Data Persistence: Secure JSON-based local storage system

● Technologies/Tools Used

Programming Language: Python 3.8+
Data Processing: JSON, Datetime, Collections
Machine Learning: Custom ML algorithms for risk prediction
Data Visualization: Matplotlib (optional)
Development Tools: IDLE, VS Code, Python standard library
Architecture: Modular design with Repository pattern

● Steps to Install & Run the Project
Prerequisites:
Python 3.8 or higher installed

Installation Steps:

Download the Code
Run the Application
Launch the application
Use menu options to navigate
Create sample notes and assignments
Explore ML analytics features
View generated reports and schedules

● Instructions for Testing
Test Scenario 1: Basic CRUD Operations
text
1. Create 2 notes with different priorities
2. Create 3 assignments with varying due dates
3. View all created items
4. Update one note and one assignment
5. Mark one assignment as completed

Test Scenario 2: ML Features Demonstration
text
1. Create assignments with:
   - One due tomorrow (high risk)
   - One due in 3 days (medium risk) 
   - One due next week (low risk)
2. Run ML Analytics to see risk predictions
3. Check work schedule recommendations

Test Scenario 3: Data Persistence Testing
text
1. Create multiple notes and assignments
2. Exit the application
3. Restart the application
4. Verify data is preserved and loaded correctly

Expected Test Outcomes:

 All CRUD operations work without errors
 ML predictions show logical risk assessments
 Work schedules prioritize urgent tasks
 Data persists between application sessions
 Search functionality returns correct results




```
