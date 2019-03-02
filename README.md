# iReporter Api

Corruption is a huge bane to Africaâ€™s development. African countries must develop novel and
localised solutions that will curb this menace, hence the birth of iReporter. iReporter enables
any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention

[![Build Status](https://travis-ci.org/bekeplar/iReporterV1.svg?branch=develop)](https://travis-ci.org/bekeplar/iReporterV1)
[![Maintainability](https://api.codeclimate.com/v1/badges/5767084e8421e1056f25/maintainability)](https://codeclimate.com/github/bekeplar/iReporterV1/maintainability)
[![Coverage Status](https://coveralls.io/repos/github/bekeplar/iReporterV1/badge.svg?branch=ch-pep-style)](https://coveralls.io/github/bekeplar/iReporterV1?branch=ch-pep-style)

## Required features

- Users can create an account and log in. 
- Users can create a ?red-flag ??record (An incident linked to corruption). 
- Users can create ?intervention?? record? ??(a call for a government agency to intervene e.g  repair bad road sections, collapsed bridges, flooding e.t.c). 
- Users can edit their ?red-flag ??or ?intervention ??records. 
- Users can delete their ?red-flag ??or ?intervention ??records.  
- Users can add geolocation (Lat Long Coordinates) to their ?red-flag ??or ?intervention  records?. - - Users can change the geolocation (Lat Long Coordinates) attached to their ?red-flag ??or  intervention ??records?. 
- Admin can change the ?status?? of a record to either ?under investigation, rejected ??(in the  event of a false claim)? ??or? resolved ??(in the event that the claim has been investigated and  resolved)?. 


## Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/redflags|Create a redflag resource
GET|api/v1/redflags|Fetch all redflags reported
GET|api/v1/redflags/<redflag_id>|Fetch a specific redflag record
DELETE|api/v1/redflags/<int:redflag_id>|Delete a specific redflag
PATCH|api/v1/redflags/<int:redflag_id>/location|Edit location of a specific redflag
PATCH|api/v1/redflags/<int:redflag_id>/comment|Edit a comment of a specific redflag
PATCH|api/v1/redflags/<int:redflag_id>/status|Edit status of a specific redflag
POST|api/v1/auth/signup|create a new user
POST|api/vi/auth/login|Login a user

## Requirements

- Python
- Flask
- Virtualenv
- postgresql
- Postman

## Getting started

- Clone the project to your local machine

```
git clone https://github.com/bekeplar/iReporter.git
```

- Change to the cloned directory

```

cd iReporter
pip install virtualenv
source venv/bin/activate
git checkout develop
pip install -r requirements.txt
python run.py
```

- For those on windows

```
cd iReporter
python -m venv venv
venv\Scripts\activate
```

- Run tests by

```
pip install pytest
pytest

```

- Testing Endpoints

```
copy the url in the terminal
paste it in postman
Use the following sample data

redflag = [
    {
            "title": "corruption",
            "location": [60, 120],
            "comment": "These are serious ",
            "type": "redflag"
        }
]

user = [
    {
        "firstname":"bekelaze",
        "lastname":"Joseph",
        "othernames":"beka",
        "email":"bekeplar@gmail.com",
        "phoneNumber":"0789057968",
        "username":"bekeplar",
        "password":"bekeplar1234"
    }
]

intervention = [
    {
            "title": "Potholes",
            "location": [35, 110],
            "comment": "There are potholes along Mukono-seeta Road",
            "type": "intervention"
        }
]

```

## Hosting link

[https://keplaxireporter.herokuapp.com/]

## Authors

Bekalaze Joseph

### Courtesy of

Andela Uganda