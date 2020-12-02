# apple_ii_basic_2_wav
Takes in tolkenized Applesoft basic data and converts to wave file

This program doesn't do much at this point. It currently takes the data from a tolkenized Applesoft Basic program and generates a wave file to be loaded into an Apple II using an audio cable to the cassette port.

The test data for the first commit is from the simplest program I could think of:

### 10 PRINT "A"

If you type that into your Apple II or an emulator and look at the data starting at 0x801 you would see the following data:
10 8 10 0 186 34 65 34 0 0 0

This is put into a python list, hard code into the program for now: program_data = [10, 8, 10, 0, 186, 34, 65, 34, 0, 0, 0]

