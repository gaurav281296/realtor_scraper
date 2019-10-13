from validator_collection import checkers
from tkinter import *

root=Tk()
root.title('Realtor Scraper')

# LABELS

title_label=Label(root, text = 'Real Estate Data')
title_label.grid(row=0,column=1,columnspan=2)

state_label=Label(root, text = 'State')
state_label.grid(row=1,column=2)

city_label=Label(root, text = 'City')
city_label.grid(row=2,column=2)


#Buttons

view_button=Button(root,text="View all",width=12,command=view_command)
view_button.grid(row=2,column=3)

search_button=Button(root,text="Search entry",width=12,command=search_command)
search_button.grid(row=3,column=3)

add_button=Button(root,text="Add entry",width=12,command=add_command)
add_button.grid(row=4,column=3)

update_button=Button(root,text="Update",width=12,command=update_command)
update_button.grid(row=5,column=3)

delete_button=Button(root,text="Delete",width=12,command=delete_command)
delete_button.grid(row=6,column=3)

exit_button=Button(root,text="Exit",width=12,command=root.destroy)
exit_button.grid(row=7,column=3)


root.mainloop()