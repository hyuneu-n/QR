import cv2

# QRCodeDetector 초기화
qr_detector = cv2.QRCodeDetector()

# 외장 카메라 연결
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 연결 상태를 확인하세요.")
    exit()

print("외장 카메라가 켜졌습니다. 'q'를 눌러 종료하세요.")

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # QR 코드 탐지
    data, points, _ = qr_detector.detectAndDecode(frame)
    
    if points is not None:
        # 바운딩 박스 그리기
        points = points[0].astype(int)  # float -> int로 변환
        for i in range(len(points)):
            cv2.line(frame, tuple(points[i]), tuple(points[(i + 1) % len(points)]), (0, 255, 0), 2)

        # 가로세로 길이 계산
        width = int(((points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2) ** 0.5)
        height = int(((points[1][0] - points[2][0]) ** 2 + (points[1][1] - points[2][1]) ** 2) ** 0.5)
        
        # 길이 화면에 표시 (빨간색)
        cv2.putText(frame, f"Width: {width}px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, f"Height: {height}px", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # QR 코드 데이터 화면에 표시 (흰색)
        if data:
            cv2.putText(frame, f"Data: {data}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # 프레임 출력
    cv2.imshow("QR Code Detection", frame)

    # 'q'를 눌러 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
