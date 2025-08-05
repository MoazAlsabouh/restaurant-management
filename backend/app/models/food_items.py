from app.extensions import db
from app.models.food_category import FoodCategory

class FoodItems(db.Model):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    food_category_id = db.Column(db.Integer, db.ForeignKey('food_category.id'))
    food_category = db.relationship('FoodCategory', backref='food_items', lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return f"<FoodItems id={self.id}, name={self.name}>"
