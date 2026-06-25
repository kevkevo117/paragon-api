# Paragon API

A REST API built with Python and Flask for managing cities and characters in a custom fantasy campaign world.

## Features

- View all cities
- View individual cities
- View all characters
- Create new characters
- Store character data in SQLite

## Technologies

- Python
- Flask
- SQLAlchemy
- SQLite
- Git

## Endpoints

### Cities

GET /cities

GET /cities/<city_name>

### Characters

GET /characters

POST /characters

### Database Characters

GET /dbcharacters

## Example Character

{
    "name": "Aldric",
    "class": "Paladin",
    "city": "Fortitudo"
}