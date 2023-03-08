import tkinter
from tkinter import messagebox
import pandas as pd
import tldextract
import ttkbootstrap as ttk
from tkinter import *
from ttkbootstrap.constants import *
from tkinter import filedialog
from Src_File.webtech import web_tech
from Src_File.cookie import cookie
from Src_File.http_method import http_methods
from Src_File.headers import headers
from Src_File.sslscan import get_ssl_info
from Src_File.subdomains import find_subdomains
from Src_File.website_links import *
from Src_File.Excel_format import format_worksheet
from Src_File.domain_info import whois_info
import os
from threading import *


base_folder = os.path.dirname(__file__)
theme_file = os.path.join(base_folder, 'src/files/theme.txt')

base_folder = os.path.dirname(__file__)
image_src = os.path.join(base_folder, 'src/images/document.png')

base_folder = os.path.dirname(__file__)
setting_image = os.path.join(base_folder, 'src/images/settings.png')


base_folder = os.path.dirname(__file__)
subdomain_file = os.path.join(base_folder, 'src/files/subdomains.txt')


with open(theme_file, 'r')as f:
    theme=f.read()
    root = ttk.Window(themename=theme)  # solar,darkly,cyborg,vapor,superhero,morph

    style = ttk.Style()
    root.title("Scanner")
    root.iconphoto(False, PhotoImage(file=image_src))
    root.maxsize(width=480, height=250)
    root.minsize(width=480, height=250)

    label1 = ttk.Label(root, text="URL", font=('courier', 18), bootstyle="info")
    label1.place(x=35, y=55)

    ente = ttk.Entry(root, width=35, font=('courier', 10), bootstyle="black")
    ente.place(x=120, y=50, height=40)

def scan():
    global url
    try:
        url = ente.get()
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} is reachable.")
            button_explore.configure(state=DISABLED)
            ente.configure(state=DISABLED)
            main()
        else:
            print(f"{url} is not reachable. Status code: {response.status_code}")
            messagebox.showinfo("Error", "Invalid URL")
    except requests.exceptions.RequestException:
        print(f"{url} is not reachable.")
        messagebox.showinfo("Error", "Invalid URL")




