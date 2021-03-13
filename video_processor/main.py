import os
import cv2
import time
import caffe
import argparse
import requests
import threading
import numpy as np
from PIL import Image

MODEL_FILE = './model/deploy.prototxt'
PRETRAINED = './model/snapshot_iter_6318.caffemodel'

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"


def cut_out_lots(frame, parking_map):
    """
        Cut out parking lots from the image of the entire parking site using a parking map.
    """

    for lot in parking_map:

        # Fetch id
        id = lot['id']

        # Unpack coordinates
        xs, ys, xe, ye = lot['coordinates']

        # Yield region with parking lot
        yield id, frame[ys:ye, xs:xe]


def get_image_data(img):
    """
        Format parking lot image to match the input layer of the neural network.
    """

    # Resize to match input of our model
    img = Image.fromarray(img).resize(size=(224, 224))

    # Convert back to numpy array
    img = np.array(img)

    # Make sure format is right
    img = img.astype(np.uint8)

    # Flatten image
    img_data = np.asarray([img.transpose(2, 1, 0)])

    # Normalize image
    img_data = np.divide(img_data, 256.0)

    return img_data


def is_occupied(net, img_data):
    """
        Check if parking lot is occupied.
    """

    # Execute prediction
    out = net.forward_all(data=img_data)

    # Return prediction
    return np.argmax(out['score']) == 1


def receiver(stream_url, frame_lock, tts=60):
    """
        Thread that recieve frame from RTSP stream every @tts seconds. 
    """

    global curr_frame

    print(f'[INFO] <rec> Receiver started!')
    print(f'[INFO] <rec> Stream URL: {stream_url}')

    # Initialize video stream capturing
    cap = cv2.VideoCapture(stream_url)

    while cap.isOpened():

        # Save start time
        start_time = time.time()

        # Read frame from video stream
        ret, frame = cap.read()

        # Stop loop if unable to get frame
        if not ret:
            print('[ERROR] Unable to get frame!')
            break

        # Set current frame
        with frame_lock:
            curr_frame = frame

        print('[INFO] <rcv> Got New Frame!')

        # Wait N seconds
        wt = tts - (time.time() - start_time)
        if wt > 0:
            time.sleep(wt)

        # Get id of latest frame
        frameId = cap.get(cv2.CAP_PROP_POS_FRAMES)  # Current Frame ID

        # Make sure next frame is last one
        cap.set(1, frameId)

    print(f'[INFO] <rec> Receiver stopped!')


def processor(core_url, processor_id, frame_lock, parking_map):
    """
        Thread that process parking site images and submit updates to the core.
    """

    global curr_frame

    # Load neural network
    net = caffe.Net(MODEL_FILE, PRETRAINED, caffe.TEST)

    # Set cpu mode cause we don't have gpu version
    caffe.set_mode_cpu()

    print('[INFO] <prc> Processor started!')

    while True:

        frame = None

        with frame_lock:
            if curr_frame is not None:
                frame = np.copy(curr_frame)

        if frame is not None:

            lots = cut_out_lots(frame, parking_map)

            states = []

            # For each parking lot
            for id, img in lots:

                # Match image to neural net requirements
                img_data = get_image_data(img)

                states += [{
                    'id': id,
                    'is_occupied': is_occupied(net, img_data)
                }]

            print(f'[INFO] <prc> Parking State: {states}')

            # Submit new parking state to the Core
            requests.post(
                f'{core_url}/api/processors/{processor_id}/lots/', data=states)

            # Clear current frame
            with frame_lock:
                curr_frame = None

        # Wait before next check
        time.sleep(1)

    print('[INFO] <prc> Processor stopped!')


if __name__ == '__main__':

    # Parse input arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--processor_id', type=str,
                        help='Video Processor Id', required=True)
    parser.add_argument('-u', '--core_url', type=str,
                        help='URL Address of Core endpoint', required=True)

    args = parser.parse_args()

    processor_id = args.processor_id
    core_url = args.core_url

    # Get parking map
    response = requests.get(f'{core_url}/api/processors/{processor_id}/map')
    parking_map = response.json()

    # Get rtsp stream url
    response = requests.get(f'{core_url}/api/processors/{processor_id}/rtsp')
    rtsp_url = response.json()['url']

    global curr_frame
    curr_frame = None

    # Lock object to safely access current frame from multiple threads
    frame_lock = threading.Lock()

    
    rc_thread = threading.Thread(target=receiver,
                                 args=[rtsp_url, frame_lock],
                                 kwargs={'tts': 60})

    pc_thread = threading.Thread(target=processor,
                                 args=[core_url, processor_id, frame_lock, parking_map])

    # Start receiver and processor
    rc_thread.start()
    pc_thread.start()

    # Wait till they are done
    rc_thread.join()
    pc_thread.join()
