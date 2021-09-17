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

    def create_user_infos(self, user_infos: models.UserInfos, db: Session):
        db_user_infos = models.UserInfos(user_id=user_infos.user_id, schooling=user_infos.schooling, institution=user_infos.institution)
        db.add(db_user_infos)
        db.commit()
        db.refresh(db_user_infos)
        return db_user_infos

    def create_recover(self, recover_dict: models.RecoverUser, db: Session):
        db_recover = models.RecoverUser(user_id= recover_dict['user_id'], token= recover_dict['token'], used=recover_dict['used'], subscription_date=recover_dict['subscription_date'])
        db.add(db_recover)
        db.commit()
        db.refresh(db_recover)
        return db_recover

    def get_user_by_email(self, email: str, db: Session):
        return db.query(models.User).filter(models.User.email == email).first()

    def get_user_by_id(self, id: str, db: Session):
        return db.query(models.User).filter(models.User.id == id).first()

    def get_user_infos_by_user_id(self, id: str, db: Session):
        return db.query(models.UserInfos).filter(models.UserInfos.user_id == id).first()

    def get_recover_by_id(self, id: str, db: Session):
        return db.query(models.RecoverUser).filter(models.RecoverUser.id == id).first()

    def auth_user(self, database_password: str, password: str):
        return hash_instance.check_password(password, database_password)

    def update_user(self, user_id: str, update_dict: dict, db: Session):
        db.query(models.User).filter(models.User.id == user_id).update(update_dict, synchronize_session=False)
        db.commit()
        return None





