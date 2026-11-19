"""
Cognitive Computing Assignment - Question 2
Emotion-Aware Cognitive Assistant using Facial Expression Detection

Install:
    pip install opencv-python deepface tf-keras

The first run may take longer because DeepFace downloads its model.
Press Q in the webcam window to quit.

Note: The program estimates facial expressions. It cannot know a person's
actual feelings or mental state with certainty.
"""
import cv2


def main():
    try:
        from deepface import DeepFace
    except ImportError:
        print("DeepFace is not installed.")
        print("Run: pip install deepface tf-keras")
        return

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Could not open webcam. Check camera connection and permissions.")
        return

    print("Emotion-aware assistant started.")
    print("Look toward the camera. Press Q in the video window to quit.")

    current_emotion = "Detecting..."
    frame_number = 0

    # A simple supportive response for the expression estimate.
    responses = {
        "happy": "You seem to be smiling. Keep spreading positivity!",
        "sad": "You may look sad. Consider taking a break or talking to someone.",
        "angry": "You may look upset. Take a slow breath and pause for a moment.",
        "fear": "You may look worried. Try to relax and take a few deep breaths.",
        "surprise": "You look surprised!",
        "disgust": "Your expression may show discomfort.",
        "neutral": "You appear to have a neutral expression.",
    }

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Could not read a frame from the webcam.")
                break

            frame_number += 1

            # Analyse every 8th frame to reduce processing time.
            if frame_number % 8 == 0:
                try:
                    result = DeepFace.analyze(
                        img_path=frame,
                        actions=["emotion"],
                        detector_backend="opencv",
                        enforce_detection=False,
                        silent=True,
                    )
                    if isinstance(result, list) and result:
                        current_emotion = result[0].get(
                            "dominant_emotion", "unknown"
                        ).lower()
                    elif isinstance(result, dict):
                        current_emotion = result.get(
                            "dominant_emotion", "unknown"
                        ).lower()
                except Exception:
                    # Keep the last estimate if no face is detected in a frame.
                    pass

            response = responses.get(
                current_emotion,
                "Expression detected: " + current_emotion
            )

            cv2.putText(
                frame,
                "Estimated expression: " + current_emotion,
                (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                response[:75],
                (15, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                (255, 255, 255),
                1,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame, "Press Q to quit", (15, 105),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 200, 255), 2
            )

            cv2.imshow("Emotion-Aware Cognitive Assistant", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()

    print("Emotion detection stopped.")


if __name__ == "__main__":
    main()
