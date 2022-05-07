import numpy as np
import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose


class Exersize_service:
    def __init__(self):
        self.counter = 0
        self.calories = 0

    def calculate_angle(self, a, b, c):
        a = np.array(a)  # First
        b = np.array(b)  # Mid
        c = np.array(c)  # End

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def arm_curl(self):
        cap = cv2.VideoCapture(0)
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, elbow, wrist)

                    # Curl counter logic
                    if angle > 160:
                        stage = "down"
                    if angle < 30 and stage == 'down':
                        stage = "up"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def squat(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/squats.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Get coordinates
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    # Calculate angle

                    angle_knee = self.calculate_angle(hip, knee, ankle)  # Knee joint angle

                    # Curl counter logic
                    if angle_knee > 169:
                        stage = "UP"
                    if angle_knee <= 90 and stage == 'UP':
                        stage = "DOWN"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def pull_up(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/pullup3.mp4')
        self.counter = 0
        self.stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(elbow, shoulder, hip)

                    # Curl counter logic
                    if angle > 100:
                        stage = "up"
                    if angle < 90 and stage == 'up':
                        stage = "down"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter
                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def chair_dips(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/Chair Dips.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, hip, knee)

                    # Curl counter logic
                    if angle > 100:
                        stage = "down"
                    if angle < 60 and stage == 'down':
                        stage = "up"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)
                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def crunch(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/crunches.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, hip, knee)

                    # Curl counter logic
                    if angle > 100:
                        stage = "up"
                    if angle < 90 and stage == 'up':
                        stage = "down"
                        self.counter += 1
                        print(self.counter)

                        # Calorie calc logic
                        self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def side_lateral_raise(self):
        cap = cv2.VideoCapture(0)
        self.counter = 0
        self.stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(elbow, shoulder, hip)

                    # Curl counter logic
                    if angle < 30:
                        stage = "up"
                    if angle > 80 and stage == 'up':
                        stage = "down"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def push_up(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/pushup.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, elbow, wrist)

                    # Curl counter logic
                    if angle > 160:
                        stage = "down"
                    if angle < 80 and stage == 'down':
                        stage = "up"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def lunge(self):
        cap = cv2.VideoCapture('/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/Lunge.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    # Calculate angle

                    angle_knee = self.calculate_angle(hip, knee, ankle)  # Knee joint angle

                    # Curl counter logic
                    if angle_knee > 169:
                        stage = "down"
                    if angle_knee <= 90 and stage == 'down':
                        stage = "up"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def leg_raise(self):
        cap = cv2.VideoCapture(
            '/Users/gimseungheon/Desktop/김승헌/sessac_python/cal_excersize/videos/Lying Leg Raises.mp4')
        self.counter = 0
        self.calories = 0
        stage = None
        ## Setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                success, frame = cap.read()

                # Recolor image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Make detection
                results = pose.process(image)

                # Recolor back to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # Get coordinates
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

                    hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

                    knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    # Calculate angle
                    angle = self.calculate_angle(shoulder, hip, knee)

                    # Curl counter logic
                    if angle > 160:
                        stage = "up"
                    if angle < 100 and stage == 'up':
                        stage = "down"
                        self.counter += 1
                        print(self.counter)

                    # Calorie calc logic
                    self.calories = 1 * self.counter

                except:
                    pass

                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (280, 130), (51, 153, 255), -1)

                # Rep data
                cv2.putText(image, 'Reps: ' + str(self.counter),
                            (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Calorie Burnt data
                cv2.putText(image, 'Kcal: ' + str(self.calories),
                            (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 51, 51), 5, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )
                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
