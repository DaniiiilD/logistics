from sqlalchemy.orm import Session

class BaseRepository:
    
    model = None
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, id):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def delete(self, id):
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)