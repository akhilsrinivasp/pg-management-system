from flask_login import UserMixin
from .database import db, ma
from sqlalchemy.sql import func
from sqlalchemy.sql import func 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    admin = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def check_password(self, password):
        return self.password == password
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'created_at', 'updated_at', 'admin')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    size = db.Column(db.Integer, unique=False, nullable=False)
    attached_bathroom = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    status = db.Column(db.String(80), unique=False, nullable=False) # A, NA
    price = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Rooms %r>' % self.name
    
class RoomSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'size', 'attached_bathroom', 'status', 'price', 'description')
        
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)

class RoomBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    room = db.relationship('Room', backref=db.backref('room', lazy=True))
    status = db.Column(db.String(80), unique=False, nullable=False) # pending, approved, cancelled
    check_in = db.Column(db.DateTime(timezone=True), server_default=func.now())
    check_out = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return '<Bookings %r>' % self.user_id

class RoomBookingsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'room_id', 'status', 'check_in', 'check_out')

room_booking_schema = RoomBookingsSchema()
room_bookings_schema = RoomBookingsSchema(many=True)

class Mess(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    status = db.Column(db.String(80), unique=False, nullable=False) # A, NA - Available, Not Available
    price = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Mess %r>' % self.name
    
class MessSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'status', 'price')
        
mess_schema = MessSchema()
messes_schema = MessSchema(many=True)

class MessBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    mess_id = db.Column(db.Integer, db.ForeignKey('mess.id'), nullable=False)
    mess = db.relationship('Mess', backref=db.backref('mess', lazy=True))
    status = db.Column(db.String(80), unique=False, nullable=False) # pending, approved, cancelled
    check_in = db.Column(db.DateTime(timezone=True), server_default=func.now())
    check_out = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return '<Bookings %r>' % self.user_id
    
class MessBookingsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'mess_id', 'status', 'check_in', 'check_out')

mess_booking_schema = MessBookingsSchema()
mess_bookings_schema = MessBookingsSchema(many=True)

class Announcements (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return '<Announcements %r>' % self.name
    
class AnnouncementsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'created_at')

announcement_schema = AnnouncementsSchema()
announcements_schema = AnnouncementsSchema(many=True)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tickets', lazy=True))
    title = db.Column(db.String(80), unique=False, nullable=False)
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    status = db.Column(db.String(80), unique=False, nullable=False) # open, closed
    
    def __repr__(self):
        return '<Ticket %r>' % self.user_id
    
class TicketSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'title', 'description', 'created_at', 'status')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

class TicketReplies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    ticket = db.relationship('Ticket', backref=db.backref('replies', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('replies', lazy=True))
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return '<TicketReplies %r>' % self.ticket_id
    
class TicketRepliesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ticket_id', 'user_id', 'description', 'created_at')
    
ticket_reply_schema = TicketRepliesSchema()
ticket_replies_schema = TicketRepliesSchema(many=True)


