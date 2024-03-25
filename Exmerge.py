#Will import this module so that i can use it for troubleshooting and debugging
from datetime import datetime
#This library will interact with excel files 
import pandas as pd 
 #For mathmatical calculations and the like
import numpy as np 
#This one is for graph plotting and data visualization
import matplotlib.pyplot as plt 
#The Library responsible for the UI of the project 
import flet as ft 
#This library is for navigating to the folder directory 
import os 

#The code below contains all the python code that will build both the backend and frontend of the application. 
#here is the variable to control sessions
newlogsession = True
#Code for evaluating the datatype of input given
def datatypeevaluator(data):
    def is_integer():
        try: 
            if int(data) == float(data):
                return int(data)
        except: 
            pass
    
    def is_float():
        try: 
            index = str(data).index('.')
            return float(data)
        except: 
            pass
    
    def is_string():
        try: 
            try: 
                int(data)
            except: 
                float(data)
        except: 
            return data
    
    intval = is_integer()
    floatval = is_float()
    stringval = is_string()
    if intval != None : 
        return intval
    elif floatval != None: 
        return floatval
    elif stringval != None: 
        return stringval
    else: 
        print("Something went wrong with the input conversion we are sorry !")
    
    #This function will log a report on what all processes that occur in the application
def logreport(data):
    filename = "log.txt"
    currentdate = datetime.today()
    try: 
        with open(filename , "a") as file : 
            file.write(" " + "\n")
            file.write(str(currentdate) +" : "+ data.strip() + "\n")
    except FileNotFoundError: 
        print(f"File '{filename}' not found. Creating a new file")
        with open(filename , "w") as file: 
            file.write(" " +"\n")
            file.write(str(currentdate) +" : " + data.strip() + "\n")
    except Exception as e: 
        print(f"Error writing to file: {str(e)}")
        
