"""
Personal Notes and Assignment Deadline Tracker

"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field

# Configuration
class Config:
    def __init__(self):
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )

# Enums and Data Models
class NotePriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class AssignmentStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Subject(Enum):
    MATH = "math"
    SCIENCE = "science"
    COMPUTER_SCIENCE = "computer_science"
    OTHER = "other"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Note:
    id: int
    title: str
    content: str
    priority: NotePriority
    created_at: datetime
    updated_at: datetime
    tags: List[str] = field(default_factory=list)

@dataclass
class Assignment:
    id: int
    title: str
    description: str
    subject: Subject
    due_date: datetime
    status: AssignmentStatus
    priority: int
    estimated_hours: float
    created_at: datetime

    @property
    def days_until_due(self) -> int:
        return max(0, (self.due_date - datetime.now()).days)

# Repository Classes
class BaseRepository:
    def __init__(self, storage_file: str):
        self.storage_file = storage_file
        self._ensure_storage()
    
    def _ensure_storage(self):
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)
    
    def _load_data(self) -> List[Any]:
        try:
            with open(self.storage_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, data: List[Any]):
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

class NoteRepository(BaseRepository):
    def __init__(self):
        super().__init__("data/notes.json")
    
    def get_all(self) -> List[Note]:
        data = self._load_data()
        notes = []
        for item in data:
            try:
                note = Note(
                    id=item['id'],
                    title=item['title'],
                    content=item['content'],
                    priority=NotePriority(item['priority']),
                    created_at=datetime.fromisoformat(item['created_at']),
                    updated_at=datetime.fromisoformat(item['updated_at']),
                    tags=item.get('tags', [])
                )
                notes.append(note)
            except (KeyError, ValueError) as e:
                logging.warning(f"Skipping invalid note: {e}")
        return notes
    
    def create(self, note_data: Dict[str, Any]) -> Note:
        notes = self.get_all()
        new_id = max([note.id for note in notes], default=0) + 1
        
        now = datetime.now()
        note = Note(
            id=new_id,
            title=note_data['title'],
            content=note_data['content'],
            priority=NotePriority(note_data.get('priority', 'medium')),
            created_at=now,
            updated_at=now,
            tags=note_data.get('tags', [])
        )
        
        notes.append(note)
        self._save_data([note.to_dict() for note in notes])
        logging.info(f"Created note with ID: {new_id}")
        return note
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'priority': self.priority.value,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'tags': self.tags
        }

# Add to_dict method to Note class
def note_to_dict(note: Note) -> Dict[str, Any]:
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'priority': note.priority.value,
        'created_at': note.created_at.isoformat(),
        'updated_at': note.updated_at.isoformat(),
        'tags': note.tags
    }

# Add to_dict method to Assignment class
def assignment_to_dict(assignment: Assignment) -> Dict[str, Any]:
    return {
        'id': assignment.id,
        'title': assignment.title,
        'description': assignment.description,
        'subject': assignment.subject.value,
        'due_date': assignment.due_date.isoformat(),
        'status': assignment.status.value,
        'priority': assignment.priority,
        'estimated_hours': assignment.estimated_hours,
        'created_at': assignment.created_at.isoformat()
    }

class AssignmentRepository(BaseRepository):
    def __init__(self):
        super().__init__("data/assignments.json")
    
    def get_all(self) -> List[Assignment]:
        data = self._load_data()
        assignments = []
        for item in data:
            try:
                assignment = Assignment(
                    id=item['id'],
                    title=item['title'],
                    description=item['description'],
                    subject=Subject(item['subject']),
                    due_date=datetime.fromisoformat(item['due_date']),
                    status=AssignmentStatus(item['status']),
                    priority=item['priority'],
                    estimated_hours=item['estimated_hours'],
                    created_at=datetime.fromisoformat(item['created_at'])
                )
                assignments.append(assignment)
            except (KeyError, ValueError) as e:
                logging.warning(f"Skipping invalid assignment: {e}")
        return assignments
    
    def create(self, assignment_data: Dict[str, Any]) -> Assignment:
        assignments = self.get_all()
        new_id = max([a.id for a in assignments], default=0) + 1
        
        # Fix: Handle date parsing properly
        due_date = assignment_data['due_date']
        if isinstance(due_date, str):
            due_date = datetime.fromisoformat(due_date)
        
        assignment = Assignment(
            id=new_id,
            title=assignment_data['title'],
            description=assignment_data.get('description', ''),
            subject=Subject(assignment_data['subject']),
            due_date=due_date,
            status=AssignmentStatus(assignment_data.get('status', 'not_started')),
            priority=assignment_data.get('priority', 5),
            estimated_hours=assignment_data.get('estimated_hours', 1.0),
            created_at=datetime.now()
        )
        
        assignments.append(assignment)
        self._save_data([assignment_to_dict(a) for a in assignments])
        logging.info(f"Created assignment with ID: {new_id}")
        return assignment
    
    def update_status(self, assignment_id: int, status: AssignmentStatus) -> bool:
        assignments = self.get_all()
        for assignment in assignments:
            if assignment.id == assignment_id:
                assignment.status = status
                self._save_data([assignment_to_dict(a) for a in assignments])
                return True
        return False

# ML Service
class MLService:
    def predict_completion_risk(self, assignment: Assignment) -> Tuple[RiskLevel, float]:
        days_factor = max(0, 10 - assignment.days_until_due) / 10.0
        priority_factor = assignment.priority / 10.0
        hours_factor = min(assignment.estimated_hours / 20.0, 1.0)
        
        risk_score = (days_factor * 0.4 + priority_factor * 0.4 + hours_factor * 0.2)
        risk_score = max(0.0, min(1.0, risk_score))
        
        if risk_score < 0.3:
            risk_level = RiskLevel.LOW
        elif risk_score < 0.7:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.HIGH
        
        return risk_level, risk_score
    
    def recommend_work_schedule(self, assignments: List[Assignment], available_hours: float = 8.0) -> List[Dict[str, Any]]:
        pending = [a for a in assignments if a.status != AssignmentStatus.COMPLETED]
        if not pending:
            return []
        
        # Sort by risk and due date
        scored_assignments = []
        for assignment in pending:
            risk_level, risk_score = self.predict_completion_risk(assignment)
            score = risk_score * 0.7 + (1.0 / max(1, assignment.days_until_due)) * 0.3
            scored_assignments.append((assignment, score))
        
        scored_assignments.sort(key=lambda x: x[1], reverse=True)
        
        schedule = []
        remaining_hours = available_hours
        
        for assignment, score in scored_assignments:
            if remaining_hours <= 0:
                break
            
            allocated = min(assignment.estimated_hours * 0.6, remaining_hours)
            if allocated > 0.5:  # Only allocate if meaningful time
                risk_level, _ = self.predict_completion_risk(assignment)
                schedule.append({
                    'assignment': assignment,
                    'allocated_hours': allocated,
                    'risk_level': risk_level
                })
                remaining_hours -= allocated
        
        return schedule

# Main Application
class DeadlineTrackerApp:
    def __init__(self):
        self.config = Config()
        self.note_repo = NoteRepository()
        self.assignment_repo = AssignmentRepository()
        self.ml_service = MLService()
        logging.info("Application started")
    
    def display_menu(self):
        print("\n" + "="*40)
        print("    DEADLINE TRACKER")
        print("="*40)
        print("1. Notes Management")
        print("2. Assignment Management") 
        print("3. ML Analytics")
        print("4. View All Data")
        print("0. Exit")
        print("="*40)
    
    def notes_management(self):
        while True:
            print("\n--- Notes ---")
            print("1. Create Note")
            print("2. View Notes")
            print("3. Back")
            
            choice = input("Choice: ").strip()
            
            if choice == '1':
                self.create_note()
            elif choice == '2':
                self.view_notes()
            elif choice == '3':
                break
            else:
                print("Invalid choice")
    
    def create_note(self):
        try:
            title = input("Title: ").strip()
            content = input("Content: ").strip()
            
            if not title or not content:
                print("Title and content are required!")
                return
            
            note_data = {
                'title': title,
                'content': content,
                'priority': input("Priority (low/medium/high) [medium]: ").strip() or "medium",
                'tags': [tag.strip() for tag in input("Tags (comma separated): ").split(',') if tag.strip()]
            }
            
            note = self.note_repo.create(note_data)
            print(f"✓ Note created (ID: {note.id})")
            
        except Exception as e:
            print(f"Error creating note: {e}")
    
    def view_notes(self):
        notes = self.note_repo.get_all()
        if not notes:
            print("No notes found")
            return
        
        print(f"\n--- Notes ({len(notes)} total) ---")
        for note in notes:
            print(f"ID: {note.id} | {note.title} | {note.priority.value}")
            print(f"Created: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            if note.tags:
                print(f"Tags: {', '.join(note.tags)}")
            print("-" * 30)
    
    def assignment_management(self):
        while True:
            print("\n--- Assignments ---")
            print("1. Create Assignment")
            print("2. View Assignments")
            print("3. Mark Complete")
            print("4. Back")
            
            choice = input("Choice: ").strip()
            
            if choice == '1':
                self.create_assignment()
            elif choice == '2':
                self.view_assignments()
            elif choice == '3':
                self.mark_complete()
            elif choice == '4':
                break
            else:
                print("Invalid choice")
    
    def create_assignment(self):
        try:
            title = input("Title: ").strip()
            if not title:
                print("Title is required!")
                return
            
            # Fix: Better date input handling
            due_date_str = input("Due date (YYYY-MM-DD): ").strip()
            try:
                due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
            except ValueError:
                print("Invalid date format! Use YYYY-MM-DD")
                return
            
            assignment_data = {
                'title': title,
                'description': input("Description: ").strip(),
                'subject': input("Subject (math/science/computer_science/other) [other]: ").strip() or "other",
                'due_date': due_date,
                'priority': int(input("Priority (1-10) [5]: ").strip() or "5"),
                'estimated_hours': float(input("Estimated hours [1.0]: ").strip() or "1.0")
            }
            
            assignment = self.assignment_repo.create(assignment_data)
            print(f"✓ Assignment created (ID: {assignment.id})")
            
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error creating assignment: {e}")
    
    def view_assignments(self):
        assignments = self.assignment_repo.get_all()
        if not assignments:
            print("No assignments found")
            return
        
        print(f"\n--- Assignments ({len(assignments)} total) ---")
        for assignment in assignments:
            status_icon = "✓" if assignment.status == AssignmentStatus.COMPLETED else "○"
            print(f"{status_icon} ID: {assignment.id} | {assignment.title}")
            print(f"   Due: {assignment.due_date.strftime('%Y-%m-%d')} | Priority: {assignment.priority}/10")
            print(f"   Status: {assignment.status.value} | Hours: {assignment.estimated_hours}")
            print("-" * 40)
    
    def mark_complete(self):
        try:
            assignment_id = int(input("Assignment ID to mark complete: ").strip())
            if self.assignment_repo.update_status(assignment_id, AssignmentStatus.COMPLETED):
                print("✓ Assignment marked as completed")
            else:
                print("Assignment not found")
        except ValueError:
            print("Invalid ID")
    
    def ml_analytics(self):
        assignments = self.assignment_repo.get_all()
        pending = [a for a in assignments if a.status != AssignmentStatus.COMPLETED]
        
        if not pending:
            print("No pending assignments for analysis")
            return
        
        print(f"\n--- ML Analytics ({len(pending)} pending assignments) ---")
        
        # Risk analysis
        print("\nRisk Analysis:")
        for assignment in pending:
            risk_level, risk_score = self.ml_service.predict_completion_risk(assignment)
            risk_icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}[risk_level.name]
            print(f"{risk_icon} {assignment.title}: {risk_level.value} (score: {risk_score:.2f})")
        
        # Work schedule
        print("\nRecommended Work Schedule:")
        schedule = self.ml_service.recommend_work_schedule(assignments)
        for i, item in enumerate(schedule, 1):
            assignment = item['assignment']
            hours = item['allocated_hours']
            risk_level = item['risk_level']
            print(f"{i}. {assignment.title}: {hours:.1f}h (risk: {risk_level.value})")
    
    def view_all_data(self):
        print("\n--- All Data Summary ---")
        
        notes = self.note_repo.get_all()
        assignments = self.assignment_repo.get_all()
        
        print(f"Notes: {len(notes)}")
        print(f"Assignments: {len(assignments)}")
        
        completed = len([a for a in assignments if a.status == AssignmentStatus.COMPLETED])
        pending = len([a for a in assignments if a.status != AssignmentStatus.COMPLETED])
        
        print(f"Completed assignments: {completed}")
        print(f"Pending assignments: {pending}")
        
        if pending > 0:
            total_hours = sum(a.estimated_hours for a in assignments if a.status != AssignmentStatus.COMPLETED)
            print(f"Total estimated work: {total_hours:.1f} hours")
    
    def run(self):
        print("Welcome to Deadline Tracker!")
        
        while True:
            try:
                self.display_menu()
                choice = input("Enter choice: ").strip()
                
                if choice == '1':
                    self.notes_management()
                elif choice == '2':
                    self.assignment_management()
                elif choice == '3':
                    self.ml_analytics()
                elif choice == '4':
                    self.view_all_data()
                elif choice == '0':
                    print("Goodbye!")
                    break
                else:
                    print("Invalid choice")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                print("An error occurred. Please try again.")

# Fix: Add to_dict methods to dataclasses
Note.to_dict = note_to_dict
Assignment.to_dict = assignment_to_dict

if __name__ == "__main__":
    app = DeadlineTrackerApp()
    app.run()
