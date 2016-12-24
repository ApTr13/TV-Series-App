# TV-Series-App
A flask-based Web Application that stores and displays data of TV Series and their Episodes with Facebook Sign-in...
It works on the CRUD Principle... i.e Create, Read, Update & Delete data... 
Also it has Authentication and  Authorization properties...
Visitors can view the TV Serieses and episodes... get their data in JSON format...
Users can sign in using their Facebook ID and add,edit,delete new series and their episodes....

###Contents
1. **db_setup.py** - Database setup module for creating database of the Application...
2. **lotsofseries.py** - A py module for populating "series.db", adding several series with episodes...
3. **project.py** - Flask Project file for the TV Series Application that runs the application on local server
4. **db_setup.pyc** - Pre-complied version of db_setup.py
5. **templates** - A folder containing all .html files to be rendered in app
6. **static** - A folder containing all css and jpg files used in app

In order to run a database, the following things need to be set up:

1. [Virtual Box](https://www.virtualbox.org/)
2. [Vagrant](https://www.vagrantup.com/downloads.html) Virtual Machine
3. [Git](https://git-scm.com/downloads) on Windows(Terminal on Linux/Mac)

Now fork and clone [fullstack-nanodegree-vm repository](https://github.com/udacity/fullstack-nanodegree-vm) so that you get the directory fullstack in your current User.

### Steps to successfully run TV Series App on your localhost...
1. Clone this repository [TV Series App](https://github.com/ApTr13/TV-Series-App).

2. Go to **fullstack->vagrant->**

3. Extract the files of **series.zip** here

4. Now open your Terminal/Cmd/GitBash and give following commands from home folder:
> cd fullstack\vagrant

5. Boot the virtual machine into Virtual box.
> vagrant up

6. Virtual machine gets booted. Now start vagrant with the command:
> vagrant ssh

7. cd to the series folder from home as
> cd vagrant\series

8. First we need to have a database in order to run the Application so complie the **db_setup.py** module
> python db_setup.py

9. Now we need to add some data to our database. so run the **lotsofseries.py** file
> python lotsofseries.py

10. Final step up is to complie the **project.py** which runs a flask environment for our Web Application
> python project.py

Voila :D....
Now you can see the series and episodes pre-added by **Mr.Popo**...
Or you can login yourself using your **Facebook Id**... to add your favourite series and their episodes...

Remember that you can see or edit the py module outside the virtual box... The job of Vagrant is to help set up the database for app...
Install [Python 2.7](https://www.python.org/download/releases/2.7/) to compile the module....
Make sure your Vagrant has Flask installed in it...

For furthur queries, contact apurvatripathi13@gmail.com..... 
Soon launching TV Series app at my very own [Portfolio-ApTr13](http://aptr13.me)... :D



