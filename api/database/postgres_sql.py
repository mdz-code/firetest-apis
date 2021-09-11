from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import update
from . import schemas, models
from ..config.hashed import Hash

hash_instance = Hash()

class PostgresSQL:

    def create_user(self, user: models.User, db: Session):
        raw_password = user.hashed_password
        hashed_password = hash_instance.get_hashed_password(raw_password)

        
        db_user = models.User(email=user.email, complete_name=user.complete_name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user_by_email(self, email: str, db: Session):
        return db.query(models.User).filter(models.User.email == email).first()

    def get_user_by_id(self, id: str, db: Session):
        return db.query(models.User).filter(models.User.id == id).first()

    def auth_user(self, database_password: str, password: str):
        return hash_instance.check_password(password, database_password)

    def update_user(self, user_id: str, update_dict: dict, db: Session):
        db.query(models.User).filter(models.User.id == user_id).update(update_dict, synchronize_session=False)
        db.commit()
        return None