def main():
    folder_selected = filedialog.askdirectory()



    t1 = Thread(target=web_tech,args=(url,))
    t2 = Thread(target=cookie,args=(url,))
    t3=Thread(target=headers,args=(url,))
    t4=Thread(target=http_methods,args=(url,))
    t5 = Thread(target=get_ssl_info, args=(url,))
    t6 = Thread(target=crawl, args=(url,))
    t7 = Thread(target=find_subdomains, args=(url,))
    t8=Thread(target=whois_info,args=(url,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t8.start()
    # create a list of threads and their respective progress values
    threads = [(t1, 10), (t2, 20), (t3, 30), (t4, 40), (t5, 50), (t6, 60), (t7, 70),(t8,80)]

    while any([t.is_alive() for t, _ in threads]):
        # update the progress bar based on the completion of the threads
        progress_value = sum([p for t, p in threads if not t.is_alive()])
        progress['value'] = progress_value
        root.update()

        # calculate the percentage of completion
        percentage = round(progress_value / sum([p for _, p in threads]) * 100)
        label.config(text=f"Progress: {percentage}%")
        root.update()


    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    tld_parts = tldextract.extract(url)
    domain = tld_parts.domain
    file_path = folder_selected + '/' + domain + ".xlsx"
    df_web_tech = web_tech(url)
    df_cookie = cookie(url)
    df_header=headers(url)
    df_http_method=http_methods(url)
    df_getssl=get_ssl_info(url)
    df_getssl=df_getssl.T
    df_crawl=crawl(url)
    df_whois=whois_info(url)
    df_whois=df_whois.T
    internal_df = pd.DataFrame(list(internal_urls), columns=["Internal Links"])
    # Create a DataFrame for external links
    external_df = pd.DataFrame(list(external_urls), columns=["External Links"])
    df_find_subdomain=find_subdomains(url)
    df_subdomains = pd.DataFrame(df_find_subdomain, columns=["Subdomain", "Server"])
    if not folder_selected:
        messagebox.showinfo("Error",'Select the folder for Output')
    else:
        with pd.ExcelWriter(file_path) as writer:
            df_web_tech.to_excel(writer, sheet_name='Technologies', index=False)
            format_worksheet(writer, 'Technologies')

            df_cookie.to_excel(writer, sheet_name='Cookies', index=False)
            format_worksheet(writer, 'Cookies')

            df_http_method.to_excel(writer, sheet_name='HTTP Methods', index=False)
            format_worksheet(writer, 'HTTP Methods')

            df_header.to_excel(writer, sheet_name='Headers', index=True)
            format_worksheet(writer, 'Headers')

            df_getssl.to_excel(writer, sheet_name='SSLScan', index=True)
            format_worksheet(writer, 'SSLScan')

            df_whois.to_excel(writer, sheet_name='Whois', index=True)
            format_worksheet(writer, 'Whois')



            # df_whois.to_excel(writer, sheet_name='WhoisLookup', index=False)
            # format_worksheet(writer,'WhoisLookup')

            internal_df.to_excel(writer, sheet_name='Internal Links', index=False)
            format_worksheet(writer, 'Internal Links')

            external_df.to_excel(writer, sheet_name='External Links', index=False)
            format_worksheet(writer, 'External Links')

            df_subdomains.to_excel(writer, sheet_name='Subdomains', index=True)
            format_worksheet(writer, 'Subdomains')

            label.config(text=f"Progress: {100}%")
            messagebox.showinfo("Scan Completed", "The Scan has finished!.")
            root.after(1000, root.destroy)


def themechange():
    vare=combo.get()
    with open(theme_file, 'w')as f:
        style.theme_use(vare)
        f.write(vare)
        window.destroy()


def loadfile():
    input_file_path = filedialog.askopenfilename(title="Select Input File",
                                                 filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    # check if user selected a file
    if input_file_path:
        # check if file extension is txt
        if input_file_path.endswith('.txt'):
            # open input file in read mode
            with open(input_file_path, 'r') as input_file:
                # read the contents of the input file
                input_file_contents = input_file.read()

            # ask user to select output file
            output_file_path = subdomain_file

            # check if user selected a file
            with open(output_file_path, 'w') as output_file:
                # write the contents of the input file to the output file
                output_file.write(input_file_contents.replace(" ", ""))

            # inform user that file has been written successfully

            messagebox.showinfo("Notification", 'File is upload')
            window.destroy()
        else:
            messagebox.showinfo("Error",'Select the file')
            window.destroy()

def open_file():
    # Open a file dialog to select a file
    file_path = subdomain_file
    if not file_path:
        return

    # Create a new window to display the file
    window = ttk.Toplevel(root)
    window.title(file_path)
    window.iconphoto(False, PhotoImage(file=image_src))
    window.geometry("500x500")

    # Create a text widget to display the file contents
    text_widget = ttk.Text(window)
    text_widget.pack(expand=True, fill="both")

    # Read the file contents and display in the text widget
    with open(file_path, "r") as file:
        text_widget.insert("1.0", file.read())

    def save_file():
        # Save the file contents back to the original file
        with open(file_path, "w") as file:
            file.write(text_widget.get("1.0", "end-1c"))
            window.destroy()

    # Add a save button to save the changes
    save_button = ttk.Button(window, text="Save", command=save_file)
    save_button.pack()


def popup():
    global eee,combo,window
    # Create a new window
    window = Toplevel(root)
    window.geometry("210x220")
    window.title("port  configuration")
    window.iconphoto(False, PhotoImage(file=image_src))
    # window.maxsize(width=210, height=220)
    # window.minsize(width=210, height=220)
    note = ttk.Notebook(window)
    note.pack(pady=15)
    frame1 = Frame(note, width=680, height=500)
    frame2 = Frame(note, width=680, height=500)
    frame1.pack(fill="both", expand=1)
    frame2.pack(fill="both", expand=1)
    note.add(frame1, text="Themes")
    note.add(frame2, text="subdomain file")

    # themes tab
    label3 = ttk.Label(frame1, text="Themes", font=('courier', 12))
    label3.place(x=28, y=40)
    with open(theme_file, 'r') as f:
        eee = ["solar", "darkly", "cyborg", "vapor", "superhero", "morph", "cosmo", "sandstone", "flatly", "yeti",
               "lumen",
               "pulse", "minty", "journal", "cerculean", "united", "simplex", "litera"]
        combo = ttk.Combobox(frame1, bootstyle=" info outline menubutton", values=eee, width=13, font=('courier', 10))
        combo.place(x=40, y=75, height=25)
        combo.set(f.read())
        # Create a main button
        btn2 = ttk.Button(frame1, text='ok', command=themechange)
        btn2.place(x=70, y=125)

    label2 = ttk.Label(frame2, text='Load the file for subdomain')
    label2.pack(padx=10, pady=10)
    button1 = ttk.Button(frame2, text='Load File', command=loadfile,bootstyle=" outline toolbutton")
    button1.pack(padx=10, pady=10)

    paste = ttk.Button(frame2,text='Open',bootstyle=" outline toolbutton",command=open_file)  # borderwidth=0,width=50,height=30)
    paste.place(x=70,y=100)





im1=tkinter.PhotoImage(file=setting_image)
btn=ttk.Button(root,image=im1,bootstyle=" success link button",command=popup)#borderwidth=0,width=50,height=30)
btn.place(x=10,y=5)
button_explore = ttk.Button(root,
                        text = "Scan",bootstyle=" outline toolbutton",command=scan)
button_explore.place(x=210,y=129,height=39)

progress = ttk.Progressbar(root, length=200, mode="determinate")
progress.place(x=135,y=195)
progress.step(0)
label = Label(root, text="Progress: 0%")
label.place(x=185,y=210)

root.mainloop()
