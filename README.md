# Run in Local
Run it with:                                                                                                                                                            

source venv/bin/activate
python manage.py runserver

Then visit:
- http://127.0.0.1:8000/ — homepage
- http://127.0.0.1:8000/gallery/ — gallery with filtering
- http://127.0.0.1:8000/admin/ — admin to add artworks/tags

You'll want to create a superuser if you haven't already so you can log into the admin:

python manage.py createsuperuser