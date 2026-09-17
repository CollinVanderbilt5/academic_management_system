# Full-Stack Academic Management System

by Collin Vanderbilt, Dorian Williams-Webster, Haley Hankins, Will Dorsey

## Overview
This repository contains a full-stack academic management web application engineered to streamline university administration workflows, user authentication, and real-time academic reporting across multi-role user tiers. 

The application features a modular RESTful backend built with Flask, integrated with a cloud-hosted MySQL database on AWS RDS designed to handle complex relational mappings, access controls, and administrative holds.

## Key Highlights
* **Multi-Role API Architecture:** Engineered a Python (Flask) RESTful API enforcing role-based access control (RBAC) across Students, Professors, and Advisors for authentication, class enrollment, advising holds, and assignment tracking.
* **AWS Cloud Database Design:** Designed and normalized a MySQL relational database hosted on AWS RDS with strict foreign key constraints, dynamic indexing, and custom relational schema mappings.
* **Complex Database Queries:** Authored dynamic SQL queries and parameterized statements to execute multi-table joins, assignment scheduling logic, and real-time aggregate calculations (e.g., student grade averages).
* **Full-Stack Security & Integration:** Rendered responsive frontend views using HTML/CSS/JS and configured `Flask-CORS` for secure cross-origin communication between localized development servers and cloud endpoints.

## Tech Stack
* **Backend:** Python, Flask, Flask-CORS
* **Database:** MySQL, SQL
* **Cloud Infrastructure:** AWS RDS
* **Frontend:** HTML5, CSS3, JavaScript

## Installation

Clone this repo, and install mysql if you want a brand new database
If you're using a brand new database update the settings in lines 12-15 and run queries. It should connect and setup database with our setup file

Now you can use the queries in python files you make to test out functions.

But if you want to see what they were used for, you should our site.
In this repo we have a virtual enviorment that we used for the flask server
To access the virtual enviorment enter the following command:

    source venv/bin/activate

Then with the virtual enviorment activated, to get the required libraries enter this command

    pip install -r requirements.txt

After that run server.py, in the terminal it should give you the local webaddress you can use to few the website.
