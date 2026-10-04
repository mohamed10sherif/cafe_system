import tkinter as tk 
from tkinter import ttk , messagebox 
from cafe_system import CafeManagementSystem , Order , Coupon 

BURGUNDY = "#800020"
CREAM = "#F5E6D3"
DARK_BURGUNDY = "#5C0015"
GOLD = "#D4AF37"

window = tk.Tk()
cafe = CafeManagementSystem()
window.title("Shefo Cafe ")
window.geometry("800x600")
window.configure(bg=BURGUNDY)

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview",
    background=CREAM,
    fieldbackground=CREAM,
    foreground=DARK_BURGUNDY,
    rowheight=32,
    font=("Arial", 11)
)
style.configure(
    "Treeview.Heading",
    background=DARK_BURGUNDY,
    foreground=CREAM,
    font=("Arial", 11, "bold"),
)
style.map("Treeview.Heading", background=[("active", BURGUNDY)])
style.map("Treeview", background=[("selected", GOLD)], foreground=[("selected", DARK_BURGUNDY)])


def clear_window() : 
    for widget in window.winfo_children() : 
        widget.destroy() 

def title(text):
    tk.Label(window, text=text, font=("Arial", 26, "bold"),
             bg=BURGUNDY, fg=CREAM).pack(pady=15)

def button(parent, text, command, bg=CREAM, width=16, fg=DARK_BURGUNDY, height=1):
    return tk.Button(parent, text=text, font=("Arial", 12, "bold"), bg=bg,
                     fg=fg, width=width, height=height, command=command)

def create_table(parent, columns):
    frame = tk.Frame(parent, bg=BURGUNDY)
    frame.pack(fill="both", expand=True, padx=30)
    table = ttk.Treeview(frame, columns=list(columns), show="headings", selectmode="browse")
    for name, (text, width) in columns.items():
        table.heading(name, text=text)
        table.column(name, width=width, anchor="center")
    table.tag_configure("low", background="#FFE0A3")
    table.tag_configure("out", background="#F4B6B6", foreground="#8B0000")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return table

PRODUCT_COLUMNS = {"id": ("ID", 50), "name": ("Name", 180), "price": ("Price", 90),
                   "stock": ("Stock", 70), "category": ("Category", 140), "status": ("Status", 120)}

def fill_products_table(table, products):
    table.delete(*table.get_children())
    for product in products:
        status = product.get_stock_status()
        tag = {"Out of Stock": "out", "Low Stock": "low"}.get(status, "")
        table.insert("", "end", tags=(tag,), values=(
            product.ID, product.name, f"{product.price} EGP",
            product.stock, product.category, status or "Available"))
        
def selected_product_id(table):
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a product first")
        return None
    return int(table.item(selected[0], "values")[0])

def read_quantity(spinbox):
    try:
        quantity = int(spinbox.get())
    except ValueError:
        messagebox.showwarning("Invalid Quantity", "Please enter a whole number")
        return None
    if quantity <= 0:
        messagebox.showwarning("Invalid Quantity", "Quantity must be greater than 0")
        return None
    return quantity

def show_text_screen(heading, text, width):
    clear_window()
    title(heading)
    box = tk.Text(window, width=width, height=22, font=("Courier New", 11),
                  bg=CREAM, fg=DARK_BURGUNDY, padx=15, pady=10)
    box.insert("1.0", text)
    box.config(state="disabled")
    box.pack()
    button(window, "← Back to Menu", show_main_menu, width=18).pack(pady=15)


