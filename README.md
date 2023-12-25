# GPT vs itself
This library allows two OpenAI GPT assistants to have a discussion.

## How to run
1. Clone this repository to your local machine
2. Set up your OpenAI API key as detailed below
3. Install the packages found in requirements.txt into your environment
4. (Optional) Change the parameters in [config.yaml](config.yaml)
5. Run [scripts/example_main.py](scripts/example_main.py)

## Setting up the API key
To use the OpenAI API, you must have bought credits (as of Dec 2023)
and produced an API key after purchasing credits.

Then, you must add the API key to your ~/.bash_profile file as detailed in the
[OpenAI API Quickstart guide](https://platform.openai.com/docs/quickstart?context=python).

Note: after purchasing credits, your account may take some time (up to a day) to
be functional. Before that, you may run into errors when making API calls.
