officially started learniing python

10/12/2024
- watched few odoo-web tutorials and took quiz
- learned commands for odoo CLI 
- learned how to create and modify .conf file
- learned how to run the odoo
- learned about different important urls of backend side and forntend side 
- learned how to Disable Database Manager Or Selector
- learned how to create new odoo module(just a skeleton) and took an overview of its file structure structure

11/12/2024
- watched few odoo-web tutorials and took quiz
- learned following topics 
    - how to make customly created odoo modules to show up on the apps section of the odoo
    - modules __menifest__.py file code structure its keys and vlaues etc. 
    - models.py of custom module
    - classes in python and different type of classes in python like model class which are important in framwork like odoo, django 
    - what is ORM

13/12/2024
- setted 
learned following things
- how to debug odoo
    - using odoo.log file to log every info, critical error etc.
- how to create a class with orm features to easyly interact with database without worring about low-level operations
- what is views in mvc and how to createa and use views.xml 
- how to access database form PowerShell
- learned how to create a basic form, tree view and menu with action 

17/12/2024
learned following things, following the official documentation
-  diffrent type of modal fields
-  common attributes of fields 
- Automatic Fields
- security mechanism
- about csv files
- Access Rights

18/12/2024
learned following things, following the official documentation
-  made a custom form using xml tags and attributes specifically built for odoo. 
-  made a custom search functionality(serch view) to be able to search in different fields. 
-  made a predefined search filter using domain to be able to quick search some widly searched terms. 
-  made a predefined search filter using group by to be able to quickly group common values of some field. 
-  learned about Many2one which is necessary to establish Relations Between Models

19/12/2024
learned following things, following the official documentation
-  made a another sub menu and and third level menu. 
-  added many2one field, in proprerty advertisement form, list and model
-  learned about its concept

20/12/2024
learned following things, following the official documentation
- Many2many field and made seperate view,action, and menu for it.
- One2many field and made seperate view,action, and menu for it.
- auto_install
- learned about diffrent fields in more detail
    - simple fields
    - Relational fields
    - Function/Compute/Reference fields
- learned about diffrent fields attributes in more detail
- Text field vs Char field

21/12/2024
learned following things, following the official documentation
    - applied the Computed Fields
        - learned about its Dependencies
        - learned about its Inverse Function
    - learned about its Onchanges
    
24/12/2024 - sick leave
25/12/2024 - sick leave

26/12/2024
27/12/2024
learned following things, following the official documentation
    - Object Type
    - Action Type
    - Constraints
        - learned about SQL
        - learned about Python
28/12/2024 - picnic
30/12/2024 - sunday
30/12/2024
learned following things, following the official documentation
    - what is xml-rpc
    - inheritance in Odoo
    - learned about standard CRUD using Python inheritanc
    - Delegation

31/12/2024
learned following things, following the official documentation 
    - Overriding the definition of fields in the model
    - Adding constraints to the model
    - Adding methods to the model
    - Overriding existing methods in the model

15/01/2024
learned following things, following the official documentation
    - I reviewed everything I have learned about Odoo so far.
    - how to set widget for a field
    - added a inline list view inside a form
    - did research on ecommerce app in odoo
    - added a default order using _order in model

16/01/2024
learned following things, following the official documentation
    - created a structure of new app `sports_ecommerce` including all the neccessary files.
    - modified __menifiest__.py as per requirment
    - modified __init__.py as per requirment
    - created a model with appropriate fields
    - created a access file ir.model.access.csv to restrict access
    - created a menu (in app switcher, first level and action menu)

17/01/2024
learned following things, following the official documentation
    - created a controller file to show product page
    - created a product page basic templet

18/01/2024
    - learned basics of decorators
    - @http.route decorator for odoo
    - improved the product page layout by modifing the website templet xml file 

20/01/2024

21/01/2024
    - learned about different methods to install libraries Executable Installer, Using Pre-built Wheels, Manual Installation
    - learned about docker
        - what it is
        - image and container
        - basic concepts
        - some main commands
        - about .env file 
        - setup and ran the project successfully.

24/01/2024
    - solved the bug of `missing record for the module`occuring due to leftover records in the database and the fact that Odoo's uninstallation and metadata management are sometimes incomplete.
    - Product Catalog Setup - Created 3-4 sample sports products
    - created a product form view using view template inherentence
    - custom field added to the `product.template` model
    - made inhereted form field invisible
    - learned how to identify any field name using odoo developer tool and inspect element

