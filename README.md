# Quest Engine

Version: 0.1.3 - Completion of GUI (for now)

This repository will contain an AI enhanced, text-adventure game engine that will allow users to create open world text adventures with the help of an LLM and play them with features that add more interacitveness and immersion using an LLM. 

## Features
- Open world
- LLM creating immersion by:
    - controlling npcs
    - interpreting commands
    - describing the outcome of actions
    - deciding the consequences of certain actions

## Requirements

- Python 3.12 or later
- openai (you will need you own API key)

### Dependencies
- openai (GPT) 
NOTE: I hope to one day be able to run the LLM locally, but we'll have to wait for technology to catch up to my dreams for that :( 

## Usage

To use quest engine, clone this repository.

`git clone https://github.com/levgrav/guest-engine.git`

As of right now ony the `quest-engine-create` application exists. To run it, run `src/quest-engine-create/main.py`

You will need to create a file called `openai_api_key.txt` in the base directory with a valid API key in order to use any of the LLM features

## Lisence

MIT License (c) 2023 Levi Eby. See `LICENSE.md` for more details.

## Credits

This game engine was (and is currently being) developed by Levi Eby.
