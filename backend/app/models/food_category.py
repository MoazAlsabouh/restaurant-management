from app.extensions import db

class FoodCategory(db.Model):
    __tablename__ = 'food_category'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f"<FoodItems id={self.id}, type={self.type}>"
