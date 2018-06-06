FROM ciscopnp/python_node
CMD  "mkdir /home/pnprma"
COPY . /home/pnprma
COPY ./run.sh /
RUN pip install /home/pnprma
RUN cd /home/pnprma/rma-ui/dna-app; npm install
EXPOSE 3000
#CMD ["nohup npm start > output.log&"]
WORKDIR /home/pnprma
ENTRYPOINT ["/run.sh"]
CMD []