from octolib import mc, flash_element

# flash_element(mc, 'red', 5, duration=2)
# flash_element(mc, 'red', 100)

flash_element(mc, 'red', 255,
              ranges=[
                  (0,None),
                  (7,None),
                  (None,0),
                  (None,7)
              ],
              duration=2)


flash_element(mc, 'green', 255)
flash_element(mc, 'blue', 187, duration=1.2)