25/01/2024
    - learned about following things 
        - Templates and Layouts diffrence and structure
        - position, expr, Data Attributes

27/01/2024
    - learned about conditional rendering
    - learned about Primary Inheritance
    - learned about Extension Inheritance

28/01/2025
    - learned Template directives
        - Data output
        - Conditionals
        - Loops
        - attributes
        - setting variables
        - calling sub-templates
    - solved the issue of not being able to menipulate the structure of the web-page 
        - learned how to accuratly find the qweb template being used on the page
        - and how to menipulate it 
29/01/2025
30/01/2025
31/01/2025
    learned following things
    - added a functional add to cart button on the listing page of products
    - passing the correct context
    - Debugging Context Errors in QWeb
    - finding the correct model for the context
    - Identifying the Right Model to Extend

01/02/2025
    - added a menu item to "Categories" to manage category
    - inherited a form view for it and added a discription field in it.
    - to create a mega menu
        - found a template that responsible for the navabar 
        - found a model that responsible for the menu and sub-menu 
03/02/2025
    - modified a menu item "Categories" to manage category with inherinting and extending the right model "product.public.category"
    - inherited a form view for it and added a discription field in it.
    - created a mega menu
        - using odoo inbuit functionality and website modlue created a mega menu. 
        - using edit fucntionality of webisite module edited some content of the mega menu 
04/02/2025
    - leared about what Software Development Life Cycle is.
    - took an overview on how to deploy odoo custom module on the server.
    - took an overview on AWS .
    - added a field inside the "product.template" to add multiple images
    - added a field in form view of product_template which is "product.product_template_only_form_view"
06/02/2025
    - figured out the model and field that stores the multiple images of the product.
    - learned about API
    - created a most basic api
    - created an api to fetch a data of products from odoo product.template module. 
    - learned little bit about postman api software
    - watched video on how to authonticate in odoo from external application 

08/02/2025
    - Learned about JSON-RPC API and its architecture.
    - Explored how JSON-RPC enables remote procedure calls using JSON.
    - Understood its stateless and lightweight nature for efficient communication.
    - Studied authentication and authorization, including token-based access.
    - Gained insights into securing and integrating API-based applications.

10/02/2025
- created JSON-RPC API and achived same result as REST API.
- learned about what is the "web-scraping"
- setup a new enviroment for practice purpose(installed a beuatifulsoup4)
- scraped the "https://quotes.toscrape.com/tag/inspirational/", and stored the quotes, author name and tags in csv file


11/02/2025
learned about the following things
    - used and learned about the "list comprehension"
    - how parsing works  
    - how html code gets fetched
    - what the packages, moduals and submoduals
    - find_all to get the all HTML tags inside a list 
    - .text to get the content from the HTML tag
    - for loop using zip 
    - how to create and write into a csv file 
    - use of headers for request to bypass restriction
    - how to find the api responsible for data that we want to scrap

12/02/2025
learned about the following things
    - learned difference between Playwright and Selenium
    - worked on a demo project to extract the data of all the "Most Popular Movies" from imdb.
        - used selenium to counter the "Lazy Loading" of "Imdb" site movies list data
        - created a custom logic to filter "year" preventing unwanted data while scraping it.
        - added a condition to handle missing data
            - added a conditions so that if some data is missing then it would print "N/A" instead of it
        - learned difference between selenium and playwright
        - successfully extracted follwing data field of 100 movies form Imdb
            - sr. no.
            - title
            - year
            - rating

13/02/2025
learned about the following things.
    - diffrent module and classes used for my perticular requirments 
        - webdriver
        - Service
        - By
        - WebDriverWait
        - expected_conditions
        - ChromeDriverManager
        - time
    - how install crome-drivers
    - understood the logic behind condition which scroll the whole page.
    - serched little bit about how "instagram post downloader" downloads the post

14/02/2025
learned about the following things.
    - did extensive reaseach on the inst post download fucntionality
    - created a web app for a client to extract the pdf tables and insert the data into csv file
        - set up the project
        - did research on what is tablua, what does it do
        - created frontend for it
        - successfully implemented the features
            - upload pdf file
            - extract the data and download the file in csv format

15-02-2025

- Enhanced the project's front-end using Bootstrap for a more appealing design.  
- Created a progress update video for the client.  
- Installed OBS Studio to record the project demo.
