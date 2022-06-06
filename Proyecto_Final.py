from fileinput import filename
from tkinter import messagebox, ttk
from tkinter import *
import sqlite3

conetion = sqlite3.connect('database1.db') 

class Login :
        
        def __init__(self, window):
        # Initializations 
                self.wind = window
                #self.wind.title('Register Application')
                
                #tabla = conetion.cursor()
                #tabla.execute(''' create table table1 (usuario varchar (50), password varchar (50) )''' )
                self.wind.title("Login")

                #self.wind.resizable(width=False, height=False)
               
                frame = LabelFrame(self.wind, text = 'Loggin Employee')
                frame.grid(row = 0, column = 0, columnspan = 3, pady = 20, padx=50)

                # Name Input
                Label(frame, text = 'User: ').grid(row = 1, column = 0)
                self.user = Entry(frame)
                self.user.focus()
                self.user.grid(row = 1, column = 1)

                # Last Name Input
                Label(frame, text = 'PassWord: ').grid(row = 2, column = 0)
                self.password = Entry(frame)
                self.password.grid(row = 2, column = 1)
                
                ttk.Button(frame, text = 'Login',command = self.ingresar).grid(row = 6, columnspan = 2, sticky = W + E)
                
                self.message = Label(text = '', fg = 'red')
                self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        def ingresar(self): 
                dato = (self.user.get(), self.password.get())
                query ='SELECT * FROM employee WHERE user=? and cod=?'
                tabla = conetion.cursor()
                tabla.execute(query,dato)
                dato = tabla.fetchall()
                #for dato2 in dato:

                if (len(dato) != 0)  :
                    Product(window)  
                else:
                        self.message['text'] = 'User o password incorrect'        


class Product:
    # connection dir property
    db_name = 'database1.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Register Application')

        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Register new Employee')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        # Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Last Name Input
        Label(frame, text = 'Last Name: ').grid(row = 2, column = 0)
        self.last = Entry(frame)
        self.last.grid(row = 2, column = 1)
        
        # Indentification input
        Label(frame, text = 'Id Number: ').grid(row = 3, column = 0)
        self.id = Entry(frame)
        self.id.grid(row = 3, column = 1)
        
        # Phone number Input
        Label(frame, text = 'Phone: ').grid(row = 4, column = 0)
        self.phone = Entry(frame)
        self.phone.grid(row = 4, column = 1)
        
        # Direction Input
        Label(frame, text = 'Direction: ').grid(row = 5, column = 0)
        self.direct = Entry(frame)
        self.direct.grid(row = 5, column = 1)
        
        # others campus
        self.cod = ''
        self.user = '' 
        self.email =''
        
        
        # Button Add Product 
        ttk.Button(frame, text = 'Save', command = self.add_product).grid(row = 6, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = 2)
        self.tree.grid(row = 4, column = 0, columnspan = 2)
        self.tree.heading('#0', text = 'Cod', anchor = CENTER)
        self.tree.heading('#1', text = 'Full Name', anchor = CENTER)

        # Buttons
        #photo = PhotoImage(filename =['img\\borrar.png'])
    
        ttk.Button(text = 'DELETE', command = self.delete_product).grid(row = 5, column = 0, sticky = W + E)
        ttk.Button(text = 'EDIT', command = self.edit_product).grid(row = 5, column = 1, sticky = W + E)

        # Filling the Rows
        self.get_products()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM employee ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = f'{row[8]}', values = f'{row[1]}.{row[2]}')

    # User Input Validation
    def validation(self):
        valor = False
        if len(self.name.get()) != 0 and len(self.last.get()) != 0 and len(self.id.get()) != 0 :
            if len(self.id.get()) == 11:
                n = self.id.get()
                if n.isalnum():
                    valor = True
                    
            if self.phone.get() != '' :
                if len(self.phone.get()) == 10:
                    n = self.phone.get()
                    n = n[:3]
                    if ( (n == '809' or n == '829' or n == '849') and n.isalnum()):
                        valor = True
                    else: valor = False
                else: valor = False
        return valor   

    def add_product(self):
        if self.validation():
            query = f'SELECT * FROM employee WHERE cedula={self.id.get()}'
            resultado =  self.run_query(query)
            
            if (len(resultado.fetchall()) == 0)  :
                query = 'INSERT INTO employee VALUES(NULL, ?,?,?,?,?,?,?,?)'
            
                if self.name.get() != '':
                    n = self.name.get()
                    l = self.last.get()
                    i = self.id.get()
                    self.user =f'{n[0]}{l[0]}{i[-4:]}'
                    self.cod = i[-4:]
                    
                self.email = f'{self.user}@farcon.com'
                parameters =  (self.name.get(), self.last.get(),self.id.get(),self.phone.get(),self.direct.get(),self.user,self.email,self.cod)
                
                self.run_query(query, parameters)
                self.message['text'] = 'Employee {} added Successfully'.format(self.name.get())
                self.name.delete(0, END)
                self.last.delete(0, END)
                self.id.delete(0,END)
                self.phone.delete(0,END)
                self.direct.delete(0,END)
                        
            else:
                self.message['text'] = 'The Employee exist'
                self.get_products()
        
        else:
            self.message['text'] = 'Name, Last Name and ID Are Required'
        self.get_products()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Employee'
            return
        self.message['text'] = ''
        valor = messagebox.askquestion('DELETE','Do you want to delete employee?')
        if valor == 'yes':
            name = self.tree.item(self.tree.selection())['text']
            query = 'DELETE FROM employee WHERE cod = ?'
            self.run_query(query, (name, ))
            self.message['text'] = 'Employee {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Employee'
            return
        name = self.tree.item(self.tree.selection())['text']
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Employee'
        # Old Name
        Label(self.edit_wind, text = 'Cod:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state ='readonly').grid(row = 0, column = 2)
        
        query = f'SELECT * FROM employee WHERE cod={name}'
        resultado =  self.run_query(query)
        datos = resultado.fetchall()
    
        
        Label(self.edit_wind, text = 'Name: ').grid(row = 1, column = 1)
        self.name = Entry(self.edit_wind,textvariable = StringVar(self.edit_wind, value = datos[0][1]))
        self.name.grid(row = 1, column = 2)
    
        # Last Name Input
        Label(self.edit_wind, text = 'Last Name: ').grid(row = 2, column = 1)
        self.last = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = datos[0][2]))
        self.last.grid(row = 2, column = 2)
        
        # Indentification input
        Label(self.edit_wind, text = 'Id Number: ').grid(row = 3, column = 1)
        self.id = Entry(self.edit_wind,textvariable = StringVar(self.edit_wind, value = datos[0][3]))
        self.id.grid(row = 3, column = 2)
        
        # Phone number Input
        Label(self.edit_wind, text = 'Phone: ').grid(row = 4, column = 1)
        self.phone = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = datos[0][4]))
        self.phone.grid(row = 4, column = 2)
        
        # Direction Input
        Label(self.edit_wind, text = 'Direction: ').grid(row = 5, column = 1)
        self.direct = Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = datos[0][5]))
        self.direct.grid(row = 5, column = 2)
        
        
        parameters =  (self.name.get(), self.last.get(),self.id.get(),self.phone.get(),self.direct.get(),name)
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(parameters, name)).grid(row = 7, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, parametros, name):
        if self.validation():
            query = 'UPDATE employee SET name = ?, lastName = ?, cedula =?, phone = ?, direction = ? WHERE cod = ?'
            self.run_query(query, parametros)
            self.edit_wind.destroy()
            self.message['text'] = 'Employee {} updated successfylly'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Login(window)
    window.mainloop()