def show_login_screen():
    clear_window()
    title_label = tk.Label(
        window,
        text="WELCOME TO SHEFO CAFE" , 
        font=("Arial" , 28 , "bold"),
        bg=BURGUNDY,
        fg=CREAM )
    title_label.pack(pady=40)

    login_frame = tk.Frame(window , bg=CREAM, padx=30,pady=30 )
    login_frame.pack()

    username_label = tk.Label(
        login_frame,
        text="Username",
        font=("Arial" , 12 , "bold"), 
        bg=CREAM , 
        fg=DARK_BURGUNDY )
    username_label.grid(row=0, column=0, padx=10, pady=10)

    username_entry = tk.Entry(
        login_frame,
        font=("Arial", 12),
        width=25 )
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    password_label = tk.Label(
        login_frame,
        text="Password",
        font=("Arial", 12, "bold"),
        bg=CREAM,
        fg=DARK_BURGUNDY )
    password_label.grid(row=1, column=0, padx=10, pady=10)

    password_entry = tk.Entry(
        login_frame,
        font=("Arial", 12),
        width=25,
        show="*" )
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    def login() : 
        username = username_entry.get()
        password = password_entry.get() 
        result = cafe.login(username , password)

        if result : 
            show_main_menu()
        else :
            messagebox.showerror("Login Failed , Invalid username or password")
            password_entry.delete(0,tk.END)


    password_entry.bind("<Return>", lambda event: login())
    button(login_frame, "LOGIN", login, DARK_BURGUNDY, fg=CREAM).grid(row=2, column=0, columnspan=2, pady=20)

def show_products_screen() : 
    clear_window() 
    title("Products")
    table = create_table(window, PRODUCT_COLUMNS)
    fill_products_table(table, cafe.products)
    button(window, "← Back to Menu", show_main_menu, width=18).pack(pady=20)

def show_order_screen():
    clear_window()
    title("Search & Order")
 
    search_frame = tk.Frame(window, bg=BURGUNDY)
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", font=("Arial", 12, "bold"),
             bg=BURGUNDY, fg=CREAM).pack(side="left", padx=5)
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, font=("Arial", 12),
             width=30).pack(side="left", padx=5)

    table = create_table(window, PRODUCT_COLUMNS)
 
    def refresh_table(*args):
        text = search_var.get().strip()
        fill_products_table(table, [p for p in cafe.products if p.search_product(text)])
 
    refresh_table()
    search_var.trace_add("write", refresh_table)
 
    bottom = tk.Frame(window, bg=BURGUNDY)
    bottom.pack(pady=15)
    tk.Label(bottom, text="Quantity:", font=("Arial", 12, "bold"),
             bg=BURGUNDY, fg=CREAM).grid(row=0, column=0, padx=5)
    spin = tk.Spinbox(bottom, from_=1, to=50, width=5, font=("Arial", 12))
    spin.grid(row=0, column=1, padx=5)
 
    def add_to_cart():
        product_id = selected_product_id(table)
        if product_id is None:
            return
        quantity = read_quantity(spin)
        if quantity is None:
            return
        product = cafe.find_product_by_ID(product_id)
        if quantity > product.stock:
            messagebox.showwarning("Not Enough Stock", f"Only {product.stock} left of {product.name}")
            return
        cafe.cart.add_item(product, quantity)
        messagebox.showinfo("Added", f"{quantity} x {product.name} added to cart")
        refresh_table()
        spin.delete(0, tk.END)
        spin.insert(0, "1")
 
    button(bottom, "Add to Cart", add_to_cart, GOLD).grid(row=0, column=2, padx=15)
    button(bottom, "View Cart →", show_cart_screen, width=12).grid(row=0, column=3, padx=5)
    button(bottom, "← Back", show_main_menu, width=8).grid(row=0, column=4, padx=5)

