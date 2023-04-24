# Pokemon Team Rater
This project is deployed [at this link via Heroku](https://pokemon-team-rater.herokuapp.com/) and uses the [PokeAPI](https://pokeapi.co/) for all data involving Pokemon.

## What is the Pokemon Team Rater?
The Pokemon Team Rater (PTR) is designed for users to create teams of Pokemon and allow other users to rate and comment on these teams. Users will create a team of up to six Pokemon via the PokeAPI and can describe why they have chosen those specific Pokemon for their team. Other logged in users can then rate and comment on different created teams.

## Usage of the PTR

* Users create a secure account with a username and password, and sensitive areas of the app, such as editing a team or commenting on a build, can only be done by logged-in users. Each Team is linked to a User, and within each Team there will be linked Pokemon with data retrieved via the PokeAPI.

* Once logged in, users can create a new team and then search for the Pokemon that they want in a team. An autocompleted list of Pokemon will appear via the search bar. The user can make any additional comments on the team build and upload it to the app's main page, which will display recent team builds. Other users can then view this team and rate and comment on it via the team's specific page. The team's creator can update or delete the team at any time, but only for teams that they have created.

## Creation of the PTR

The PTR incorporates Python, Flask, SQLAlchemy, PostgreSQL, JavaScript, jQuery, Axios, HTML, and CSS. The PTR also utilizes Bootstrap for styling purposes and FontAwesome for icons.
