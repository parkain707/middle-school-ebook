# -*- coding: utf-8 -*-
from database import create_order, approve_order, get_orders, verify_token
from mailer import send_ebook_email
import os

print("=== [Sentinel QA] 데이터베이스 및 자동 발송 엔드투엔드 무결점 검증 시작 ===")

# 1. 신규 주문 생성 시험
order_id, token = create_order(buyer_name="이서준", buyer_email="seojun2026@school.net", buyer_phone="010-1234-5678")
print(f"1. 주문 생성 성공 -> 주문번호: {order_id}, 보안토큰: {token[:12]}...")

# 2. 토큰 사전 열람 시도 (미입금 차단 검증)
check_unapproved = verify_token(token)
assert check_unapproved is None, "미승인 토큰이 통과되었습니다! 결함 발생"
print("2. 미입금 토큰 열람 차단 검증 -> PASS (미승인 상태 열람 불가 확인)")

# 3. 박희망 선생님 입금 확인 및 승인
approved_order = approve_order(order_id)
assert approved_order is not None, "주문 승인 실패"
assert approved_order["status"] == "APPROVED", "상태 변경 실패"
print(f"3. 입금 승인 완료 -> 상태: {approved_order['status']}, 승인일시: {approved_order['approved_at']}")

# 4. 이메일 자동 발송 엔진 가동
mail_res = send_ebook_email(
    buyer_name=approved_order["buyer_name"],
    buyer_email=approved_order["buyer_email"],
    access_token=approved_order["access_token"]
)
print(f"4. 이메일 발송 결과 -> 상태: {mail_res['status']}, 파일: {mail_res.get('path')}")
assert os.path.exists(mail_res.get('path')), "발송 이메일 파일이 생성되지 않았습니다!"

# 5. 승인 후 토큰 다운로드 검증
check_approved = verify_token(token)
assert check_approved is not None, "승인된 토큰 검증 실패"
assert check_approved["download_count"] >= 1, "다운로드 카운트 증가 실패"
print(f"5. 승인 토큰 정식 열람 & 다운로드 검증 -> PASS (다운로드 횟수: {check_approved['download_count']}회)")

print("[QA ALL PASS] 데이터베이스 구축 및 이메일 자동 발송 파이프라인 100% 무결점 통과!")
