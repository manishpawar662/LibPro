from flask import Flask, render_template, request, redirect, jsonify,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, MetaData, inspect
from datetime import datetime
import os
import json
import requests
app = Flask(__name__)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from requests.adapters import HTTPAdapter, Retry

app = Flask(__name__)
app.secret_key = "my_secret_key"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_uri = f'sqlite:///{os.path.join(BASE_DIR, "library.db")}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
#Models
class Books(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer, nullable=False,unique=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, nullable=False,default=100)

class Members(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    memberid = db.Column(db.String(10),  nullable=False,unique=True)
    name = db.Column(db.String(30), nullable=False)
    outstanding_debt = db.Column(db.Integer, nullable=False)

class Transactions(db.Model):
    sno = db.Column(db.Integer, primary_key=True,unique=True)
    Transactionid = db.Column(db.Integer,unique=True)
    bookid = db.Column(db.Integer, nullable=False)
    memberid = db.Column(db.Integer, nullable=False)
    date_issued = db.Column(db.DateTime, nullable=False,default=datetime.date)
    date_returned = db.Column(db.DateTime, nullable=True)
    rent_fee = db.Column(db.Integer, nullable=False)
    status=db.Column(db.String(20),nullable=False)

@app.route('/addrecord/<string:table>',methods=['GET','POST'])
def addrecord(table):
    record_class=globals().get(table.capitalize())
    if record_class is None:
        flash("Invalid Operation",'warning')
        return render_template('index.html')
    else:
        if f'{table}'=='transactions':
            allTransaction=Transactions.query.all()
            allbooks= Books.query.all()
            allmembers=Members.query.all()
            return render_template(f'add{table}.html',alltransaction=allTransaction,allbooks=allbooks,allmembers=allmembers)
        else:
            return render_template(f'add{table}.html')

#D-Delete
@app.route('/deleterecord/<string:table>/<int:sno>',methods=['GET','POST'])
def deleterecord(table,sno):
    record_class=globals().get(table.capitalize())
    record=record_class.query.filter_by(sno=sno).first()
    db.session.delete(record)
    db.session.commit()
    flash("1 record Deleted Successfully",'success')
    allrecords=record_class.query.all()
    return redirect(f'{table}')
#U-update
@app.route('/updaterecord/<string:table>/<int:sno>' or "/updaterecord",methods=['GET','POST'])
@app.route('/updaterecord/<string:table>', methods=['GET', 'POST'])
def updaterecord(table,sno):
    record_class=globals().get(table.capitalize())
    if sno!=None:
        if request.method=='POST':
            if table=="books":
                print("Book table")
                bookid=request.form['bookid']
                title=request.form['title']
                author=request.form['author']
                stock=request.form['stock']

                book= Books.query.filter_by(sno=sno).first()
                book.bookid=bookid
                book.title=title
                book.author=author
                book.stock=stock
                db.session.add(book)
                db.session.commit()
                flash("Book Updated successfully",'success')
            elif table=="members":
                print("Member table")
                memberid=request.form['memberid']
                name=request.form['name']
                outstanding_debt=request.form['outstanding_debt']
                
                member= Members.query.filter_by(sno=sno).first()
                member.memberid=memberid
                member.name=name
                member.outstanding_debt=outstanding_debt
                db.session.add(member)
                db.session.commit()
                flash("Member Updated successfully",'success')
            elif table=="transactions":
                print("Transaction table")
                Transactionid=request.form['transactionid']
                bookid=request.form['bookid']
                memberid=request.form['memberid']
                date_issued=request.form['date_issued']
                date_returned=request.form['date_returned']
                status=request.form['status']
                # print("before conversion",date_returned)
                date_issued = datetime.strptime(date_issued, '%Y-%m-%d')
                date_returned = datetime.strptime(date_returned, '%Y-%m-%d')
                # print("After conversion",date_returned)

                rent_fee=request.form['rent_fee']

                transaction= Transactions.query.filter_by(Transactionid=Transactionid).first()
                old_status=transaction.status
                transaction.Transactionid=Transactionid
                transaction.bookid=bookid
                transaction.memberid=memberid
                transaction.date_issued=date_issued
                transaction.date_returned=date_returned
                transaction.rent_fee=rent_fee
                transaction.status=status
                if(transaction.status!=old_status and transaction.status=="Pending"):
                    member= Members.query.filter_by(memberid=transaction.memberid).first()
                    member.outstanding_debt=str(int(member.outstanding_debt)+int(rent_fee))
                    
                    book= Books.query.filter_by(bookid=transaction.bookid).first()
                    book.stock-=1

                elif(transaction.status!=old_status and transaction.status=="Paid"):
                    member= Members.query.filter_by(memberid=transaction.memberid).first()
                    member.outstanding_debt=str(int(member.outstanding_debt)-int(rent_fee))
                    
                    book= Books.query.filter_by(bookid=transaction.bookid).first()
                    book.stock+=1
                else:
                    pass
                db.session.add(transaction)
                db.session.commit()
                flash("Transaction Updated successfully",'success')
            else:
                flash("Something went wrong",'error')
            allrecords=record_class.query.all()
            return render_template(f'{table}.html',allrecords=allrecords)
    #If there is no sno then update page is requested
    if record_class is None:
        flash("Invalid operation",'warning')
        return redirect('/')
    else:
        record = record_class.query.filter_by(sno=sno).first()
        if record is None:
            flash('Invalid record','warning')
            return redirect('/')
        else:
            inspecter= inspect(record)
            if hasattr(record, "date_issued")  and hasattr(record, "date_returned") :
                record.date_issued=record.date_issued.date()
                record.date_returned=record.date_returned.date()
            return render_template(f'update{table}.html', record=record)
#search
@app.route('/search/<string:table>',methods=['GET','POST'])
def search(table):
    if request.method=="POST":
        search=request.form['searchitem'] 
        table_class = globals().get(table.capitalize())
        
        if table_class is not None:
            # table_class.query.filter_by().distinct().all()
            inspector=inspect(table_class)
            allcolumns=table_class.__table__.columns
            filter_condition=[column.contains(search) for column in allcolumns]
            allconditions=or_(*filter_condition)
            search_records = table_class.query.filter(allconditions).distinct().all()
        return render_template(f'{table}.html',allrecords=search_records)
    return redirect(f'/{table}')

#R-Read and create
@app.route('/<string:table>',methods=['GET','POST'])
def view(table):
    record_class=globals().get(table.capitalize())
    # inspector=inspect(record_class)
    if record_class is None:
        flash("Invalid Operation",'warning')
        return redirect('/')
        # print(f"Table class for '{name.capitalize()}' not found.")
    else:
        if request.method=="POST":
            if f'{table}'== "books":
                books(request)
            elif f'{table}'== "members":
                members(request)
            elif f'{table}'== "transactions":
                transactions(request)
            else:
                flash("Invalid Operation",'info')
        allrecords=record_class.query.all()
        return render_template(f'{table}.html',allrecords=allrecords)

def books(request):
    if request.method=="POST":
        bookid=request.form['bookid']
        title=request.form['title']
        author=request.form['author']
        stock=request.form['stock']
        books =  Books(bookid=bookid,title=title,author=author,stock=stock)
        db.session.add(books)
        db.session.commit()
        allbooks= Books.query.all()
    return render_template('books.html',allrecords=allbooks)

def transactions(request):
    if request.method=="POST":
        Transactionid=request.form['transactionid']
        bookid=request.form['bookid']
        memberid=request.form['memberid']
        date_issued=request.form['date_issued']
        date_returned=request.form['date_returned']
        rent_fee=request.form['rent_fee']
        status=request.form['status']

        date_issued = datetime.strptime(date_issued, '%Y-%m-%d')
        date_returned = datetime.strptime(date_returned, '%Y-%m-%d')
        new_transaction= Transactions(Transactionid=Transactionid,bookid=bookid,memberid=memberid,date_issued=date_issued,date_returned=date_returned,rent_fee=rent_fee,status=status)
        
        member = Members.query.filter_by(memberid=memberid).first()
        book = Books.query.filter_by(bookid=bookid).first()
        if book and member:
            if((int(member.outstanding_debt)==500) or (int(member.outstanding_debt)+int(rent_fee)>500)):
                flash('Member cannot have debt more than 500','warning')
            elif book.stock<=0:
                flash('Book not avaliable in stock','warning')
            else:
                if status=="Pending":
                    member.outstanding_debt=str(int(member.outstanding_debt)+int(rent_fee))
                    book.stock-=1
                    db.session.add(member)
                    db.session.commit()
                else:
                    book.stock+=1
                db.session.add(new_transaction)
                db.session.commit()
        else:
            flash("Invalid BookID or MemberID",'warning')
    allTransaction=Transactions.query.all()
    return render_template('transactions.html',allrecords=allTransaction)

def members(request):
    if request.method=="POST":
        memberid=request.form['memberid']
        name=request.form['name']
        outstanding_debt=request.form['outstanding_debt']
        new_member= Members(memberid=memberid,name=name,outstanding_debt=outstanding_debt)
        db.session.add(new_member)
        db.session.commit()
    allmembers=Members.query.all()
    return render_template('members.html',allrecords=allmembers)

#empty
@app.route('/empty/<string:table>',methods=['GET','POST'])
def empty(table):
    inspecter=inspect(db.engine)
    if inspecter.has_table(table):
        table_class = globals().get(table.capitalize())
        
        if table_class is not None:
            
            print(table_class)
            if table=='transactions':
                print("Its transaction")
                members=Members.query.all()
                for member in members:
                    member.outstanding_debt=0
                    db.session.add(member)
                    db.session.commit()
                transaction=Transactions.query.all()
                for record in transaction:
                    book=Books.query.filter_by(bookid=record.bookid).first()
                    book.stock+=1     
            table_class.query.delete()
            db.session.commit()
            flash(f"All records in the '{table}' table have been deleted.",'info')
        else:
            flash(f"Table class for '{table}' not found.",'error')
            redirect('/')
    return redirect(f'/{table}')

@app.route('/',methods=['GET','POST'])
def Home():
    return render_template('index.html')

@app.route('/importbooks',methods=['GET','POST'])
def importbooks(): 
    response=requests.get('https://frappe.io/api/method/frappe-library?page=2&title=and')
    retry = Retry(connect=3, backoff_factor=0.5)
    data=response.json()
    books=data.get("message",[])
    count=0
    for book in books:
        bookid=book.get('bookID')
        title=book.get('title')
        author=book.get('authors')
        print(count)
        if(Books.query.filter_by(bookid=bookid).first()):
            pass
        else:
            books =  Books(bookid=bookid,title=title,author=author)
            db.session.add(books)
            db.session.commit()
            count+=1
            
    if(count>0):
        flash(f'{count} Book(s) Imported Successfully','success')
    else:
        flash("Book(s) Already Exist",'warning')
    allbooks= Books.query.all()
    return redirect('/books')

if __name__ == '__main__':
    app.run(debug=True,port=8000) 