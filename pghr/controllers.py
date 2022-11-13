from flask import render_template, redirect, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import current_app as app
from pghr.models import (
    User, user_schema, users_schema,
    Room, room_schema, rooms_schema,
    RoomBookings, room_booking_schema, room_bookings_schema,
    Mess, mess_schema, messes_schema,
    MessBookings, mess_booking_schema, mess_bookings_schema,
    Announcements, announcement_schema, announcement_schema,
    Ticket, ticket_schema, tickets_schema,
    TicketReplies, ticket_reply_schema, ticket_replies_schema
)
from .database import db
from functools import wraps

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    
class RoomForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=15)])
    size = StringField('size', validators=[InputRequired(), Length(min=1, max=2)])
    attached_bathroom = BooleanField('attached_bathroom')
    status = StringField('status', validators=[InputRequired(), Length(min=1, max=2)])
    price = StringField('price', validators=[InputRequired(), Length(min=1, max=5)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=120)])
    
class RoomBookingForm(FlaskForm):
    room_id = StringField('room_id', validators=[InputRequired(), Length(min=1, max=2)])

class MessForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=15)])
    size = StringField('size', validators=[InputRequired(), Length(min=1, max=2)])
    status = StringField('status', validators=[InputRequired(), Length(min=1, max=2)])
    price = StringField('price', validators=[InputRequired(), Length(min=1, max=5)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=120)])
    
class MessBookingForm(FlaskForm):
    mess_id = StringField('mess_id', validators=[InputRequired(), Length(min=1, max=2)])

class AnnouncementForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4, max=15)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=120)])
    
class TicketForm(FlaskForm):
    title = StringField('title', validators=[InputRequired(), Length(min=4, max=15)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=120)])
    
class TicketReplyForm(FlaskForm):
    ticket_id = StringField('ticket_id', validators=[InputRequired(), Length(min=1, max=2)])
    description = StringField('description', validators=[InputRequired(), Length(min=4, max=120)])
     
"""INDEX PAGE
/LANDING PAGE"""
@app.route('/')
def index():
    return render_template('index/index.html')

