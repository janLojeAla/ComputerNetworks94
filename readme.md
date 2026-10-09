# Simple CLI Chat

A small TCP chat application with a threaded server and command-line clients. The server relays private messages between connected users and reports who is online.

## Requirements

- Python 3
- No third-party packages; the client and server use only Python's standard library.

## Installation

1. Make sure `python3` is available in your terminal.
2. Keep `client.py` and `server.py` in the same directory. There is nothing else to install.

## Run the server

In a terminal, from the project directory, start:

```sh
python3 server.py
```

The server listens on TCP port **5379** on all network interfaces. It prints an IP address and port at startup. Leave this terminal running while chatting. Stop the server with **Ctrl+C**.

## Connect a client

Open another terminal in the project directory and run:

```sh
python3 client.py
```

When prompted, enter:

1. **Server ip** — use `127.0.0.1` when the server is on the same computer; otherwise enter the server's reachable IP address (the server prints a suggested address at startup).
2. **port** — enter `5379`.
3. **Name** — enter a username. Use a name without spaces; each connected user must have a unique name.

Run the client command again in another terminal or computer to connect additional users. For computers on a network, ensure the server's TCP port 5379 is reachable through the host firewall and network configuration.

## Client commands

- `!who` — list connected usernames.
- `@<username> <message>` — send a private message to a connected user. Example: `@alice Hi, are you there?`
- `!quit` — exit the client.

Messages addressed to a user who is not connected are not delivered. The server supports up to 64 simultaneous clients.
