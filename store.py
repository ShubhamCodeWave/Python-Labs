import mysql.connector
import datetime
import json
import csv
import sys

SESSION_FILE = "session.json"
LOG_FILE = "logs.txt"
APP_VERSION = "StoreMate v1.0"

def log(m):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.datetime.now()} | {m}\n")

def db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="shubham@123",
        database="storemate"
    )

def save_session(shop_id):
    with open(SESSION_FILE, "w") as f:
        json.dump({"shop_id": shop_id}, f)

def load_session():
    try:
        with open(SESSION_FILE) as f:
            return json.load(f)["shop_id"]
    except:
        return None

def clear_session():
    with open(SESSION_FILE, "w") as f:
        f.write("")

def banner():
    print("\n" + "="*70)
    print("STOREMATE – ADVANCED SHOP MANAGEMENT SYSTEM")
    print("Developer: Shubham Sharma")
    print(APP_VERSION)
    print("="*70)

def welcome():
    banner()
    print("1. Login to existing shop")
    print("2. Register new shop")
    print("3. Forgot password")
    print("4. About StoreMate")
    print("5. Exit")

def register():
    con = db()
    cur = con.cursor()
    print("\nRegistration started. Please enter shop details carefully.")
    shop = input("Shop name: ").strip()
    owner = input("Owner full name: ").strip()
    email = input("Email address: ").strip()
    pwd = input("Password: ").strip()
    phone = input("Phone number: ").strip()
    address = input("Shop address: ").strip()
    if not shop or not owner or not email or not pwd:
        print("Registration failed. Mandatory fields missing.")
        return
    try:
        cur.execute(
            "INSERT INTO register (shop_name,owner_name,email,password,phone,address) VALUES (%s,%s,%s,%s,%s,%s)",
            (shop, owner, email, pwd, phone, address)
        )
        con.commit()
        print("Registration successful. You can now login.")
        log("Shop registered")
    except:
        print("Registration failed. Email already exists.")
    con.close()

def login():
    con = db()
    cur = con.cursor(dictionary=True)
    print("\nLogin started.")
    email = input("Email: ").strip()
    pwd = input("Password: ").strip()
    cur.execute("SELECT * FROM register WHERE email=%s AND password=%s", (email, pwd))
    r = cur.fetchone()
    con.close()
    if r:
        save_session(r["shop_id"])
        print(f"Login successful. Welcome {r['shop_name']}.")
        log("Login success")
        dashboard(r["shop_id"])
    else:
        print("Login failed. Invalid email or password.")
        log("Login failed")

def forgot_password():
    con = db()
    cur = con.cursor(dictionary=True)
    print("\nPassword recovery started.")
    email = input("Registered email: ").strip()
    phone = input("Registered phone: ").strip()
    cur.execute("SELECT * FROM register WHERE email=%s AND phone=%s", (email, phone))
    r = cur.fetchone()
    if r:
        new = input("Enter new password: ").strip()
        cur.execute("UPDATE register SET password=%s WHERE shop_id=%s", (new, r["shop_id"]))
        con.commit()
        print("Password updated successfully.")
        log("Password reset")
    else:
        print("Details did not match. Password not changed.")
    con.close()

def dashboard(shop_id):
    while True:
        print("\nDashboard opened. Choose an option.")
        print("1. Add product")
        print("2. View products")
        print("3. Create bill")
        print("4. Sales report")
        print("5. Export sales to Excel")
        print("6. View / Edit profile")
        print("7. Change password")
        print("8. Logout")
        ch = input("Enter choice: ").strip()
        if ch == "1":
            add_product(shop_id)
        elif ch == "2":
            view_products(shop_id)
        elif ch == "3":
            billing(shop_id)
        elif ch == "4":
            sales_report(shop_id)
        elif ch == "5":
            export_sales(shop_id)
        elif ch == "6":
            profile(shop_id)
        elif ch == "7":
            change_password(shop_id)
        elif ch == "8":
            clear_session()
            print("Logout successful.")
            log("Logout")
            break
        else:
            print("Invalid option. Please try again.")

def add_product(shop_id):
    con = db()
    cur = con.cursor()
    print("\nAdding new product.")
    name = input("Product name: ").strip()
    try:
        price = float(input("Price: "))
        qty = int(input("Quantity: "))
    except:
        print("Invalid numeric input.")
        return
    if price <= 0 or qty < 0:
        print("Invalid price or quantity.")
        return
    cur.execute(
        "INSERT INTO products (shop_id,product_name,price,quantity) VALUES (%s,%s,%s,%s)",
        (shop_id, name, price, qty)
    )
    con.commit()
    con.close()
    print("Product added successfully.")
    log(f"Product added: {name}")

