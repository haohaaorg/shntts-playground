# SHNTTS-Playground
A full stack playground for ttsmms model (using shn model)

## Included
- [x] fronend
    - NextJS
- [x] backend
    - Flask

## Usage
1. clone this project
```sh
git clone https://github.com/NoerNova/shntts-playground.git
```

2. make scripts runable
```sh
chmod +x setup.sh && chmod +x run.sh
```

3. setup (install require dependencies)
```sh
./setup.sh
# or bash setup.sh
# this will install require dependencies both for frontend by ``yarn`` and backend by ``pip``
```

4. run
```sh
./run.sh
# or bash run.sh
# this will run both fronend by ``yarn dev`` and backend by ``gunicorn``
```

5. goto browser
```sh
# by default --
# frontend will run on ip localhost:3000
# backend will run on ip 127.0.0.1:5000
```

## Note
Backend on the first run will download and extract model file to ``backend/model/shn``
the model size is around 400~ MB
- **incase the model download and extract step is run slow, not finished Flask server may cause ``time-out`` and ``return 502``**

workaround is increase gunicorn time-out flag

```sh
# run.sh
# change from python -m gunicorn -w 2 -b 127.0.0.1:5000 app:app --timeout 60
python -m gunicorn -w 2 -b 127.0.0.1:5000 app:app --timeout 300
```
## License
MIT
