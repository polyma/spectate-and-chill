FROM node:6.6.0
RUN npm install -g nodemon

RUN useradd --user-group --create-home --shell /bin/false app


ENV HOME=/home/app

#Copy commands result in root-owned files
RUN chown -R app:app $HOME/


USER app
COPY . $HOME/code
WORKDIR $HOME/code

USER root
RUN npm install --rebuild
RUN npm cache clean


USER app
#CMD ["nodemon", ".", "-L"]
CMD ["node", "."]
