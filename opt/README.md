# Extra Tool 
## Fast downward tool
src: https://www.fast-downward.org

```bash
fast-downward --translate $domainfile $problemfile
```

## H2-fd-preprocessor
src: https://github.com/galvusdamor/h2-fd-preprocessor

- note: this repo require 32 bit support 
```bash
sudo apt-get install gcc-multilib g++-multilib
```

```bash
./opt/h2-fd-preprocessor/bin/preprocess < output.sas
```

## VAL
### How to compile VAL

```bash
bash scripts/build_linux_windows_dev.sh
```

## Planning as a service 
- due to that `https://solver.planning.domains/` api is not stable, we are going to directly setup the planning service locally. 
- please check `https://github.com/AI-Planning/planning-as-a-service` to run the service. 

- in order to run the server, remember to have `docker-compose` installed in your machine
- **TroubleShoot**
  - We may want to docker-compose build --no-cache to ensure we are not using any cached images, we found that the pip version may causing issues, one may want to change `RUN python3 -m pip install --upgrade pip setuptools wheel` to `RUN python3 -m pip install --upgrade "pip<24.1" "setuptools==65.7.0" "wheel==0.38.4"`
  - failed to find loop device: `sudo modprobe loop`

```bash
# make sure you are in the server folder to run the makefile
cd server
sudo make
```

To shut down:

```bash
docker compose down
```



## Planutils 
- the tool is used for evaluation module 
- we need to set it up before we can use it 
- may need to install `singularity-ce`

```bash
source .venv/bin/activate
planutils activate
export PLANUTILS_PREFIX="$HOME/.planutils"
dir_to_check="$PLANUTILS_PREFIX/bin"
# Environment need to be activated first
# Check if PLANUTILS_PREFIX is not already in PATH
if [[ ":$PATH:" != *":$dir_to_check:"* ]]; then
    export PATH="$PATH:$PLANUTILS_PREFIX/bin"
fi


cd opt/planutils-0.10.11
pip install -e . 
planutils setup 
planutils activate 
# now do the above thing
planutils install -f -y lama-first
planutils install -f -y val
planutils install -f -y dual-bfws-ffparser
```

- once complete setup, we can run `planutils activate` to activate the environment. 
- when the environment is activated, we can run the planner e.g., `lama-first example/casino/final-domain.pddl example/casino/final-problem.pddl `
- the output will be saved in the current working directory (pwd)