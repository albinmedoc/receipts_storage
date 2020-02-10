from sqlalchemy import Column, Integer, String, Float, ForeignKey, func, select
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from receipts_storage.app import db, login
from .role import Role

user_roles = db.Table("user_roles",
    db.Column("user_id", db.Integer(), db.ForeignKey("person.id", ondelete="CASCADE")),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id", ondelete="CASCADE"))
)

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    roles = db.relationship("Role", secondary=user_roles, backref="users")

    def has_roles(self, *requirements):
        role_names = [role.name for role in self.roles]
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False                    # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if not role_name in role_names:
                    return False                    # role_name requirement failed: return False

        # All requirements have been met: return True
        return True
    
    def add_role(self, role):
        if(role not in [(role.name) for role in self.roles]):
            role_object = Role.query.filter_by(name=role).first()
            if(role_object is None):
                role_object = Role(name=role)
            self.roles.append(role_object)
            db.session.commit()