# to build locally
docker build -t cc-lu-2020/dejavu . 

# to run locally
docker run --cpus=2 --rm --name djvu -it cc-lu-2020/dejavu /bin/bash

# to copy files inside container to test
docker cp ./my_solution djvu:/home/challenge/

# connect to container (and then run your solution)
docker exec -it djvu /bin/bash

