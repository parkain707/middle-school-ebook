import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "mail_config.json")
SENT_DIR = os.path.join(BASE_DIR, "sent_emails")

DEFAULT_CONFIG = {
    "simulation_mode": True,  # True: 실제 메일서버 없이 sent_emails 폴더에 저장, False: 실제 SMTP 발송
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_user": "your_email@gmail.com",
    "smtp_password": "your_app_password",
    "sender_name": "6학년 3반 담임 선생님 (박희망)",
    "sender_email": "hope_park_classroom@school.net"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
        return DEFAULT_CONFIG
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def send_ebook_email(buyer_name, buyer_email, access_token, download_base_url="http://localhost:8000"):
    config = load_config()
    os.makedirs(SENT_DIR, exist_ok=True)
    
    download_url = f"{download_base_url}/download?token={access_token}"
    reader_url = f"{download_base_url}/view?token={access_token}"
    
    subject = f"[6학년 3반 교실 연구소] {buyer_name}님, 《꿈을 여는 공부의 새벽》 전자책 완결본 다운로드 안내"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: 'Pretendard', sans-serif; background-color: #f8fafc; padding: 30px; color: #1e293b;">
        <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background: linear-gradient(135deg, #0f172a, #1e3a8a); padding: 25px; text-align: center; color: #ffffff;">
                <h1 style="margin: 0; font-size: 20px; font-weight: 700;">꿈을 여는 공부의 새벽</h1>
                <p style="margin: 6px 0 0 0; font-size: 13px; color: #93c5fd;">중학교 첫 시험 전교 1등 시크릿 (44페이지 대형 완결본)</p>
            </div>
            
            <div style="padding: 25px;">
                <p style="font-size: 15px; line-height: 1.6; margin-top: 0;">
                    안녕하세요, <strong>{buyer_name}</strong>님!<br>
                    <strong>6학년 3반 담임 선생님</strong>입니다.
                </p>
                <p style="font-size: 14px; line-height: 1.6; color: #475569;">
                    경제앱으로 <strong>박희망</strong>에게 보내주신 <strong>70,000 미소</strong> 입금이 정상 확인되었습니다.<br>
                    구매해주신 예비 중1 10대 전 과목 자기주도 공부 비법 전자책 정식 완결본(PDF)을 발송해 드립니다.
                </p>
                
                <div style="background: #f1f5f9; border-radius: 8px; padding: 18px; margin: 20px 0;">
                    <h3 style="margin: 0 0 10px 0; font-size: 14px; color: #0f172a;">📦 주문 및 결제 내역 확인</h3>
                    <ul style="margin: 0; padding-left: 20px; font-size: 13px; color: #334155; line-height: 1.8;">
                        <li><strong>수령자</strong>: {buyer_name}님</li>
                        <li><strong>발송 이메일</strong>: {buyer_email}</li>
                        <li><strong>교재값</strong>: 70,000 미소 (입금 확인 완료)</li>
                        <li><strong>결제 수단</strong>: 경제앱으로 박희망에게 입금</li>
                        <li><strong>도서 규격</strong>: 44페이지 고해상도 PDF (2.07 MB)</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{download_url}" style="background: #2563eb; color: #ffffff; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-weight: 700; font-size: 15px; display: inline-block; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);">
                        📥 44페이지 전자책 PDF 즉시 다운로드
                    </a>
                </div>
                
                <p style="font-size: 12px; color: #64748b; text-align: center;">
                    다운로드 링크는 보안 토큰 기반으로 작동하며 언제든 다시 열람하실 수 있습니다.<br>
                    웹 브라우저에서 바로 읽기: <a href="{reader_url}" style="color: #2563eb;">[온라인 리더 열기]</a>
                </p>
                
                <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 25px 0;">
                
                <p style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin-bottom: 0;">
                    발행처: 6학년 3반 교실 연구소 | 지은이: 6학년 3반 담임 선생님<br>
                    본 도서는 전자상거래법 제17조 제2항에 따라 디지털 파일 다운로드 링크 제공 후 청약철회가 제한됩니다.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join([c for c in buyer_name if c.isalnum() or c in (' ', '_')]).strip()
    
    if config.get("simulation_mode", True):
        # 시뮬레이션 모드: 파일로 즉시 저장하여 육안 검증 가능
        file_path = os.path.join(SENT_DIR, f"email_{timestamp}_{safe_name}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"[MAIL_SIMULATION_SUCCESS] 이메일 발송 완료 (시뮬레이션 모드 저장: {file_path})")
        return {"status": "SUCCESS_SIMULATED", "path": file_path, "download_url": download_url}
    else:
        # 실제 SMTP 인터넷 발송
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{config['sender_name']} <{config['sender_email']}>"
            msg["To"] = buyer_email
            
            part = MIMEText(html_body, "html", "utf-8")
            msg.attach(part)
            
            pdf_path = os.path.join(BASE_DIR, "ebook_final.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    attach = MIMEApplication(f.read(), _subtype="pdf")
                    attach.add_header('Content-Disposition', 'attachment', filename="꿈을_여는_공부의_새벽_완결본.pdf")
                    msg.attach(attach)
                    
            with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
                server.starttls()
                server.login(config["smtp_user"], config["smtp_password"])
                server.sendmail(config["sender_email"], [buyer_email], msg.as_string())
                
            print(f"[REAL_MAIL_SENT_SUCCESS] 실제 이메일 발송 완료 -> {buyer_email}")
            return {"status": "SUCCESS_REAL", "to": buyer_email, "download_url": download_url}
        except Exception as e:
            print(f"[MAIL_ERROR] 실제 메일 발송 실패: {e}")
            # 폴백: 시뮬레이션 파일 저장
            file_path = os.path.join(SENT_DIR, f"email_FALLBACK_{timestamp}_{safe_name}.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_body)
            return {"status": "FALLBACK_SAVED", "error": str(e), "path": file_path}

if __name__ == "__main__":
    res = send_ebook_email("김민준", "test@example.com", "tok_test_sample_123")
    print("Test Result:", res)
