FROM odoo:17

# Set the Odoo user for subsequent commands
USER root

# 1. Copy custom modules
COPY ./custom_addons /mnt/extra-addons

# 2. Copy Odoo configuration file
COPY ./odoo.conf /etc/odoo/odoo.conf

# 3. Copy Python requirements
COPY ./requirements.txt /tmp/requirements.txt

# 4. Install dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Switch back to the Odoo user
USER odoo

# CRITICAL FIX: The startup command must be defined here, NOT in render.yaml.
# This command runs two Odoo processes: first to initialize the database, 
# and second to start the web server for running the application.
CMD odoo \
  -c /etc/odoo/odoo.conf \
  --db-host=$DB_HOST \
  --db-port=$DB_PORT \
  --db-user=$DB_USER \
  --db-password=$DB_PASSWORD \
  --database=$DB_NAME \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
  --init=base,web,website,tailorstyle_management,tailorstyle_website \
  --stop-after-init \
  && \
  odoo \
  -c /etc/odoo/odoo.conf \
  --db-host=$DB_HOST \
  --db-port=$DB_PORT \
  --db-user=$DB_USER \
  --db-password=$DB_PASSWORD \
  --database=$DB_NAME \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons