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

# Start Odoo with the copied config
# Use environment variables for database credentials
CMD ["sh", "-c", "odoo -c /etc/odoo/odoo.conf"]
