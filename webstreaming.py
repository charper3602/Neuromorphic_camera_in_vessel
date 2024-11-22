#from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse
import datetime
#import imutils
#import time
import cv2
import dv_processing as dv



resolution = (640, 480)


# Open any camera
capture = dv.io.CameraCapture()

# Make sure it supports event stream output, throw an error otherwise
if not capture.isEventStreamAvailable():
    raise RuntimeError("Input camera does not provide an event stream.")


# Initialize a slicer
# Initialize an accumulator with some resolution
accumulator = dv.Accumulator(capture.getEventResolution())
# Apply configuration, these values can be modified to taste
accumulator.setMinPotential(0.0)
accumulator.setMaxPotential(1.0)
accumulator.setNeutralPotential(0.0)
accumulator.setEventContribution(0.05)
accumulator.setDecayFunction(dv.Accumulator.Decay.EXPONENTIAL)
accumulator.setDecayParam(1e+6)
accumulator.setIgnorePolarity(False)
accumulator.setSynchronousDecay(False)
#slicer = dv.EventStreamSlicer()



# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames (useful when multiple browsers/tabs
# are viewing the stream)
outputFrame = None
lock = threading.Lock()
# initialize a flask object
app = Flask(__name__)

@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")


def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock, evStore, events
	
	# loop over frames from the output stream
	while capture.isRunning():
		evStore = dv.EventStore()
		# Register a callback every 33 milliseconds(30fps)
		#slicer.doEveryTimeInterval(timedelta(milliseconds=33), genFrame)
		
		# Accumulate every 1000 events
		while evStore.size() < 1000:
			
			# Receive events
			events = capture.getNextEventBatch()
			# Check if anything was received
			if events is not None:
				#add events to store	
				evStore.add(events)

		#check that the event store is not empty
		if evStore is not None:
			accumulator.accept(evStore)
			framegr = accumulator.generateFrame()
			#framegr = imutils.resize(framegr,width=400)
			frame = cv2.cvtColor(framegr.image,cv2.COLOR_GRAY2BGR)
			# grab the current timestamp and draw it on the frame
			timestamp = datetime.datetime.now()
			cv2.putText(frame,timestamp.strftime("%A %d %B %Y %I:%M:%S%p"),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)
			#acquire the lock, set the output frame, and release the lock
			with lock:
				outputFrame = frame.copy()
				#check if the output frame is available, otherwise skip
				#the iteration of the loop
				if outputFrame is None:
					return
				#encode the frame in JPEG format
				(flag,encodedImage) = cv2.imencode(".jpg",outputFrame)
				#ensure the frame was successfully encoded
				if not flag:
					return
			#yield the output frame in the byte format
			yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

		
@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':
	# construct the argument parser and parse command line arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
	ap.add_argument("-o", "--port", type=int, required=True,
		help="ephemeral port number of the server (1024 to 65535)")
	ap.add_argument("-f", "--frame-count", type=int, default=32,
		help="# of frames used to construct the background model")
	args = vars(ap.parse_args())
	
	# start the flask app
	app.run(host=args["ip"], port=args["port"], debug=True,
		threaded=True, use_reloader=False)