#The main function is the function that will run and build the entire application from scratch and it will run in a continuous loop till the user exits the application.
def main(page : ft.Page):
    column_values = []
    page.appbar = ft.AppBar(
        leading = ft.IconButton(ft.icons.HELP  ), 
        title = ft.Text("File Analyzer"),
        center_title= False , 
        bgcolor= ft.colors.SURFACE_VARIANT,
        actions = [
            ft.IconButton(ft.icons.PALETTE)
        ]
    )
    page.theme_mode = 'light'
    page.window_width = 1900
    page.window_height = 1000
    page.window_resizable = False
    #Feed Back for an ongoing process
    def Start():
        progress_label.value = "Processing"
        progring.value = None
        page.update()
    #FeedBack for the end of a process
    def Done():
        progress_label.value = "Finished"
        progring.value = 1
        page.update()
    #Feed Back for when a process experiences a halt or problem 
    def AbortProcess():
        progress_label.value = "Process Aborted check log!"
        progring.value = 0
        page.update()
    #This is the function that will plot the bar graphs that compare the total previous weeks transactions with the current week transactions
    def plot_comparison(e: ft.FilePickerResultEvent):
        try : 
            Start()
            data = []
            for file in e.files: 
                df = pd.DataFrame()
                if file.name.endswith(".xlsx"):
                    df = pd.read_excel(file.path)
                elif file.name.endswith(".csv"):
                    df = pd.read_csv(file.path)
                data.append([file.name , len(df)])
            x = []
            y = []
            for element in data: 
                x.append(element[0])
                y.append(element[1])
            plt.bar(x , y)
            plt.title("Comparison Data")
            plt.xlabel("files")
            plt.ylabel("Number of transactions")
            plt.show()
            logreport("graphs plotted successfully")
            Done()
        except Exception as e : 
            print(f"Something went wrong: {str(e)}")
            AbortProcess()
    #this function will collect the values of different columns that have been queried and output them as bargraphs
    def plot_column_values(e):
        try: 
            Start()
            x = []
            y = []
            for element in column_values: 
                x.append(str(element[0]) + str(element[1]))
                y.append(element[2])
            plt.bar(x,y)
            plt.title("Query Values")
            plt.xlabel("Columns")
            plt.ylabel("Number of Transactions")
            plt.show()
            logreport("Column Graphs plotted successfully")
            Done()
        except Exception as e : 
            logreport("Could not plot column graphs " + str(e))
            AbortProcess()
    #This function will calculate the values of different columns to display them numerically
    def count_column_values(e):
        try:
            Start()
            if target_directory.value != "***":
                f_path = target_directory.value 
                df = pd.DataFrame()
                if f_path.endswith('.xlsx'):
                    df = pd.read_excel(f_path)
                elif f_path.endswith('.csv'):
                    df = pd.read_csv(f_path)
                else: 
                    print("Incorrect file type chosen")
                    return
                if df.empty: 
                    pass
                else: 
                    string = Column_input.value
                    stringlist = string.split(",")
                    progress_label.value = "Counting values..."
                    page.update()
                    countval = df[f"{stringlist[0]}"].value_counts()[datatypeevaluator(stringlist[1])]
                    progress_label.value = "Finished!"
                    page.update()
                    columndata.controls.append(ft.Text(f"Columnname: {stringlist[0]}; Query: {stringlist[1]}; Result: {str(countval)}"))
                    column_values.append([stringlist[0] , stringlist[1] , countval])
            else: 
                print("Please select a document")
            page.update()
            logreport("Counted values successfully")
            Done()
        except Exception as e: 
            logreport("Could not count values in columns " + str(e))
            AbortProcess()
    #The function below will be responsible for selecting the directory when the file picker is used
    def selectdirectory(e: ft.FilePickerResultEvent):
        directorypath = e.path
        try: 
            Start()
            DirectoryLabel.value = f"{e.path}"
            directory = e.path
            if directory != None and filetypelist.value != None: 
                mergebtn.disabled = False
            elif directory: 
                mergebtn.disabled = True
            page.update()
            logreport(f"Directory {directorypath} selected successfully")
            Done()
        except Exception as e:
            logreport(f"Could not select directory {directorypath}" + str(e)) 
            AbortProcess()
    # This code will be responsible for selecting the file that needs to have its data visualized
    def selectDocument(e: ft.FilePickerResultEvent):
        try: 
            Start()
            Documentpath = e.files[0].path
            Documentname = e.files[0].name
            target_directory.value = Documentpath
            target_directory.visible = False
            df = pd.DataFrame()
            if Documentname.endswith(".csv"):
                df = pd.read_csv(Documentpath)
            elif Documentname.endswith(".xlsx"):
                df = pd.read_excel(Documentpath)
            else: 
                print("Error encountered")
            if df.empty:
                print("No data detected in document")
            else: 
                table.columns = []
                table.rows = []
                for col in df.columns:
                    table.columns.append(ft.DataColumn(ft.Text(col)))
                count = 0 
                while count < 10 : 
                    rowlist = df.iloc[count].to_list()
                    controllist = []
                    for element in rowlist: 
                        controllist.append(ft.DataCell(ft.Text(element)))
                    table.rows.append(ft.DataRow(cells = controllist))
                    count +=1 
            page.update()
            logreport(f"Document {Documentpath} selected")
            Done()
        except Exception as e : 
            print("Something went wrong: {0}".format(str(e)))
            logreport(f"could not Select Document {Documentpath}" + str(e))
            AbortProcess()
        
    #This is to enable the mergebutton incase it is not yet enabled yet 
    def enablemerge(e):
        condition = "Directory: **********"
        if DirectoryLabel.value == condition or filetypelist.value == None: 
            mergebtn.disabled = True 
        elif DirectoryLabel.value != condition and filetypelist.value != None: 
            mergebtn.disabled = False
        page.update()
    #The Function responsible for merging the files in the directory and then writing them to an excel document
    def startmerge(e):
        try: 
            Start()
            directory = DirectoryLabel.value 
            dataframes = read_files(directory)
            df = pd.concat(dataframes)
            filetype = filetypelist.value 
            if filetype == "xlsx":
                df.to_excel( os.path.join(directory , "Master File.xlsx"),index = False)
            elif filetype == "csv":
                df.to_csv( os.path.join(directory , "Master File.csv"), index = False)
            logreport(f"Files in ({directory}) have been merged successfully")
            Done()
        except Exception as e: 
            logreport(f"Error encountered merging directory({directory}): ({str(e)})")
            AbortProcess()
        #This is the function that is capable of actually reading the files that need to be merged
    def read_files(folder_path):
        try: 
            Start()
            if filetypelist.value == "xlsx":
                dataframes = []
                for filename in os.listdir(folder_path):
                    progress_label.value = "Loading {0}".format(filename)
                    page.update()
                    if filename.endswith("xlsx"):
                        file_path = os.path.join(folder_path , filename)
                        dataframe = pd.read_excel(file_path)
                        dataframes.append(dataframe)
                progress_label.value = "Finished!"
                page.update()
                return dataframes
            elif filetypelist.value == "csv":
                dataframes = []
                for filename in os.listdir(folder_path):
                    progress_label.value = "Loading {0}".format(filename)
                    page.update()
                    if filename.endswith("csv"):
                        file_path = os.path.join(folder_path , filename)
                        dataframe = pd.read_csv(file_path)
                        dataframes.append(dataframe)
                progress_label.value = "Finished!"
                page.update()
                return dataframes
            logreport(f"Files in directory {folder_path} read successfully")
            Done()
        except Exception as e: 
            print(f"Error: {e}")
            logreport(f"Files in directory ({folder_path})could not be read ({str(e)})")
            AbortProcess()
    
    #This is the filepicker that will collect the two files to be compared and compare the total number of transactions in each of them 
    pick_graph_data = ft.FilePicker(
        on_result = plot_comparison
    )
    #This the filepicker i will use to fetch the directory of the folder to be operated on
    Directory_picker = ft.FilePicker(
        on_result= selectdirectory
    )
    #Here will be the second filepicker that will select the file whose data we are to operate on
    document_picker = ft.FilePicker(
        on_result= selectDocument
    )
    #variables
    conwidth = page.window_width
    conheight= page.window_height
    directory = '**********'
    process = "#"
    #Input controls here 
    select_directory_btn = ft.ElevatedButton(text= "Select Directory", on_click= lambda e: Directory_picker.get_directory_path())
    comparebtn = ft.ElevatedButton(text = "Compare Transaction totals" , on_click = lambda e: pick_graph_data.pick_files(allow_multiple= True) )
    mergebtn = ft.ElevatedButton(text = "Merge Files" , disabled = True , on_click= startmerge)
    select_file_btn = ft.ElevatedButton(text = 'Select File' , on_click= lambda e: document_picker.pick_files(allow_multiple= False))
    Column_input = ft.TextField(hint_text= "Enter the Column and the value you want to query separated by a comma")
    process_column_values_btn = ft.ElevatedButton(text = "Process Column Values" , on_click=count_column_values)
    plot_btn = ft.ElevatedButton(text="Plot graph for column values" , on_click= plot_column_values)
    add_column = ft.ElevatedButton(text = "Add Column")
    target_directory = ft.Text("***")
    filetypelist = ft.Dropdown(
        width = 100 , 
        options = [
            ft.dropdown.Option("csv"),
            ft.dropdown.Option("xlsx")
        ],
        on_change= enablemerge
    )
    #Output controls here 
    progring = ft.ProgressRing(width = 32 , height = 32 , stroke_width = 5 , value = 0  )
    DirectoryLabel  = ft.Text(f"Directory: {directory}")
    select_directory_label = ft.Text("Selected Directory will be here")
    columndata = ft.Column()
    mini_output_box = ft.Container(content= columndata)
    #I want this container to hold the datatable that will also contain some of the content that wil be used when generating graphs in the application
    table = ft.DataTable()
    data_table_Container = ft.Container( border= ft.border.all(2 , ft.colors.BLACK),width = 1221, height = 597,content = ft.Row( controls= [table] , scroll= True))
    progress_label = ft.Text("Progress Status")
    progressbar = ft.ProgressBar(width = 400 , color = 'amber' , bgcolor = "#eeeeee")

    #Assembly of all controls the outputs and inputs together
    dashboard = ft.Column(
        height= conheight,
        alignment= ft.MainAxisAlignment.START,
        controls = [
            #Here is the top row of controls that include the Text label and the button to select the directory and to merge the files as well 
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                width = conwidth,
                controls =[
                    ft.Container(
                        height= (conheight*(1/10)), 
                        border= ft.border.all(2 , ft.colors.BLACK),
                        width = (conwidth * 0.95) , 
                        content= ft.Row( alignment= ft.MainAxisAlignment.SPACE_EVENLY, controls = [select_directory_btn , DirectoryLabel , mergebtn ,filetypelist])),
                ]
                ),
                #This is the row that will handle the csv file contents and even populate them in a datatable
            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                width = conwidth , 
                controls = [
                    ft.Container(height = (conheight*(3/5)),
                                 width= (conwidth * 0.95),
                                 border = ft.border.all(2 , ft.colors.BLACK), 
                                 content=ft.Row(controls = [
                                     #The controls in this column will contain the file you want to select to process your results and load in the data table
                                     # The column you want to select to process the data and the columns selected will be displayed in the minibox below as a list.
                                     #You can also remove the columns selected below as well.
                                 ft.Column(
                                     width = (conwidth * (3/10)),
                                     height = conheight * (3/5),
                                     controls = [ft.Row(
                                         controls=  [select_file_btn , target_directory]
                                     ) , Column_input , mini_output_box]
                                     ),
                                 ft.Column(
                                     scroll= 'always',
                                     width= conwidth * (7/10),
                                     height = conheight * (3/5),
                                     controls=[data_table_Container]
                                     )    
                                 ])
                                 )
                ]
                ),
            ft.Row(
                alignment= ft.MainAxisAlignment.CENTER,
                width= conwidth , 
                controls = [
                    ft.Container(
                        border = ft.border.all(2 , ft.colors.BLACK ),
                        padding = 20,
                        height= 170,
                        width= (conwidth * 0.95),
                                 content= ft.Column(alignment = ft.MainAxisAlignment.CENTER,
                                                height = (conheight * (1/5)),controls = [
                                         ft.Row(
                                             alignment = ft.MainAxisAlignment.CENTER,
                                             controls = [process_column_values_btn , plot_btn , comparebtn, progress_label , progring]
                                         )
                                     ]
                                 )
                                 )
                ]
            )
        ]
        )
    page.overlay.append(Directory_picker)
    page.overlay.append(document_picker)
    page.overlay.append(pick_graph_data)
    page.add(dashboard)
    
ft.app(target= main )