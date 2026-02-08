from sqlalchemy.orm import Session
from database import SessionLocal
from models import SysTeacher

def add_teacher():
    db = SessionLocal()
    try:
        # Check if exists
        name = "潘卫华"
        existing = db.query(SysTeacher).filter(SysTeacher.name == name).first()
        
        if existing:
            print(f"Teacher {name} already exists with ID: {existing.id}")
            return existing.id
        
        # Create new
        new_teacher = SysTeacher(
            name=name, 
            title="副教授", 
            department="智能工程学院"
        )
        db.add(new_teacher)
        db.commit()
        db.refresh(new_teacher)
        
        print(f"Successfully created teacher {name} with ID: {new_teacher.id}")
        return new_teacher.id
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_teacher()
