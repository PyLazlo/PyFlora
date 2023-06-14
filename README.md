Welcome to PyFlora by Vatroslav Veble!!!

PyFlora is a demonstration app written in Python 3.11.3 for the purpose of
demonstrating my knowledge in Python and meant as a final project on
Algebra Python Developer course.

The functionality of the app is accessed after a log in. Anyone can create a new profile on the spot via the Sign up.

The PyFlora App has a Plant database (which is accessed by all users, and all users have CRUD privilage),
a User database, a Pot database and a Data database.

The Users can update and change their information inside the My Profile menu after the log in.

Inside the My Pots menu the users can view all their active pots, which plants are planted in the pots and the
sensors readings which are automatically saved every time you load the My Pots menu or click on the Sync Data button.
You may also add new pots, change their information or plant.

The sensor readings are simulated by a script, and secondary temperature data is accessed via API for the location of Zagreb, Croatia.

The graphs are plotted on the basis of the last 10 results of sensor readings inside the database.



How to run this app:

- open the root folder of the app:
   ```shell
   cd absolute_path_to_root_folder
   ```

- install requirements:
   ```shell
   pip install -r requirements.txt
   ```

- run the app:
    ```shell
    python3 run_app.py
    ```
