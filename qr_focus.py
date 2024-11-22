import cv2
import math

# QRCodeDetector 초기화
qr_detector = cv2.QRCodeDetector()

# 카메라 연결 (인덱스 2번)
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 연결 상태를 확인하세요.")
    exit()

# 카메라의 수평 시야각(FOV) 설정 (단위: 도)
camera_fov = 70  # 일반적인 웹캠의 FOV

# 화면 크기 가져오기
ret, frame = cap.read()
if not ret:
    print("프레임을 읽을 수 없습니다.")
    cap.release()
    exit()

frame_height, frame_width = frame.shape[:2]
screen_center_x = frame_width // 2  # 화면 중심 x 좌표

print("QR 코드 탐지와 초점 측정을 시작합니다. 'q'를 눌러 종료하세요.")

# 초점 측정 함수
def measure_focus(frame):
    """이미지의 초점 정도를 측정"""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Grayscale 변환
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)  # Laplacian 필터 적용
    variance = laplacian.var()  # 분산 계산
    return variance

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # QR 코드 탐지
    data, points, _ = qr_detector.detectAndDecode(frame)

    if points is not None:
        # QR 코드 중심 계산
        points = points[0].astype(int)
        qr_center_x = sum(point[0] for point in points) // 4  # x 좌표 평균

        # QR 코드 중심과 화면 중심 간의 좌우 이동 거리 계산
        delta_x = qr_center_x - screen_center_x

        # 좌우 각도 계산 (픽셀 거리 -> 각도 변환)
        angle = (delta_x / frame_width) * camera_fov

        # QR 코드 중심 표시
        cv2.circle(frame, (qr_center_x, frame_height // 2), 5, (255, 0, 0), -1)

        # QR 코드 데이터와 각도 출력
        cv2.putText(frame, f"QR Data: {data}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(frame, f"Angle: {angle:.2f} degrees", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    # 초점 측정
    focus_measure = measure_focus(frame)

    # 초점 상태 출력
    if focus_measure < 100:  # 임계값 설정 (100 이하이면 흐림)
        focus_status = "Blurry (Out of Focus)"
        color = (0, 0, 255)  # 빨간색 (초점 나감)
    else:
        focus_status = "Sharp (In Focus)"
        color = (0, 255, 0)  # 초록색 (초점 맞음)

    cv2.putText(frame, f"Focus Measure: {focus_measure:.2f}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    cv2.putText(frame, focus_status, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    # 화면 중심 표시
    cv2.line(frame, (screen_center_x, 0), (screen_center_x, frame_height), (0, 255, 0), 1)

    # 화면 출력
    cv2.imshow("QR Code and Focus Detection", frame)

    # 'q' 키를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
