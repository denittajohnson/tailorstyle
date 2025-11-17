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

# CRITICAL FIX: Changed command line args to use underscores (db_host, db_port, etc.) 
# This is the format Odoo traditionally expects when passed as a command-line option.
CMD odoo \
  -c /etc/odoo/odoo.conf \
  --db_host=$DB_HOST \
  --db_port=$DB_PORT \
  --db_user=$DB_USER \
  --db_password=$DB_PASSWORD \
  --database=$DB_NAME \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
  --init=base \
  --stop-after-init \
  && \
  odoo \
  -c /etc/odoo/odoo.conf \
  --db_host=$DB_HOST \
  --db_port=$DB_PORT \
  --db_user=$DB_USER \
  --db_password=$DB_PASSWORD \
  --database=$DB_NAME \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
  --init=web,website,tailorstyle_management,tailorstyle_website \
  --stop-after-init \
  && \
  odoo \
  -c /etc/odoo/odoo.conf \
  --db_host=$DB_HOST \
  --db_port=$DB_PORT \
  --db_user=$DB_USER \
  --db_password=$DB_PASSWORD \
  --database=$DB_NAME \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons