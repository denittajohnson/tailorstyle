# Base Image: Odoo 17
    FROM docker.io/library/odoo:17@sha256:1e34182546c20b9179a48d88d55628d4c39295f5a43532fa507e126051af5446

    # Install necessary development dependencies for Python packages
    # libsasl2-dev: for LDAP/SASL authentication
    # libxml2-dev, libxslt1-dev: for lxml, which Odoo uses for XML parsing
    # libldap2-dev: for LDAP
    # sassc: for compiling SASS/SCSS files to CSS
    RUN apt-get update && \
        apt-get install -y --no-install-recommends \
        libsasl2-dev \
        libxml2-dev \
        libldap2-dev \
        libxslt1-dev \
        sassc && \
        rm -rf /var/lib/apt/lists/*

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

    # CRITICAL FIX: Removed the --database=$DB_NAME argument.
    # Odoo will now launch and immediately display the Database Manager screen
    # because no database is explicitly specified to load.
    CMD odoo \
      -c /etc/odoo/odoo.conf \
      --db_host=$DB_HOST \
      --db_port=$DB_PORT \
      --db_user=$DB_USER \
      --db_password=$DB_PASSWORD \
      --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
      --workers=1

    # Odoo listens on port 8069
    EXPOSE 8069