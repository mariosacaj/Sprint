FROM mskx4/sprint:stable


WORKDIR /app
COPY . /app



# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "Sprint", "/bin/bash", "-c"]
RUN python manage.py collectstatic --no-input
RUN ["chmod", "+x", "commands.sh"]

EXPOSE 80
EXPOSE 8000
EXPOSE 8080