import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from app import db
from flask_login import current_user


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


class Exercises:
    counter = 0
    stage = None

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(min_detection_confidence=0.95, min_tracking_confidence=0.95)

    def gen_curl(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            hip= [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            shoulder = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            # if (0 < shoulder[0] < frame.shape[1] and 0 < shoulder[1] < frame.shape[0] and \
            #    0 < elbow[0] < frame.shape[1] and 0 < elbow[1] < frame.shape[0] and \
            #    0 < wrist[0] < frame.shape[1] and 0 < wrist[1] < frame.shape[0]):
            counter_angle = calculate_angle(shoulder, elbow, wrist)
            checker_angle = calculate_angle(hip, shoulder, elbow)
            if counter_angle > 170:
                self.stage = "down"
            if counter_angle < 30 and self.stage == 'down':
                self.stage = "up"
                self.counter += 1

                current_user.exercise5_counter += 1
                db.session.add(current_user)
                db.session.commit()
            if checker_angle > 15:
                cv2.putText(image, 'PRESS HANDS', (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5,
                            cv2.LINE_AA)

            cv2.rectangle(image, (0, 0), (225, 73), (230, 37, 69), -1)

            cv2.putText(image, 'REPS', (25, 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(self.counter),
                        (30, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, 'STAGE', (145, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, self.stage, (130, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        self.mp_drawing.draw_landmarks(image, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 40, 0), thickness=2, circle_radius=2),
                                       self.mp_drawing.DrawingSpec(color=(230, 37, 69), thickness=2, circle_radius=2)
                                       )

        frame = cv2.imencode('.jpg', image)[1].tobytes()
        return frame
        # key = cv2.waitKey(20)
        # if key == 27:
        #     break

    def gen_push_up(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            nose = [landmarks[self.mp_pose.PoseLandmark.NOSE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.NOSE.value].y]
            shoulder_left = [landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            shoulder_right = [landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_left = [landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            elbow_right = [landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                     landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_left = [landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            wrist_right = [landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                     landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            hip_left = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            hip_right = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee_left = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            knee_right = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            shoulder_angle_left = calculate_angle(shoulder_left, elbow_left, wrist_left)
            shoulder_angle_right = calculate_angle(shoulder_right, elbow_right, wrist_right)
            back_angle = calculate_angle(shoulder_left, hip_left, knee_left)
            # and nose[1] > shoulder[1]
            if shoulder_angle_left <= 100 and nose[1] > shoulder_left[1]:
                self.stage = "down"
            if shoulder_angle_left >= 160 and self.stage == 'down':
                self.stage = "up"
                self.counter += 1
                # sound.play()
                current_user.exercise3_counter += 1
                db.session.add(current_user)
                db.session.commit()

            if back_angle < 170:
                cv2.putText(image, 'BAD BACK', (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5,
                            cv2.LINE_AA)

        cv2.rectangle(image, (0, 0), (225, 73), (230, 37, 69), -1)

        cv2.putText(image, 'REPS', (25, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter),
                    (30, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(image, 'STAGE', (145, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage, (130, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        self.mp_drawing.draw_landmarks(image, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 40, 0), thickness=2, circle_radius=2),
                                       self.mp_drawing.DrawingSpec(color=(230, 37, 69), thickness=2, circle_radius=2)
                                       )

        frame = cv2.imencode('.jpg', image)[1].tobytes()
        return frame

    def gen_squat(self, frame):

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            hip = [landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
            knee = [landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            ankle = [landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            hip_knee_ankle_angle = calculate_angle(hip, knee, ankle)

            if hip_knee_ankle_angle >= 160:
                self.stage = "up"
            if hip_knee_ankle_angle <= 90 and self.stage == 'up':
                self.stage = "down"
                self.counter += 1
                current_user.exercise4_counter += 1
                db.session.add(current_user)
                db.session.commit()

            if hip_knee_ankle_angle < 60:
                cv2.putText(image, 'TOO LOW', (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5,
                            cv2.LINE_AA)

        cv2.rectangle(image, (0, 0), (225, 73), (230, 37, 69), -1)

        cv2.putText(image, 'REPS', (25, 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter),
                    (30, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.putText(image, 'STAGE', (145, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage, (130, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(image, 'TOO LOW', (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5,
        # cv2.LINE_AA)

        self.mp_drawing.draw_landmarks(image, result.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 40, 0), thickness=2, circle_radius=2),
                                       self.mp_drawing.DrawingSpec(color=(230, 37, 69), thickness=2, circle_radius=2)
                                       )

        frame = cv2.imencode('.jpg', image)[1].tobytes()
        return frame
        # key = cv2.waitKey(20)
    # if key == 27:
    # break

    # return counter
