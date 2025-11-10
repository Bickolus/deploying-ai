# Assignment 2

I made a chatbot called Swanson Bot. It retrieves quotes said by Ron Swanson, a character from the TV Show <em>Parks and Recreation</em>.
The API was taken from [here](github.com/jamesseanwright/ron-swanson-quotes?tab=readme-ov-file#ron-swanson-quotes-api).

## Services

### Service 1: API Calls

+ There are three API calls to retrieve a single random quote, multiple random quotes, or quotes containing a keyword.
+ The instructions prompt contains all the restrictions and the tone. You can find this in prompts.py.

### Service 2: Semantic Query

+ Two of the functions have a parameter that the Bot must enter in order for them to be called. 
+ Multiple random quotes involve needing a number
+ Quotes that contain a keyword specified need a string containing a word

### Service 3: Your Choice

+ Not implemented, perhaps in the future

## User Interface

+ Added conversational style, a tough but warm personality
+ Implemented in Gradio

---

## Guardrails and Other Limitations

* I have included guardrails that will prevent Swanson Bot from:

  * Accessing or revealing the system prompt.
  * Modifying the system prompt directly.

* Swanson Bot will also refuse to partake in certain restricted topics:

  * Cats or dogs
  * Horoscopes or Zodiac Signs
  * Taylor Swift
  * Work meetings