# UCSB Physics Discord Website

# Desciption 
<table>
<tr>
<td>
The UCSB Physics Discord Website is a python web application using Flask as the main framework. This website is created for the Univeristy of California, Santa Barabara Physics Discord to be able to access information in a seemless and consice manner. Also, it will be able to host forms that members can fill out and that staff memebers can interact with the results. Lastly, it provides <a href="https://github.com/KennethL27/Broida">Broida</a> with an API to interact with the form's databases. 
</td>
</tr>
</table>

___
# Structure
```
phys-disc-web
├───README.md
├───run.py
├───dev
│   ├───main.html
│   ├───pdf_builder.html
│   ├───...
│   
└───website
│   ├───reciept
│   │   ├───static
│   │   │   └───images
│   │   │
│   │   ├───templates
│   │   │   └───templates.html
│   │   │
│   │   ├───email_sender.py
│   │   └───pdf_builder.py
│   │   
│   ├───static
│   │   ├───images
│   │   ├───css_for_templates.css
│   │   ├───...
│   │  
│   ├───templates
│   │   ├───admin
│   │   ├───forms
│   │   ├───reciept
│   │   ├───html_templates.html
│   │   ├───...
│   │
│   ├───__init__.py
│   ├───forms.py
│   ├───models.py
│   ├───routes.py
│   ├───website.db
│   └───website_api.py
│   
└───phys_disc_api.py

```
*Note: the static and templates folder in website/reciept are currently not being used.*


___
# Features

## Forms
The forms built into the website  can be found in [form.py](https://github.com/KennethL27/ucsb-discord-web-dev/blob/master/website/forms.py). One of the main reasons for creating this website is to be able to customize the forms we often use for the organization. Often than not when using other types of forms (ie. Google Forms) none of the inputs can be checked before the form is submitted. As written in the code there are a couple of useful validations that occur before a user can submit their form. The main validation occurs when checking if the user correctly used a valid email address. When filling out the verification form, if a user is a currently attending UCSB then they must submit an email ending with 'ucsb.edu' or 'umail.ucsb.edu' otherwise to complete the form they may recieve a temporary verification. Another extremely useful validation occurs when a user is filling out a form is to check if the username provided contains a discord descrimator (#xxxx). Lastly, as staff members create forms with other platforms there is no way to restrict responses to verified members; however, with the database the form can check if the user is verified or not.  

## API
To allow this website to be extremely useful to the Discord Server an API is created to allow Broida to interact with information collected with the forms mentioned above. The API is split between two files: [backend_api.py](https://github.com/KennethL27/ucsb-discord-web-dev/blob/master/website/website_api.py) and [phys_disc_api.py](https://github.com/KennethL27/ucsb-discord-web-dev/blob/master/phys_disc_api.py). The backend_api allows for the the api that will run on Broida (or any future Discord Bots) to access the database only if it passes the correct token. As the api continues to be built more information and specific information will accessible. Similarly, the phys_disc_api can obtain and return the set of information given by the backend_api and when needed can alter the database for a given entry.

___
# Installation
*Currently only executed on localhost.*
In order to execute and view the live website along with the api, simply run [run.py](https://github.com/KennethL27/ucsb-discord-web-dev/blob/master/run.py). To view the site on different devices connected to the same network, comment the 5th line and uncomment the 4th line.

___
# Support
Feel to reach out to me for any questions or concerns at kenneth.lara01@gmail.com

___
# Roadmap
The following steps need to be met in order to move onto the next stage of the project:
1.  Complete the API for sending and recieving information on all databases.
2.  Able to distingush between a student and professor Verification Form.

The next step will be hosting the website either with the Physics deparmtent at UCSB or using a web hosting service.