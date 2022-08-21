FROM gcc:4.9

COPY . /myapp
WORKDIR /myapp

RUN gcc -o a Code.c
RUN  ./a < input.txt > ./output.txt 
# // docker image build -t my-gcc-app .
