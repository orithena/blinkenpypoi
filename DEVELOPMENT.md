
Abstract
========

pypoi is a poi controller written in µPython to be run on ESP8266 and ESP32.


Features
--------

Everything is just planned as of now.

- Provides a WebApp and REST interface for control
- Can show effects from files or generative functions
- Can show a timed sequence of effects
- Can blend effects together
- Effect types:
  - Backgrounds: Tiled or solid colored backgrounds
  - Masks: Cutting shapes out of backgrounds by manipulating brightness 
  - Alphas: Painting over using alpha channel
  - Shaders: Manipulating pixel data from other effects
  - Easiest method seems to be to just give each effect the array
  - Needs an effect priority, though.

Effects need:
- a priority to choose the order of effect execution for any 
  given frame.
- a name
- a callback function that accepts varargs
