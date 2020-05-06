echo "Remember to 'npm run serve' and 'python manage.py runserver'!"
echo "Now nginx will start..."
nginx -p `pwd`/ -c conf/nginx.conf && echo "[OK], listening to localhost:1234"
