# Use official Odoo 17 image
FROM odoo:17

# Copy custom modules into Odoo
COPY ./custom_addons /mnt/extra-addons

# Copy Odoo configuration
COPY ./odoo.conf /etc/odoo/odoo.conf

# Copy requirements.txt from root
COPY ./requirements.txt /tmp/requirements.txt

# Install any extra Python dependencies
RUN pip install -r /tmp/requirements.txt

EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
