# track-immoscoop

Steps:

1. fetch HTML page
2. parse EPC values and price
3. save parsed fields to CSV

## Fetch HTML page

Url `https://www.immoscoop.be/zoeken/te-huur/brugge/appartement?minBedrooms=1&maxBedrooms=2&maxPrice=900&maxEpcScore=200&sort=price%2CASC`.

## Parse EPC values and price

The HTML page contains several property cards like this:

<a data-mobile-selector="property-card_card" href="/te-huur/8200-sint-michiels/838015">...</a>

... contains other HTML elements. Nested within these elements you find the values I'm interested in.
Parse these values for all property cards.

Example price element: `<p class="property-card_price__XfyPH">€&nbsp;750</p>`
Example EPC element: `<text class="epc-icon_label__9I0Hb" x="58.0352" y="13.948">A</text>`

The parts after `__` are the same for every property card.

## Save parsed fields to CSV
