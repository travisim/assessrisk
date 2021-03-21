
# Online Recruit Assessment Card
#### Video Demo:  https://youtu.be/JFRDI1Uc38E
#### Description:
An online version of the infamous Recruit Risk Assessment Card (RAC) used in the SAf for recruits
 this website aims to safe time by allowing recuits to eaily fill in their (RAC) to increase productivity and allow for greater accountability through the use of the `History` feature. Sergeants are able to access past data of recruits Risk Assessment cards to check if recuits were in the proper condition for excercise.
 Recuits themselves are able to look at their hydration levels to find out trends and correlations between their hydration levels and physical performance to take appropriate action to maximize their physical abilities
recuits are also able to more conviniently report sick at their own convinience using the `Report Sick` button
## In templates folder
The html files adds on to `layout.html`using the jinja framework to allow for easy creation of webpages
## In static folder
contains the CSS files along with the favicon
## In main directory
application.py references helpers.py to bring in additional functions while `database.db` is a Sqlite3 database containing 2 tables, `history` and `users`
*interesting fact, the hashes of passwords are stored as hashes in `database.db` to prevent hackers from stealing the passwords
## future improvements
link `Report Sick` feature to apis to notify sergeants through whatsapp or email
include the ability for recruits to see the proper warm up and warm down procedures to encourage them to do so themself.
add physical excercise training instructions and a point system to motivate recruits to excercise while in bunka

## security
the website allows users to create accounts to store their risk assessment infomation allowing users to have privacy when using the application

## list of questions in website


           1. I am feeling well today

           2. I had 7 hours of uninterrupted rest the night before

           3. I do not have any past medical history

           4. I am not recovering from an illness

           5. I am wearing my wrist band for medical tagging purposes

           6. I have taken temperature prior to any physical activity

           7. I have drank at least 500ml of water before the activity

           8. I did not miss any lesson before this activity

           9. The ground condition is not hazardous

           10. None of my personal equipment or weapon is giving me discomfort

           11. My buddy is with me

           12. My buddy has completed his RAC

