# chatllm

To run this code, you need a GPU at least with 8GB Graphics Memory


First sync dependencies and run the server

```shell
rye sync
rye run python openai_api.py
```

Then create a new shell process, and run the following

```shell
rye run python chain.py
```

