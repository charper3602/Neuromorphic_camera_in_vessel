import dv_processing as dv
import cv2 as cv
from datetime import timedelta

# Open any camera
capture = dv.io.CameraCapture()

#set the bias sensitivity of the event camera(verylow = more light intensity required to trigger event)
capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.VeryLow)

# Make sure it supports event stream output, throw an error otherwise
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")

# Initialize an accumulator with some resolution
accumulator = dv.Accumulator(capture.getEventResolution())

# Apply accumulator configuration
accumulator.setMinPotential(0.0)
accumulator.setMaxPotential(1.0)
accumulator.setNeutralPotential(0.0)    #Setting this to 0.0 means that no change shows as black
accumulator.setEventContribution(0.05)
accumulator.setDecayFunction(dv.Accumulator.Decay.EXPONENTIAL)
accumulator.setDecayParam(1e+6)         #1 second for event to decay fully
accumulator.setIgnorePolarity(False)
accumulator.setSynchronousDecay(False)


# Initializing a slicer
slicer = dv.EventStreamSlicer()



# Callback method for slicer
def slicing_func(events: dv.EventStore):
    # Pass events into the accumulator and generate a preview frame
    accumulator.accept(events)
    frame = accumulator.generateFrame()
    # Show the accumulated image
    cv.imshow("Preview", frame.image)
    cv.waitKey(2)


# Slicer calls back to function every 33ms(30fps)
slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicing_func)

# Run the event processing while the camera is connected
while capture.isRunning():
    # Receive events
    events = capture.getNextEventBatch()

    # Check if anything was received
    if events is not None:
        print(events.coordinates())

        # If so, pass the events into the slicer to handle them
        slicer.accept(events)   #once slicer reaches timedelta of 33ms, loop will break 
                                #and slicer will execute the callback function

#once code has finished executing, close all opencv windows
cv.destroyAllWindows()
