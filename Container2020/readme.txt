The following Django Project has the following features:
1- built on a responsive template
2- models service, type, and expense tables.
service table is in a foreign key relationship with type.
expense in a foreign key relationship with both
serive and type table.
unqiue_together constraint is used on type model
3- chained dropdown menu is used on expense table
to make sure the type is displaying only things related 
to service table.
4- sites model to display the sites on the website with
links.
5- missing the tutorial model 
6- This model is completely empty and if you want to work, you must 
first migrate and then, create a superuser and make sure
the superuser has a first and last name, otherwise, you might
see the site a little bit disturbing.


The container folder is called container2020
the project folder is called edition2020
the application folder is called web

the virtualenv is called edition2020