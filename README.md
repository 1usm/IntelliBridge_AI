*************************flask setup for local development purposes*******************************

pip3 install requiremet.txt

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install flask-sqlalchemy==3.1.1
pip install flask-migrate==4.0.5
pip install mysqlclient==2.2.1
pip install python-dotenv==1.0.0
pip install gunicorn==21.2.0
pip install supervisor==4.2.5
pip install openai==1.12.0
pip install flask


# Run the application
flask run

# Initialize database
pip install Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create migration
flask db migrate -m "Description of changes"

# Apply migration
flask db upgrade

# Rollback migration
flask db downgrade

# View migration status
flask db current
flask db history


*************************Supervisor Setup (Production)*******************************
# Install supervisor
sudo apt install supervisor

# Create log directory
sudo mkdir -p /var/log/intellibridge
sudo chown -R $USER:$USER /var/log/intellibridge

# Create supervisor config
sudo nano /etc/supervisor/conf.d/intellibridge.conf

# Restart supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start intellibridge