# Quest Engine

Version: 0.2.1 - API Key checker

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
NOTE: I hope to one day be able to run the LLM locally, but we'll have to wait for technology to catch up to my dreams for that. I soon plan to add LM Studio capability to it. Unfortunately the LLMs of a reasonable size are pretty stupid right now. 

## Usage

To use quest engine, clone this repository.

`git clone https://github.com/levgrav/guest-engine.git`

There are two applications: Quest Engine Play and Quest Engine Create

To run either of them, run `python src/quest-engine-[ create | play ]/main.py`

You will need to edit the file called `openai_api_key.txt` in the base directory using a valid API key in order to use any of the LLM features. The program will also prompt you in the command line if this is not done.

To follow along with what the model is doing, look at `files/logs/log.txt`

## Lisence

MIT License (c) 2023 Levi Eby. See `LICENSE.md` for more details.

## Credits

This game engine was (and is currently being) developed by Levi Eby.
