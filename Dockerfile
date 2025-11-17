# Use official Odoo 17 image
FROM odoo:17

# Copy custom modules into Odoo
COPY ./custom_addons /mnt/extra-addons

# Copy Odoo configuration template
COPY ./odoo.conf /etc/odoo/odoo.conf

# Copy requirements.txt from root
COPY ./requirements.txt /tmp/requirements.txt

# Install any extra Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Expose Odoo port
EXPOSE 8069

# Start Odoo using environment variables for DB and admin password
CMD ["sh", "-c", "\
odoo -c /etc/odoo/odoo.conf \
--db_host=${DB_HOST} \
--db_port=${DB_PORT} \
--db_user=${DB_USER} \
--db_password=${DB_PASSWORD} \
--db_name=${DB_NAME} \
--admin_passwd=${ADMIN_PASSWD} \
"]
