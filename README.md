# Program-trade

## What is this

This is a lab of cource *Program-trade*.

## How to use

1. create a venv environment named `venv-quant`.

```shell
python -m venv venv-quant
```

2. install all packages.

```shell
./venv/Scripts/python.exe -m pip install -r ./requirements.txt
```

3. select MODE in `./src/configs/configs.py`.
4. run `./src/main.py`.

```shell
./venv/Scripts/python.exe ./src/main.py
```

5. you can also run it with some args, for example run it as follow.

```shell
./venv/Scripts/python.exe ./src/main.py --force_select_data=True
```

This force the program to regenerate selected data xlsx file.

6. for more information, please see `./src/main.py`, `./src/configs/configs.py` and `src/configs/parser.py`.