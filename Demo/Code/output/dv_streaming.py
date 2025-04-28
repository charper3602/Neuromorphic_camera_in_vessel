import dv_processing as dv
import cv2 as cv
from datetime import timedelta
import time

# Define image space resolution dimensions
resolution = (640, 480)

# Define output event stream with valid resolution



# Declare the callback method for slicer

stream = dv.io.Stream.EventStream(0, "events", "TEST_DATA", resolution)


# Initiate the server, needs stream definition to initiate
server = dv.io.NetworkWriter("127.0.0.1", 5500, stream)

# Print the ready state of the server
print("Waiting for connections...")

# Stream interval defines the packet frequency for this sample
streamInterval = timedelta(milliseconds=33)



# Run indefinitely
while True:
    # Do not produce output if there are no connected clients
    if server.getClientCount() > 0:
        capture = dv.io.CameraCapture()
        capture.setDVSBiasSensitivity(dv.io.CameraCapture.BiasSensitivity.Low)
        resolution = (640, 480)
        # Make sure it supports event stream output, throw an error otherwise
        if not capture.isEventStreamAvailable():
            raise RuntimeError("Input camera does not provide an event stream.")

        # Initialize an accumulator with some resolution
        visualizer = dv.visualization.EventVisualizer(resolution)

        # Apply color scheme configuration, these values can be modified to taste
        visualizer.setBackgroundColor(dv.visualization.colors.white())
        visualizer.setPositiveColor(dv.visualization.colors.iniBlue())
        visualizer.setNegativeColor(dv.visualization.colors.darkGrey())

        # Initialize a preview window
        #cv.namedWindow("Preview", cv.WINDOW_NORMAL)

        # Initialize a slicer
        slicer = dv.EventStreamSlicer()


        # Declare the callback method for slicer
        def slicing_callback(events: dv.EventStore):
            # Generate a preview frame
            fFilter = dv.EventFilterChain()
            
        # Allow positive polarity events only
           # fFilter.addFilter(dv.EventPolarityFilter(True))
            fFilter.addFilter(dv.noise.BackgroundActivityNoiseFilter(resolution, backgroundActivityDuration=timedelta(milliseconds=1)))
            fFilter.addFilter(dv.RefractoryPeriodFilter(resolution, timedelta(milliseconds=1)))
            fFilter.addFilter(dv.noise.FastDecayNoiseFilter(resolution,
                                       halfLife=timedelta(milliseconds=10),
                                       subdivisionFactor=4,
                                       noiseThreshold=1.0))
        # Initialize a background activity noise filter with 10-millisecond half life decay, resolution subdivision
        # factor of 4 and noise threshold of 1. Half life decay and noise threshold values controls the quality of
        # filtering, while subdivision factor is used for resolution downsizing for internal event representation.
           
            fFilter.accept(events)
            filtered= fFilter.generateEvents()
            server.writeEvents(filtered)
            #frame = visualizer.generateImage(events)

            # Show the accumulated image
           # cv.imshow("Preview", frame)
            #cv.waitKey(2)


        # Register callback to be performed every 33 milliseconds
        slicer.doEveryTimeInterval(timedelta(milliseconds=33), slicing_callback)

        # Run the event processing while the camera is connected
        while capture.isRunning():
            # Receive events
            events = capture.getNextEventBatch()

            # Check if anything was received
            if events is not None:
                # If so, pass the events into the slicer to handle them
                slicer.accept(events)
        

    # Sleep the application for the streaming interval duration
    time.sleep(streamInterval.total_seconds())