"""LOGIN PAGE
Parameters: username, password
Return Templates: login.html, index.html
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                # check if admin or user
                user = user_schema.dump(user)
                admin = user['admin']
                if admin:
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('dashboard'))
        return '<h1>Invalid username or password</h1>'
    else: 
        print("\n\n\n\n\n\n\n", form.errors)
    return render_template('index/login.html', form=form)
    
"""SIGNUP PAGE
Parameters: email, username, password, name, admin
Return Templates: signup.html, index.html
"""
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    print("\n\n\n\n\n\n\n Hello", form.validate_on_submit())
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        print("\n\n\n\n\n\n\n Hello")
        new_user = User(email=form.email.data, username=form.username.data, password=hashed_password, admin=False)
        print("\n\n\n\n\n\n\n Hello")
        db.session.add(new_user)
        db.session.commit()
        # return '<h1>New user has been created!</h1>'
        return redirect(url_for('login'))
    else:
        print("\n\n\n\n\n\n\n", form.errors)
    return render_template('index/signup.html', form=form)

"""LOGOUT PAGE
Parameters: None
Return Templates: index.html
"""
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

"""DASHBOARD PAGE - CUSTOMER
Parameters: None
Return Templates: dashboard.html
"""
@app.route('/dashboard')
@login_required
def dashboard():
    room_booked = RoomBookings.query.filter_by(user_id=current_user.id).first()
    mess_booked = MessBookings.query.filter_by(user_id=current_user.id).first()
    
    if room_booked:
        room = Room.query.filter_by(id=room_booked.room_id).first()
    else: 
        room = None
    if mess_booked:
        mess = Mess.query.filter_by(id=mess_booked.mess_id).first()
    else:
        mess = None
        
    return render_template('customer/dashboard.html', user=current_user, room=room, mess=mess, room_booked=room_booked, mess_booked=mess_booked)

"""TICKET PAGE - CUSTOMER
Parameters: None
Return Templates: ticket.html
"""
@app.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    form = TicketForm()
    if form.validate_on_submit():
        new_ticket = Ticket(title=form.title.data, description=form.description.data, user_id=current_user.id, status='pending')
        db.session.add(new_ticket)
        db.session.commit()
        return redirect(url_for('ticket'))
    else:
        print(form.errors)
    # get tickets and map it to the ticket reply
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    ticket_replies = TicketReplies.query.all()
    return render_template('customer/ticket.html', user=current_user, tickets=tickets, ticket_replies=ticket_replies, form=form)

@app.route('/ticket/<id>/delete')
@login_required
def ticket_delete(id):
    ticket_reply = TicketReplies.query.filter_by(ticket_id=id).first()
    if ticket_reply:
        db.session.delete(ticket_reply)
    ticket = Ticket.query.get(id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('ticket'))

"""ANNOUNCEMENT PAGE - CUSTOMER
Parameters: None
Return Templates: announcement.html
"""
@app.route('/announcement')
@login_required
def announcement():
    announcements = Announcements.query.all()
    return render_template('customer/announcement.html', user=current_user, announcements=announcements)

@app.route('/announcement/<id>/delete')
@login_required
def announcement_delete(id):
    announcement = Announcements.query.get(id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for('announcement'))

"""BOOKING PAGE - CUSTOMER
Parameters: None
Return Templates: booking.html
"""
@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    rooms = Room.query.all()
    messes = Mess.query.all()
    
    room_booked = RoomBookings.query.filter_by(user_id=current_user.id).first()
    mess_booked = MessBookings.query.filter_by(user_id=current_user.id).first()
    
    dont_show_room = False if not room_booked else True
    dont_show_mess = False if not mess_booked else True
    
    if room_booked:
        room = Room.query.filter_by(id=room_booked.room_id).first()
    else:
        room = None
    if mess_booked:
        mess = Mess.query.filter_by(id=mess_booked.mess_id).first()
    else:
        mess = None
    
    return render_template('customer/booking.html', user=current_user, rooms=rooms, messes=messes, room=room, mess=mess, room_booked=room_booked, mess_booked=mess_booked, dont_show_room=dont_show_room, dont_show_mess=dont_show_mess)
    
@app.route('/booking/<id>/room', methods=['POST'])
@login_required
def booking_room(id):
    room = Room.query.get(id)
    room_booked = RoomBookings.query.filter_by(user_id=current_user.id).first()
    if room_booked:
        return redirect(url_for('booking'))
    new_room_booking = RoomBookings(user_id=current_user.id, room_id=room.id, status='pending')
    db.session.add(new_room_booking)
    db.session.commit()
    return redirect(url_for('booking'))

@app.route('/booking/<id>/mess', methods=['POST'])
@login_required
def booking_mess(id):
    mess = Mess.query.get(id)
    mess_booked = MessBookings.query.filter_by(user_id=current_user.id).first()
    if mess_booked:
        return redirect(url_for('booking'))
    new_mess_booking = MessBookings(user_id=current_user.id, mess_id=mess.id, status='pending')
    db.session.add(new_mess_booking)
    db.session.commit()
    return redirect(url_for('booking'))

@app.route('/booking/room/delete', methods=['POST'])
@login_required
def booking_room_delete():
    room_booked = RoomBookings.query.filter_by(user_id=current_user.id).first()
    db.session.delete(room_booked)
    db.session.commit()
    return redirect(url_for('booking'))

@app.route('/booking/mess/delete', methods=['POST'])
@login_required
def booking_mess_delete():
    mess_booked = MessBookings.query.filter_by(user_id=current_user.id).first()
    db.session.delete(mess_booked)
    db.session.commit()
    return redirect(url_for('booking'))

"""ADMIN SECTION
"""

"""DASHBOARD PAGE - ADMIN
Parameters: None
Return Templates: dashboard.html
"""
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    return render_template('admin/dashboard.html', user=current_user)

"""TICKET PAGE - ADMIN
Parameters: None
Return Templates: ticket.html
"""
@app.route('/admin/ticket', methods=['GET', 'POST'])
@login_required
def admin_ticket():
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    form = TicketReplyForm()
    if form.validate_on_submit():
        ticket = Ticket.query.filter_by(id=form.ticket_id.data).first()
        ticket.status = 'closed'
        db.session.commit()
        
        new_ticket_reply = TicketReplies(description=form.description.data, ticket_id=form.ticket_id.data, user_id=current_user.id)

        db.session.add(new_ticket_reply)
        db.session.commit()
        return redirect(url_for('admin_ticket'))
    else:
        print("\n\n\n\n\n\n\n", form.errors)
    # get tickets and map it to the ticket reply
    tickets = Ticket.query.all()
    ticket_replies = TicketReplies.query.all()
    return render_template('admin/ticket.html', user=current_user, tickets=tickets, ticket_replies=ticket_replies, form=form)

@app.route('/admin/ticket/<id>/delete')
@login_required
def admin_ticket_delete(id):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # delete ticket and ticket replies
    ticket_reply= TicketReplies.query.filter_by(ticket_id=id).first()
    if ticket_reply:
        db.session.delete(ticket_reply)
    ticket = Ticket.query.get(id)
    db.session.delete(ticket)
    db.session.commit()
    return redirect(url_for('admin_ticket'))
 

"""ANNOUNCEMENT PAGE - ADMIN
Parameters: None
Return Templates: announcement.html
"""
@app.route('/admin/announcement', methods=['GET', 'POST'])
@login_required
def admin_announcement():
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    form = AnnouncementForm()
    if form.validate_on_submit():
        new_announcement = Announcements(title=form.title.data, description=form.description.data)
        db.session.add(new_announcement)
        db.session.commit()
        return redirect(url_for('admin_announcement'))
    else:
        print("\n\n\n\n\n\n\n", form.errors)
    announcements = Announcements.query.all()
    return render_template('admin/announcement.html', user=current_user, announcements=announcements, form=form)

@app.route('/admin/announcement/<id>/delete')
@login_required
def admin_announcement_delete(id):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    announcement = Announcements.query.get(id)
    db.session.delete(announcement)
    db.session.commit()
    return redirect(url_for('admin_announcement'))

"""BOOKING PAGE - ADMIN
Parameters: None
Return Templates: booking.html
"""
@app.route('/admin/booking', methods=['GET', 'POST'])
@login_required
def admin_booking():
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # query rooms with status=pending
    room_pending = RoomBookings.query.join(Room, RoomBookings.room_id==Room.id).join(User, RoomBookings.user_id==User.id).add_columns(Room.id, Room.name, Room.size, Room.attached_bathroom, Room.price, RoomBookings.id, RoomBookings.status, User.id, User.username).filter(RoomBookings.status=='pending').all()
    mess_pending = MessBookings.query.join(Mess, MessBookings.mess_id==Mess.id).join(User, MessBookings.user_id==User.id).add_columns(Mess.id, Mess.name, Mess.description, Mess.price, MessBookings.id, MessBookings.status, User.id, User.username).filter(MessBookings.status=='pending').all()
    
    # query rooms with status=approved
    room_approved = RoomBookings.query.join(Room, RoomBookings.room_id==Room.id).join(User, RoomBookings.user_id==User.id).add_columns(Room.id, Room.name, Room.size, Room.attached_bathroom, Room.price, RoomBookings.id, RoomBookings.status, User.id, User.username).filter(RoomBookings.status=='approved').all()
    mess_approved = MessBookings.query.join(Mess, MessBookings.mess_id==Mess.id).join(User, MessBookings.user_id==User.id).add_columns(Mess.id, Mess.name, Mess.description, Mess.price, MessBookings.id, MessBookings.status, User.id, User.username).filter(MessBookings.status=='approved').all()
    
    # query all rooms joined users on room bookings
    room_bookings = RoomBookings.query.join(Room, RoomBookings.room_id==Room.id).join(User, RoomBookings.user_id==User.id).add_columns(Room.id, Room.name, Room.size, Room.attached_bathroom, Room.price, RoomBookings.id, RoomBookings.status, User.id, User.username).all()
    mess_bookings = MessBookings.query.join(Mess, MessBookings.mess_id==Mess.id).join(User, MessBookings.user_id==User.id).add_columns(Mess.id, Mess.name, Mess.description, Mess.price, MessBookings.id, MessBookings.status, User.id, User.username).all()
    
    return render_template('admin/booking.html', user=current_user, room_pending=room_pending, mess_pending=mess_pending, room_approved=room_approved, mess_approved=mess_approved, room_bookings=room_bookings, mess_bookings=mess_bookings)
    
@app.route('/admin/booking/room/<username>/approve', methods=['POST'])
@login_required
def admin_booking_approve_room(username):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # get id 
    user = User.query.filter_by(username=username).first()
    user_id = user_schema.dump(user)['id']

    # get booking
    room_booking = RoomBookings.query.filter_by(user_id=user_id).first()
    room_booking.status = 'approved'
    db.session.commit()
    return redirect(url_for('admin_booking'))

@app.route('/admin/booking/room/<username>/reject', methods=['POST'])
@login_required
def admin_booking_reject_room(username):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # get id 
    user = User.query.filter_by(username=username).first()
    user_id = user_schema.dump(user)['id']

    # get booking
    room_booking = RoomBookings.query.filter_by(user_id=user_id).first()
    room_booking.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('admin_booking'))

@app.route('/admin/booking/mess/<username>/approve', methods=['POST'])
@login_required
def admin_booking_approve_mess(username):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # get id 
    user = User.query.filter_by(username=username).first()
    user_id = user_schema.dump(user)['id']

    # get booking
    mess_booking = MessBookings.query.filter_by(user_id=user_id).first()
    mess_booking.status = 'approved'
    db.session.commit()
    return redirect(url_for('admin_booking'))

@app.route('/admin/booking/mess/<username>/reject', methods=['POST'])
@login_required
def admin_booking_reject_mess(username):
    if not user_schema.dump(current_user)['admin']:
        return redirect(url_for('dashboard'))
    
    # get id 
    user = User.query.filter_by(username=username).first()
    user_id = user_schema.dump(user)['id']

    # get booking
    mess_booking = MessBookings.query.filter_by(user_id=user_id).first()
    mess_booking.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('admin_booking'))