def show_cart_screen():
    clear_window()
    title("Your Cart")
    table = create_table(window, {"id": ("ID", 50), "name": ("Name", 200), "price": ("Price", 100),
                                  "qty": ("Qty", 70), "subtotal": ("Subtotal", 120)})
    total_var = tk.StringVar()
 
    def refresh():
        table.delete(*table.get_children())
        for item in cafe.cart.items:
            table.insert("", "end", values=(
                item.product.ID, item.product.name, f"{item.product.price} EGP",
                item.quantity, f"{item.get_Subtotal():.2f} EGP"))
        total_var.set(f"Subtotal: {cafe.cart.calculate_subtotal():.2f} EGP")
 
    refresh()
    tk.Label(window, textvariable=total_var, font=("Arial", 14, "bold"),
             bg=BURGUNDY, fg=GOLD).pack(pady=5)
 
    bar = tk.Frame(window, bg=BURGUNDY)
    bar.pack(pady=10)
    tk.Label(bar, text="Qty to remove:", font=("Arial", 12, "bold"),
             bg=BURGUNDY, fg=CREAM).grid(row=0, column=0, padx=5)
    spin = tk.Spinbox(bar, from_=1, to=50, width=5, font=("Arial", 12))
    spin.grid(row=0, column=1, padx=5)
 
    def remove():
        product_id = selected_product_id(table)
        if product_id is None:
            return
        quantity = read_quantity(spin)
        if quantity is None:
            return
        if not cafe.cart.remove_item(product_id, quantity):
            messagebox.showwarning("Cannot Remove", "You can't remove more than what's in the cart")
        refresh()
 
    button(bar, "Remove", remove, width=10).grid(row=0, column=2, padx=10)
    button(bar, "Checkout", show_checkout_screen, GOLD, width=10).grid(row=0, column=3, padx=5)
    button(bar, "← Back", show_main_menu, width=8).grid(row=0, column=4, padx=5)

def show_checkout_screen():
    if cafe.cart.is_empty():
        messagebox.showwarning("Empty Cart", "Your cart is empty")
        return
    clear_window()
    title("Checkout")
 
    order = Order(cafe.order_number, cafe.cart)
    order.calculate_auto_discount()
    order.calculate_final_total()
 
    frame = tk.Frame(window, bg=CREAM, padx=30, pady=20)
    frame.pack()
    summary_var = tk.StringVar()
 
    def update_summary():
        summary_var.set(
            f"Subtotal          : {order.subtotal:.2f} EGP\n"
            f"Auto Discount     : {order.auto_discount * 100:.0f}%\n"
            f"Coupon Discount   : {order.coupon_discount * 100:.0f}%\n"
            f"Discounted Amount : {order.discounted_amoount:.2f} EGP\n"
            f"Service Charge    : {order.service_charge:.2f} EGP\n"
            f"FINAL TOTAL       : {order.final_total:.2f} EGP")
 
    update_summary()
    tk.Label(frame, textvariable=summary_var, font=("Courier New", 12, "bold"),
             bg=CREAM, fg=DARK_BURGUNDY, justify="left").grid(row=0, column=0, columnspan=3, pady=10)
 
    tk.Label(frame, text="Coupon:", font=("Arial", 12, "bold"),
             bg=CREAM, fg=DARK_BURGUNDY).grid(row=1, column=0, pady=8)
    coupon_entry = tk.Entry(frame, font=("Arial", 12), width=18)
    coupon_entry.grid(row=1, column=1, pady=8)
 
    def apply_coupon():
        code = coupon_entry.get().strip().upper()
        if code and not Coupon.is_valid(code):
            messagebox.showwarning("Invalid Coupon", "This coupon code is not valid")
            code = ""
        order.apply_coupon_discount(code)
        order.calculate_final_total()
        update_summary()
 
    button(frame, "Apply", apply_coupon, width=8).grid(row=1, column=2, padx=5)
 
    payment_var = tk.StringVar(value="Cash")
    pay_frame = tk.Frame(frame, bg=CREAM)
    pay_frame.grid(row=2, column=0, columnspan=3, pady=8)
 
    def toggle_cash():
        received_entry.config(state="normal" if payment_var.get() == "Cash" else "disabled")
 
    for method in ("Cash", "Card", "Mobile Wallet"):
        tk.Radiobutton(pay_frame, text=method, value=method, variable=payment_var,
                       command=toggle_cash, font=("Arial", 12), bg=CREAM,
                       fg=DARK_BURGUNDY).pack(side="left", padx=10)
 
    tk.Label(frame, text="Received:", font=("Arial", 12, "bold"),
             bg=CREAM, fg=DARK_BURGUNDY).grid(row=3, column=0, pady=8)
    received_entry = tk.Entry(frame, font=("Arial", 12), width=18)
    received_entry.grid(row=3, column=1, pady=8)
 
    def confirm():
        method = payment_var.get()
        order.set_payment_method(method)
        if method == "Cash":
            try:
                received = float(received_entry.get())
            except ValueError:
                messagebox.showwarning("Invalid Amount", "Please enter a valid received amount")
                return
            if not order.process_cash(received):
                messagebox.showwarning("Not Enough", f"Received amount is less than {order.final_total:.2f} EGP")
                return
        cafe.complete_order(order)
        show_receipt_screen(order)
 
    button(frame, "Confirm Payment", confirm, GOLD, width=20).grid(row=4, column=0, columnspan=3, pady=12)
    button(frame, "← Back to Cart", show_cart_screen, width=20).grid(row=5, column=0, columnspan=3)