def view_products(shop_id):
    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM products WHERE shop_id=%s", (shop_id,))
    rows = cur.fetchall()
    if not rows:
        print("No products available.")
        return
    print("\nAvailable products:")
    for r in rows:
        status = "LOW STOCK" if r["quantity"] <= r["min_stock"] else "OK"
        print(f"{r['product_name']} | Price {r['price']} | Quantity {r['quantity']} | {status}")
    con.close()

def billing(shop_id):
    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT shop_name,address FROM register WHERE shop_id=%s", (shop_id,))
    shop = cur.fetchone()
    cname = input("Customer full name: ").strip()
    cphone = input("Customer phone: ").strip()
    try:
        items = int(input("How many different items customer is buying: "))
    except:
        print("Invalid number.")
        return
    if items <= 0:
        print("Billing cancelled. No items selected.")
        return
    cur.execute("INSERT INTO sales (shop_id,total_amount) VALUES (%s,%s)", (shop_id, 0))
    con.commit()
    bill_id = cur.lastrowid
    total = 0
    for _ in range(items):
        view_products(shop_id)
        pname = input("Enter product name exactly as shown: ").strip()
        try:
            qty = int(input("Enter quantity: "))
        except:
            print("Invalid quantity.")
            continue
        cur.execute("SELECT * FROM products WHERE shop_id=%s AND product_name=%s", (shop_id, pname))
        p = cur.fetchone()
        if not p:
            print("Product not found.")
            continue
        if qty <= 0 or qty > p["quantity"]:
            print("Requested quantity not available.")
            continue
        amt = qty * p["price"]
        total += amt
        cur.execute(
            "INSERT INTO bill_items (bill_id,product_name,quantity,price) VALUES (%s,%s,%s,%s)",
            (bill_id, pname, qty, p["price"])
        )
        cur.execute("UPDATE products SET quantity=quantity-%s WHERE product_id=%s", (qty, p["product_id"]))
        cur.execute("DELETE FROM products WHERE quantity<=0")
        con.commit()
    cur.execute("UPDATE sales SET total_amount=%s WHERE bill_id=%s", (total, bill_id))
    con.commit()
    print("\nBill generated successfully.")
    print(shop["shop_name"])
    print(shop["address"])
    print(f"Customer: {cname} {cphone}")
    print(f"Bill number: {bill_id}")
    print(f"Total payable amount: {total}")
    log(f"Bill created {bill_id}")
    con.close()

def sales_report(shop_id):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*),SUM(total_amount) FROM sales WHERE shop_id=%s", (shop_id,))
    c, s = cur.fetchone()
    print(f"Total bills generated: {c}")
    print(f"Total sales amount: {s if s else 0}")
    con.close()

def export_sales(shop_id):
    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM sales WHERE shop_id=%s", (shop_id,))
    rows = cur.fetchall()
    if not rows:
        print("No sales data to export.")
        return
    with open("sales_report.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(rows[0].keys())
        for r in rows:
            w.writerow(r.values())
    print("Sales exported successfully to sales_report.csv.")
    log("Sales exported")
    con.close()

def profile(shop_id):
    con = db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM register WHERE shop_id=%s", (shop_id,))
    r = cur.fetchone()
    print("\nProfile details:")
    print(r)
    if input("Do you want to edit profile? (y/n): ").lower() == "y":
        phone = input("New phone: ").strip()
        address = input("New address: ").strip()
        cur.execute("UPDATE register SET phone=%s,address=%s WHERE shop_id=%s", (phone, address, shop_id))
        con.commit()
        print("Profile updated.")
        log("Profile updated")
    con.close()

def change_password(shop_id):
    con = db()
    cur = con.cursor()
    old = input("Enter old password: ").strip()
    cur.execute("SELECT * FROM register WHERE shop_id=%s AND password=%s", (shop_id, old))
    if cur.fetchone():
        new = input("Enter new password: ").strip()
        cur.execute("UPDATE register SET password=%s WHERE shop_id=%s", (new, shop_id))
        con.commit()
        print("Password changed successfully.")
        log("Password changed")
    else:
        print("Incorrect old password.")
    con.close()

def about():
    banner()
    print("StoreMate is a CLI based shop management system.")
    print("Designed for small retail businesses.")
    print("Built using Python and MySQL.")
    print("Accessible for visually impaired users.")
    print("Thank you for using StoreMate.")

def main():
    sid = load_session()
    if sid:
        dashboard(sid)
    while True:
        welcome()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            login()
        elif ch == "2":
            register()
        elif ch == "3":
            forgot_password()
        elif ch == "4":
            about()
        elif ch == "5":
            sys.exit()

main()
