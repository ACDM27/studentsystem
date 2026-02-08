from sqlalchemy.orm import Session
from database import SessionLocal
from models import SysTeacher

def check_teachers():
    db = SessionLocal()
    try:
        teachers = db.query(SysTeacher).all()
        print(f"Found {len(teachers)} teachers.")
        for t in teachers:
            print(f"ID: {t.id}, Name: {t.name}, Dept: {t.department}")
            
        if not teachers:
            print("No teachers found! Needed for achievement creation.")
            # Create a default teacher
            default_teacher = SysTeacher(name="默认导师", title="讲师", department="计算机学院")
            db.add(default_teacher)
            db.commit()
            print(f"Created default teacher with ID: {default_teacher.id}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_teachers()