def show_receipt_screen(order):
    line = "-" * 44
 
    def row(label, value):
        return f"{label:<26}{value:>18}"
 
    lines = [f"{'Product':<20}{'Price':>7}{'Qty':>5}{'Subtotal':>12}", line]
    for item in order.items:
        p = item["product"]
        lines.append(f"{p.name:<20}{p.price:>7}{item['quantity']:>5}{item['subtotal']:>12.2f}")
    lines += [line,
              row("Subtotal:", f"{order.subtotal:.2f} EGP"),
              row("Auto Discount:", f"{order.auto_discount * 100:.0f}%"),
              row("Coupon Discount:", f"{order.coupon_discount * 100:.0f}%"),
              row("Discounted Amount:", f"{order.discounted_amoount:.2f} EGP"),
              row("Service Charge:", f"{order.service_charge:.2f} EGP"),
              line,
              row("FINAL TOTAL:", f"{order.final_total:.2f} EGP"),
              row("Payment Method:", order.payment_method)]
    if order.payment_method == "Cash":
        lines += [row("Received:", f"{order.received_amount:.2f} EGP"),
                  row("Change:", f"{order.change:.2f} EGP")]
    lines += [line, "", "Thank you for your purchase! Enjoy your meal!"]
    show_text_screen(f"Receipt #{order.order_number}", "\n".join(lines), 48)

def show_reports_screen():
    data = cafe.get_report_data()
    lines = []
    if data["total_orders"] == 0:
        lines.append("No orders yet :(")
    else:
        lines += [f"Total Orders        : {data['total_orders']}",
                  f"Total Sales         : {data['total_sales']:.2f} EGP",
                  f"Average Order Value : {data['average']:.2f} EGP",
                  "", f"{'Product':<20}{'Sold':>6}{'Remaining':>12}", "-" * 38]
        for product, quantity in data["sold"].items():
            lines.append(f"{product.name:<20}{quantity:>6}{product.stock:>12}")
        lines += ["", "Low stock:"]
        lines += [f"  - {p.name} ({p.stock} left)" for p in data["low_stock"]] or ["  None"]
        lines += ["Out of stock:"]
        lines += [f"  - {p.name}" for p in data["out_of_stock"]] or ["  None"]
        lines += ["", "Order history:"]
        lines += [f"  #{o.order_number} | {o.final_total:.2f} EGP | {o.payment_method}"
                  for o in cafe.completed_orders]
    show_text_screen("Daily Report", "\n".join(lines), 60)    


def show_main_menu():
    clear_window()
    main_menu = tk.Label (
        window , 
        text= "Main Menu",
        font=("Arial" , 28 , "bold") , 
        bg = BURGUNDY , fg = CREAM )
    main_menu.pack(pady=30) 

    menu_frame = tk.Frame(window , bg = BURGUNDY)
    menu_frame.pack()

    buttons = [
        ("View Products", show_products_screen),
        ("Search Product", show_order_screen),
        ("Add to Cart", show_order_screen),
        ("Remove from Cart", show_cart_screen),
        ("View Cart", show_cart_screen),
        ("Checkout", show_checkout_screen),
        ("Daily Reports", show_reports_screen),
        ("Logout", show_login_screen)
        ]

    for index , (text , action ) in enumerate(buttons) : 
        row = index // 2 
        column = index % 2 
        tk.Button(
            menu_frame , text= text , 
            font=("Arial" , 13 , "bold") , 
            bg= CREAM , fg= DARK_BURGUNDY , width= 20 , height= 2 , 
            command= action 
        ).grid(row=row , column=column , padx= 15 , pady=10)

show_login_screen()
window.mainloop()